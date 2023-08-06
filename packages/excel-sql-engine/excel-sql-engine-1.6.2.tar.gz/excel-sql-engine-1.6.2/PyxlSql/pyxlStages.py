# ---------------------------------------------------------------------------------------------------------------
# PyxlSQL project
# This program and library is licenced under the European Union Public Licence v1.2 (see LICENCE)
# developed by fabien.battini@gmail.com
# ---------------------------------------------------------------------------------------------------------------

from typing import Union
from PyxlSql.pyxlErrors import PyxlSqlInternalError
from PyxlSql.pyxlSheets import PyxlSheet
from PyxlSql.pyxlAbstracts import Clause, Index, AbstractResult
from PyxlSql.pyxlResults import EnvResult, GroupResult, ValueResult
from PyxlSql.pyxlArgs import SheetArg, ExprArg, FieldArg

#
# Execution model for UPDATE and SELECT (with clauses)
#
# A pipeline is built.
# e.g.:  Select --> Where --> Join --> Identity >
# Each stage is an iterator, that implements
#      get_sheets_nb: returns list(sheet nb)
#      __next__():    returns list(indexes): for each sheet, the index for which next stage is valid
#                             or [] when the stage is finished
#   Whenever possible, a stage does NOT store values, and calls get_next() for its predecessor
#   THis is NOT always possible, e.g. with ORDER BY.
#
# TODO: IN THE FUTURE, several Select can be pipelined.
#       in this case, get_next() will ALSO return intermediate values
#       this means that the intermediate value MUST be Named, so we need to introduce 'AS' + rename vars (@0 ...)


class Stage:
    """Element of a Pipeline"""
    def __init__(self):
        pass

    def __iter__(self):
        return self

    def __next__(self) -> AbstractResult:
        raise PyxlSqlInternalError("get_next on base Stage class")

    def get_sheets(self):
        raise PyxlSqlInternalError("get_src_sheets on base Stage class")


class FromStage(Stage):
    """Initial Pipeline element, which just reads its input WS"""

    def __init__(self, sheet_arg: SheetArg):
        super().__init__()
        self.sheet_arg = sheet_arg
        self.iterator = None  # iter(sheet_arg.get_sheet().get_row_range())

    def __iter__(self):
        self.range = self.sheet_arg.get_sheet().get_row_range()
        self.current_row = self.range[0]
        self.last_row = self.range[-1]
        return self

    def __next__(self) -> AbstractResult:
        if self.current_row <= self.last_row:
            self.current_row += 1
            return EnvResult(self.current_row - 1, self.sheet_arg)
        raise StopIteration

    def get_sheets(self):
        return [self.sheet_arg]


class WhereStage(Stage):
    """Pipeline stage for WHERE Clause"""

    def __init__(self, source: Stage, expression: ExprArg):
        super().__init__()
        self.source = iter(source)
        self.expression = expression
        self.src_sheets = source.get_sheets()

    def __iter__(self):
        return self

    def __next__(self) -> AbstractResult:
        while True:
            inputs: AbstractResult = next(self.source)
            src_val = self.expression.evaluate(inputs, None)
            if src_val:
                return inputs
        #  will raise StopIteration if exhausted

    def get_sheets(self):
        return self.src_sheets


class HavingStage(Stage):
    """Pipeline stage for HAVING Clause"""
    def __init__(self, source: Stage, expression: ExprArg):
        super().__init__()
        self.source = iter(source)
        self.expression = expression
        self.src_sheets = source.get_sheets()

    def __iter__(self):
        return self

    def __next__(self) -> AbstractResult:
        while True:
            inputs: AbstractResult = next(self.source)
            src_val = self.expression.evaluate(inputs, None)
            if src_val:
                return inputs
        #  will raise StopIteration if exhausted

    def get_sheets(self):
        return self.src_sheets


class UpdateStage(Stage):
    """Final Pipeline stage for UPDATE Command"""

    def __init__(self, dst_sheet: SheetArg, source: Stage, sets: list[Clause]):
        super().__init__()
        self.dst_sheet = dst_sheet
        self.source = iter(source)
        self.sets = sets
        if source is None:
            #  An update without dedicated source
            self.src_sheets = [dst_sheet]
            # self.dst_index_in_src = 0
        else:
            self.src_sheets = [dst_sheet] + source.get_sheets()

    def execute(self):
        for inputs in self.source:
            dst_row = inputs.get_row(self.dst_sheet)
            outputs = ValueResult()
            for clause in self.sets:
                clause.eval_clause(inputs, outputs)
            for clause in self.sets:
                clause.execute_clause(outputs, dst_row)

    # Does NOT implement get_sheets(self), because final statement


class SelectStage(Stage):
    """Intermediate pipeline stage for SELECT INTO command"""

    def __init__(self, dst_sheet: SheetArg, source: Stage, sets: list[Clause]):
        super().__init__()
        self.dst_sheet: SheetArg = dst_sheet
        self.source = iter(source)
        self.src_sheets: list[PyxlSheet] = [dst_sheet] + source.get_sheets()
        self.sets: list[Clause] = sets

    def get_sheets(self):
        return self.src_sheets

    def __iter__(self):
        return self

    def __next__(self) -> AbstractResult:
        inputs: AbstractResult = next(self.source)
        outputs = ValueResult()
        for clause in self.sets:
            clause.eval_clause(inputs, outputs)
        return outputs
        #  will raise StopIteration if exhausted


class IntoStage(Stage):
    """Final Pipeline stage that writes the values in a new table"""

    def __init__(self, dst_sheet: SheetArg, source: Stage, sets: list[Clause]):
        super().__init__()
        self.dst_sheet: SheetArg = dst_sheet
        self.source: Stage = source
        self.src_sheets: list[PyxlSheet] = [dst_sheet] + self.source.get_sheets()
        self.sets: list[Clause] = sets

    def execute(self):
        dst_row = self.dst_sheet.get_start_of_range()

        for inputs in self.source:
            for clause in self.sets:
                clause.execute_clause(inputs, dst_row)
            dst_row += 1


class GroupByStage(Stage):
    def __init__(self, source: Stage, expression: ExprArg):
        super().__init__()
        self.source = iter(source)
        self.expression = expression
        self.src_sheets = source.get_sheets()
        self.output = []
        self.current_item = 0
        self.max_item = 0

    def __iter__(self):
        values_and_rows = {}
        # build the list of items that have the same values
        for inputs in self.source:
            src_val = self.expression.evaluate(inputs, None)  # FIXME: None should be an ouputs
            if src_val not in values_and_rows:
                values_and_rows[src_val] = GroupResult()
            values_and_rows[src_val].append(inputs)

        self.current_item = 0
        # now, keep only the list of GroupResult
        self.output = list(values_and_rows.values())
        self.max_item = len(values_and_rows)
        return self

    def __next__(self) -> AbstractResult:
        if 0 <= self.current_item < self.max_item:
            res = self.output[self.current_item]
            self.current_item += 1
            return res  # a list with only 1 value, since only 1 field.
        raise StopIteration  # exhausted

    def get_sheets(self):
        return self.src_sheets


class OrderByStage(Stage):
    def __init__(self, source: Stage, expression: ExprArg):
        super().__init__()
        self.source = iter(source)
        self.expression = expression
        self.src_sheets = source.get_sheets()
        self.output = []
        self.current_item = 0
        self.max_item = 0

    def __iter__(self):
        unsorted = []
        for inputs in self.source:
            src_val = self.expression.evaluate(inputs, None)
            unsorted.append((inputs, src_val))

        # TODO: default value should be 0 and not "" when the type is "Number"
        default_val = "" if isinstance(unsorted[0][1], str) else 0
        unsorted.sort(key=lambda item: item[1] or default_val)  # sort in place more efficient than sorted()
        self.output = unsorted
        self.current_item = 0
        self.max_item = len(self.output)

        return self

    def __next__(self):
        if 0 <= self.current_item < self.max_item:
            res = self.output[self.current_item][0]
            self.current_item += 1
            return res
        raise StopIteration  # exhausted

    def get_sheets(self):
        return self.src_sheets


class FullJoinStage(Stage):
    """Intermediate Pipeline stage for all Join commands"""

    def __init__(self, first_arg: Stage, second_arg: Stage,
                 first_expr: Union[ExprArg, FieldArg],
                 second_expr: Union[ExprArg, FieldArg]):
        super().__init__()
        self.first_arg = first_arg
        self.second_arg = second_arg
        self.first_expr = first_expr
        self.second_expr = second_expr
        self.first_sheets = self.first_arg.get_sheets()
        self.second_sheets = self.second_arg.get_sheets()
        self.src_sheets = self.first_sheets + self.second_sheets
        self.index = -1
        self.results = {}
        self.max_index = -1

    def get_sheets(self):
        return self.src_sheets

    def __iter__(self):
        # we compute once the result, and deliver it row by row
        self.results = self.compute_all_rows()
        self.index = -1
        self.max_index = len(self.results)
        return self

    def __next__(self):
        self.index += 1
        if self.index < self.max_index:
            return self.results[self.index]
        raise StopIteration

    @staticmethod
    def eval_on(expression: ExprArg, stage: Stage):
        """Computes all answer to the ON clause,
        results_hash[value] = [rows,...] # list of rows that have this value (each rowS is itself a list of row)
       """
        results_hash = {}

        for inputs in stage:
            val = expression.evaluate(inputs, None)
            if val not in results_hash:
                results_hash[val] = []
            results_hash[val].append(inputs)
        return results_hash

    def compute_all_rows(self):
        first_val_to_results = self.eval_on(self.first_expr, self.first_arg)
        second_val_to_results = self.eval_on(self.second_expr, self.second_arg)

        results: list[AbstractResult] = []  # A list of [row] for each possible value
        chosen_first_list: list[str] = []   # the list of index in the first  list chosen with the ON clause
        chosen_second_list: list[str] = []  # the list of index in the SECOND list chosen with the ON clause
        for val, first_results_list in first_val_to_results.items():
            if val in second_val_to_results:
                # normal behavior. We will have to manage REDUCTION or duplication of dst due to multiple src
                for second_result in second_val_to_results[val]:
                    for first_result in first_results_list:
                        results.append(first_result + second_result)
                        chosen_first_list.append(first_result.signature)
                        chosen_second_list.append(second_result.signature)

        results = self.manage_left_join(chosen_first_list, results)
        results = self.manage_right_join(chosen_second_list, results)

        return results

    def manage_left_join(self, chosen_list: list[str], results: list[AbstractResult]):
        # each EnvResult in the first_arg of LEFT JOIN, must be available in result
        # so, there must be an EnvResult with the same rows
        for first_result in self.first_arg:
            sig = first_result.signature
            if sig not in chosen_list:
                second_result = EnvResult()
                for i in range(0, len(self.second_sheets)):
                    second_result.add_index(Index(-1, self.second_sheets[i]))
                results.append(first_result + second_result)
        return results

    def manage_right_join(self, chosen_list: list[str], results: list[AbstractResult]):
        for second_result in self.second_arg:
            sig = second_result.signature
            if sig not in chosen_list:
                first_result = EnvResult()
                for i in range(0, len(self.first_sheets)):
                    first_result.add_index(Index(-1, self.first_sheets[i]))
                results.append(first_result + second_result)
        return results


class LeftJoinStage(FullJoinStage):
    """Intermediate Pipeline stage for LEFT JOIN commands"""

    def __init__(self, first_arg: Stage, second_arg: Stage,
                 first_expr: Union[ExprArg, FieldArg],
                 second_expr: Union[ExprArg, FieldArg]):
        super().__init__(first_arg, second_arg, first_expr, second_expr)

    def manage_right_join(self, chosen_list, results):
        return results


class RightJoinStage(FullJoinStage):
    """Intermediate Pipeline stage for  RIGHT JOIN commands"""

    def __init__(self, first_arg: Stage, second_arg: Stage,
                 first_expr: Union[ExprArg, FieldArg],
                 second_expr: Union[ExprArg, FieldArg]):
        super().__init__(first_arg, second_arg, first_expr, second_expr)

    def manage_left_join(self, chosen_list, results):
        return results


class InnerJoinStage(FullJoinStage):
    """Intermediate Pipeline stage for  INNER JOIN commands"""
    #       behavior: see https://www.w3schools.com/sql/sql_join_inner.asp
    def __init__(self, first_arg: Stage, second_arg: Stage,
                 first_expr: Union[ExprArg, FieldArg],
                 second_expr: Union[ExprArg, FieldArg]):
        super().__init__(first_arg, second_arg, first_expr, second_expr)

    def manage_left_join(self, chosen_list, results):
        return results

    def manage_right_join(self, chosen_list, results):
        return results
