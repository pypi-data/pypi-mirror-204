# ---------------------------------------------------------------------------------------------------------------
# PyxlSQL project
# This program and library is licenced under the European Union Public Licence v1.2 (see LICENCE)
# developed by fabien.battini@gmail.com
# ---------------------------------------------------------------------------------------------------------------

import re
from typing import Optional
from copy import copy
from PyxlSql.pyxlErrors import PyxlSqlParseError, PyxlSqlExecutionError, PyxlSqlInternalError
from PyxlSql.pyxlWorkbook  import   PyxlWorkbook
from PyxlSql.pyxlAbstracts import AbstractStatement, Clause, Arg, AbstractResult, AbstractRunner
from PyxlSql.pyxlResults import EnvResult, GroupResult, ValueResult
from PyxlSql.pyxlArgs import SheetArg, ExprArg, FieldArg, CstArg, AggregateExprArg, FormulaArg
from PyxlSql.pyxlStages import Stage, UpdateStage, LeftJoinStage, RightJoinStage, WhereStage, \
    GroupByStage, HavingStage, OrderByStage, FromStage, FullJoinStage, SelectStage, IntoStage, \
    InnerJoinStage
from PyxlSql.pyxlPivot import Pivot

# ---------------------------------------------------------------------------------------------------
# class Cmd
# ---------------------------------------------------------------------------------------------------
# CLass Cmd and Class Clause in the same file, because it is simpler for type checking

class Cmd(AbstractStatement):
    name = "ERROR CMD"
    """A statement at the highest level of hierarchy : Command"""

    def __init__(self, runner:AbstractRunner, dst_wb: PyxlWorkbook, dst_sheet_arg: Optional[Arg] = None):
        super().__init__()
        self.runner = runner
        self.dst_wb: PyxlWorkbook = dst_wb
        self.next_sheet_number = 0  # The sheet number of next SheetArg analysed
        self.dst_sheet_arg: Optional[Arg] = dst_sheet_arg
        if self.dst_sheet_arg:
            assert isinstance(dst_sheet_arg, SheetArg), "INTERNAL: Cmd, dst_sheet_arg"
            dst_sheet_arg.set_sheet_number(self.build_sheet_number())

        self.from_arg: Optional[AbstractStatement] = None
        self.source_sheets: list[SheetArg] = []
        self.allows_from = False

        self.joins: list[JoinClause] = []
        self.allows_join = False

        self.sets: list[SetClause, UidClause, FormatClause] = []
        self.allows_set = False

        self.where_clause: Optional[WhereClause] = None
        self.allows_where = False

        self.group_clause: Optional[GroupClause] = None
        self.allows_group = False

        self.having_clause: Optional[HavingClause] = None
        self.allows_having = False

        self.order_by_clause: Optional[OrderByClause] = None
        self.allows_order_by = False

    def is_a_command(self):
        return True

    def build_sheet_number(self):
        self.next_sheet_number += 1
        return self.next_sheet_number - 1

    def add_where(self, clause: AbstractStatement):
        if not self.allows_where:
            raise PyxlSqlParseError(f"WHERE clause not legal for {self.name}", clause.current_line)
        if self.where_clause is not None:
            raise PyxlSqlParseError(f"only 1 WHERE clause for {self.name}", clause.current_line)
        self.where_clause = clause

    def add_source_sheet(self, sheet_arg):
        assert isinstance(sheet_arg, SheetArg), "INTERNAL: add_source_sheet"
        self.source_sheets.append(sheet_arg)

    def sheet_from_alias(self, sheet_alias: str, not_in_src=False, not_in_dst=False) -> SheetArg:
        found = None
        all_sheets = [] if not_in_dst else [self.dst_sheet_arg]
        all_sheets += [] if not_in_src else self.source_sheets
        for sheet in all_sheets:
            assert isinstance(sheet, SheetArg), "INTERNAL: sheet_from_alias"
            if sheet_alias == sheet.alias:
                if found is None:
                    found = sheet
                else:
                    raise PyxlSqlParseError(f"Duplicate alias {sheet_alias}",
                                            f"'{found.get_sheet_name()}' == '{sheet.get_sheet_name()}'")
        return found

    def add_from(self, clause):  # clause MUST be a FromClause
        """
        :param clause: FromClause
        :return: None
        Inserts clause as the FROM element of the Cmd, or raises an error if illegal
        """
        if not self.allows_from:
            raise PyxlSqlParseError(f"FROM clause not legal for {self.name}", clause.current_line)
        if self.from_arg:
            raise PyxlSqlParseError(f"illegal 2nd FROM clause for {self.name}", clause.current_line)
        if self.dst_sheet_arg is None:
            raise PyxlSqlInternalError(f"FROM without a source sheet {self.name}")
        self.from_arg = clause

        self.add_source_sheet(clause)

    def add_group(self, clause: AbstractStatement):
        if not self.allows_group:
            raise PyxlSqlParseError(f"GROUP BY clause not legal for {self.name}", clause.current_line)
        self.group_clause = clause

    def add_having(self, clause: AbstractStatement):
        if not self.allows_having:
            raise PyxlSqlParseError(f"HAVING clause not legal for {self.name}", clause.current_line)
        if self.having_clause is not None:
            raise PyxlSqlParseError(f"only 1 HAVING clause for {self.name}", clause.current_line)
        self.having_clause = clause

    def add_order_by(self, clause: AbstractStatement):
        if not self.allows_having:
            raise PyxlSqlParseError(f"ORDER BY clause not legal for {self.name}", clause.current_line)
        if self.order_by_clause is not None:
            raise PyxlSqlParseError(f"only 1 ORDER clause for {self.name}", clause.current_line)
        self.order_by_clause = clause

    def add_join(self, clause):
        """
        :param clause: JoinClause
        :return: None
        Inserts clause in the list of JOIN element of the Cmd, or raises an error if illegal
        """
        if not self.allows_join:
            raise PyxlSqlParseError(f"JOIN clause not legal for {self.name}", clause.current_line)
        # if len(self.source_sheets) == 0:
        #     raise PyxlSqlParseError(f"JOIN clause without FROM for {self.name}", clause.current_line)
        self.add_source_sheet(clause.first_arg)
        self.joins.append(clause)

    def add_set(self, clause):
        """
        :param clause: Union[SetClause, UidClause, FormatClause]
        :return: None
        """
        if not self.allows_set:
            raise PyxlSqlParseError(f"SET clause not legal for {self.name}", clause.current_line)
        self.sets.append(clause)

    def execute(self):
        raise PyxlSqlInternalError(f"command.execute on {self.name}")


class UpdateCmd(Cmd):
    name = 'UPDATE'
    help = "Updates the sheet 'Sheet'"

    def __init__(self, runner: AbstractRunner, dst_wb, dst_sheet_arg: SheetArg,
                 _as_token=None, sheet_alias: Optional[CstArg] = None):
        super().__init__(runner, dst_wb, dst_sheet_arg=dst_sheet_arg)
        self.allows_join = True
        self.allows_set = True
        self.allows_where = True
        self.allows_on = True
        self.allows_from = False
        self.allows_group = True
        self.allows_having = True
        self.allows_order_by = True
        self.do_not_erase = []
        self.sets: list[Clause]
        if sheet_alias:
            dst_sheet_arg.add_alias(sheet_alias.get_constant())
        # dst_sheet_arg.verify_fields(not_in_dst=True)  # useless: never a field

    def build_stage(self, first_stage: Stage) -> UpdateStage:
        assert isinstance(self.dst_sheet_arg, SheetArg), "INTERNAL: build_stage"
        self.sets: list[Clause]
        return UpdateStage(self.dst_sheet_arg, first_stage, self.sets)

    def build_select_stage(self, first_stage: Stage) -> Stage:
        return first_stage  # this stage is pass through: No need for a Select with UPDATE

    def execute(self, print_me: bool = True):
        if print_me:
            print(f"EXECUTE {self.name} '{self.dst_sheet_arg.get_sheet_name()}'")

        # build the pipeline
        # TODO: Manage inner Commands, e.g. JOIN of SELECT...
        # Hint: do it recursively rather than iterative
        self.joins: list[JoinClause]
        join: JoinClause

        reversed_fields = reversed(self.joins)
        previous_join_clause: Optional[JoinClause] = None
        second_stage: Optional[Stage] = None
        for join in reversed_fields:
            assert isinstance(join.first_arg, SheetArg), "INTERNAL: execute join.first_arg"

            if second_stage is None:
                second_stage = FromStage(join.first_arg)
            else:
                assert previous_join_clause is not None, "INTERNAL: execute previous_join_clause"
                first_stage = FromStage(join.first_arg)
                second_stage = previous_join_clause.build_stage(first_stage, second_stage)
            previous_join_clause = join

        current_stage: Stage
        if self.allows_from:  # For SELECT INTO only
            assert isinstance(self.from_arg, SheetArg), "INTERNAL: execute from_arg"
            first_stage = FromStage(self.from_arg)
        else:                 # For UPDATE Only
            assert isinstance(self.dst_sheet_arg, SheetArg),  "INTERNAL: execute dst_sheet_arg"
            first_stage = FromStage(self.dst_sheet_arg)

        if previous_join_clause:
            current_stage = previous_join_clause.build_stage(first_stage, second_stage)
        else:  # there is only one FROM
            current_stage = first_stage

        # Now, current_stage is the input

        if self.where_clause:
            assert isinstance(self.where_clause, WhereClause),  "INTERNAL: execute WhereClause"
            current_stage = self.where_clause.build_stage(current_stage)

        if self.group_clause:
            assert isinstance(self.group_clause, GroupClause),  "INTERNAL: execute GroupClause"
            current_stage = self.group_clause.build_stage(current_stage)

        current_stage = self.build_select_stage(current_stage)

        if self.having_clause:
            assert isinstance(self.having_clause, HavingClause),  "INTERNAL: execute HavingClause"
            current_stage = self.having_clause.build_stage(current_stage)

        if self.order_by_clause:
            assert isinstance(self.order_by_clause, OrderByClause),  "INTERNAL: execute OrderByClause"
            current_stage = self.order_by_clause.build_stage(current_stage)

        my_stage = self.build_stage(current_stage)
        my_stage.execute()


# SelectIntoCmd and UpdateCmd build their execution Pipeline
# assuming a statement as: (see https://www.w3schools.com/sql/sql_having.asp)
# SELECT INTO   dst0
# FROM          src1
# FIELD         field1  =   expr
# FORMAT        field2  =   example
# UID           field3  =   example
# LEFT JOIN     src2    ON  expr1 = expr2
# WHERE         expr3
# GROUP BY      expr4
# HAVING        expr5
# ORDER BY      expr6
#
# The expected pipeline is:
#   stage0      = FromStage(src1)
#   stage1      = FromStage(dst0)
#   stage2      = leftJoinStage(stage0, stage1, expr, expr) (runs also ON)
#   stage4      = WhereStage(stage2, expr)
#   stage3      = GroupStage(stage3, expr)
#   stage5      = HavingStage(stage4, expr)
#   stage6      = OrderBy(stage5, expr)
#   SelectStage(stage6, sets0)
#      sets0    = list of all Field, format, UID clauses
#
#
#
# NOTE from https://dba.stackexchange.com/questions/5038/sql-server-join-where-processing-order
# The logical processing of a query is
# 1. FROM
# 2. ON
# 3. JOIN
# 4. WHERE
# 5. GROUP BY
# 6. WITH CUBE or WITH ROLLUP
# 7. HAVING
# 8. SELECT
# 9. DISTINCT
# 10. ORDER BY
# 11. TOP

class SelectIntoCmd(UpdateCmd):
    srcWb: PyxlWorkbook
    name = 'SELECT INTO'
    help = "Updates in 'DstSheet' with data selected from SrcSheet"

    def __init__(self, runner: AbstractRunner, dst_wb: PyxlWorkbook, dst_sheet_arg: SheetArg,
                 _as_token=None, sheet_alias: Optional[CstArg] = None):
        super().__init__(runner, dst_wb, dst_sheet_arg=dst_sheet_arg, _as_token=_as_token, sheet_alias=sheet_alias)
        self.allows_from = True
        dst_sheet = dst_sheet_arg.get_sheet()

        for i in dst_sheet_arg.get_column_range():
            col_name = dst_sheet.openpyxl_sheet.cell(row=dst_sheet.first_row, column=i).value
            if col_name is None or col_name == "" or col_name == " ":
                continue
            col_name = str(col_name)
            cell = dst_sheet.openpyxl_sheet.cell(row=dst_sheet.first_row + 1, column=i)
            formula = cell.value
            if formula and str(formula)[0] == '=':
                SetClause(self, None, [], FieldArg(self, col_name),
                          CstArg(self, '='), FormulaArg(self, formula))

            if cell.has_style:
                FormatClause(self, None, [None, None, cell], FieldArg(self, col_name), None, None)

    def build_stage(self, first_stage: Stage) -> IntoStage:
        assert isinstance(self.dst_sheet_arg, SheetArg), "INTERNAL: build_stage"
        self.sets: list[Clause]
        return IntoStage(self.dst_sheet_arg, first_stage, self.sets)

    def build_select_stage(self, first_stage: Stage) -> Stage:
        assert isinstance(self.dst_sheet_arg, SheetArg), "INTERNAL: build_select_stage"
        self.sets: list[Clause]
        return SelectStage(self.dst_sheet_arg, first_stage, self.sets)

    def execute(self, print_me: bool = True):
        self.dst_sheet_arg: SheetArg
        print(f"EXECUTE {self.name} '{self.dst_sheet_arg.get_sheet_name()}' ")  # FROM '{self.src_sheet.title}'")

        # In Row = 2 ONLY
        # Erase all cells that are not in do_not_erase
        my_dict = self.dst_sheet_arg.named_sheet.column_names
        for column in my_dict:
            if column not in self.do_not_erase:
                self.dst_sheet_arg.named_sheet.set_value(2, column, None)

        super().execute(print_me=False)


# -----------------------------------------------------------------------------------------------------------------
# Cmd that do not need a pipeline
# -----------------------------------------------------------------------------------------------------------------

# Example: PIVOT	Customers	FROM	Operators
class PivotCmd(Cmd):
    name = "PIVOT"
    help = "creates a mini Pivot table in sheet"

    def __init__(self, runner: AbstractRunner, dst_wb, dst_sheet_arg: SheetArg, _from_kwd, src_arg):
        super().__init__(runner, dst_wb, dst_sheet_arg=dst_sheet_arg)
        self.src_sheet_arg = src_arg
        self.pivot = None
        # dst_sheet_arg.verify_fields(not_in_src=True)  # useless: never a field
        # src_arg.verify_fields(not_in_dst=True)  # useless: never a field

    def execute(self):
        print(f"EXECUTE PIVOT '{self.dst_sheet_arg.get_sheet_name()}' FROM '{self.src_sheet_arg.get_sheet_name()}'")
        assert self.dst_sheet_arg is not None, "INTERNAL: PivotCmd::execute "
        dst_sheet = self.dst_sheet_arg.get_sheet()
        src_sheet = self.src_sheet_arg.get_sheet()
        colors_column = dst_sheet.columns[2]
        dst_sheet.column_styles[colors_column]=None # otherwise, the color of the 1st rox is copied due to automatic style

        self.pivot = Pivot(dst_sheet,src_sheet , use_formula=True)



# Example: SAVE OpenTV.xlsx
class SaveCmd(Cmd):
    name = 'SAVE'
    help = "Saves the workbook in 'Filename'"

    def __init__(self, runner: AbstractRunner, dst_wb, filename: CstArg, _from_kw=None, workbook=None):
        super().__init__(runner, dst_wb)
        self.filename = filename.get_constant()
        self.workbook = dst_wb.get_workbook(workbook.get_constant()) if workbook else dst_wb
        # filename.verify_fields(not_in_src=True)  # useless: never a field

    def execute(self):

        for sheet in self.workbook.sheets_to_delete:
            print(f"EXECUTE DELETE {sheet}")
            self.dst_wb.delete_sheet(sheet)
        self.workbook.sheets_to_delete = []

        print(f"EXECUTE {self.name} {self.filename}")
        self.workbook.save(self.filename)


class ExportCmd(Cmd):
    name = 'EXPORT HTML'
    help = "Saves the workbook as an HTML file in 'Filename'"

    def __init__(self, runner: AbstractRunner, dst_wb, filename: CstArg, _from_kw=None, workbook=None):
        super().__init__(runner, dst_wb)
        self.filename = filename.get_constant()
        self.workbook = dst_wb.get_workbook(workbook.get_constant()) if workbook else dst_wb
        # filename.verify_fields(not_in_src=True)  # useless: never a field

    def execute(self):

        print(f"EXECUTE {self.name} {self.filename}")
        self.workbook.export_html(self.filename)

# Example: DELETE Micro-SQL
class DeleteCmd(Cmd):
    name = 'DELETE SHEET'
    help = "Deletes the sheet 'Sheet'"

    def __init__(self, runner: AbstractRunner, dst_wb, sheet_name: CstArg):
        super().__init__(runner, dst_wb)
        self.sheet_name = sheet_name.get_constant()
        # sheet_name.verify_fields(not_in_src=True)  # useless: never a field

    def execute(self):
        self.dst_wb.sheets_to_delete.append(self.sheet_name)


class ImportCmd(Cmd):
    """
    Class used to import modules for the evaluation of Python expression by 'EXPRESSION'
    The expression may refer to non-imported code

    IMPORT module               : 'import module'
    IMPORT module SUBS a, b, c  : 'from module import a b c'
    IMPORT module SUBS *        : 'from module import *'
    """
    name = 'IMPORT'
    help = "Imports python 'Module' (SUBS submodules|)"

    def __init__(self, runner: AbstractRunner, dst_wb, module: Arg, _subs_kwd=None, sub_modules=None):
        """
        Dynamically imports a module
        """
        # See https://docs.python.org/3/tutorial/modules.html
        # if a package’s __init__.py code defines a list named __all__,
        # it is taken to be the list of module names that should be imported
        # when "from package import * " is encountered

        super().__init__(runner, dst_wb)
        self.module = module.get_constant()
        self.sub_modules = sub_modules.get_constant() if sub_modules is not None else None
        # sheet_name.verify_fields(not_in_src=True)  # useless: never a field

    def execute(self):
        if self.sub_modules is None:
            print(f"EXECUTE {self.name} {self.module}")
        else:
            print(f"EXECUTE {self.name} {self.module} SUBS {self.sub_modules}")

        self.dst_wb.import_module(self.module, self.sub_modules)

class RenameCmd(Cmd):
    """
    Class used to rename a sheet to a new name
    RENAME sheet AS new_name
    no SQL equivalent
    """
    name = 'RENAME SHEET'
    help = "Renames excel 'Sheet' AS 'new_name'"
    def __init__(self, runner: AbstractRunner, dst_wb, sheet: SheetArg, _as_kwd, new_name: CstArg):
        """
        rename a sheet
        """
        super().__init__(runner, dst_wb)
        self.sheet_name = sheet.get_sheet_name()
        self.new_name = new_name.get_constant()

    def execute(self):
        print(f"EXECUTE {self.name} {self.sheet_name} AS {self.new_name}")
        self.dst_wb.rename_sheet(self.sheet_name, self.new_name)

class LoadCmd(Cmd):
    """
    Class used to Load a new Excel file and execute PyxlSQL commands in it
    LOAD  filename
    no SQL equivalent
    """
    name = 'LOAD'
    help = "Load a new Excel file and execute PyxlSQL commands in it "
    def __init__(self, runner: AbstractRunner, dst_wb, filename: CstArg):
        """
        LOAD  filename
        """
        super().__init__(runner, dst_wb)
        self.filename = filename.get_constant()

    def execute(self):
        print(f"EXECUTE {self.name} {self.filename}")

        runner = self.runner
        cmdline = runner.build(["-f", "tests/" + self.filename])
        cmdline.run_first()


class DatabaseCmd(Cmd):
    """
    Class used to load data from an Excel sheet by specifying non default start and end
    "DATABASE" src_sheet "START" cell "END" cell
    """
    name = 'DATABASE'
    help = "load data from an Excel sheet by specifying non default start and end"

    def __init__(self, runner: AbstractRunner, dst_wb,
                 sheet: SheetArg, _start_kwd, start: CstArg, _end_kwd, end: CstArg):
        """
        "DATABASE" src_sheet "START" cell "END" cell
        """
        super().__init__(runner, dst_wb)
        self.sheet = sheet
        self.sheet_name = sheet.get_sheet_name()
        self.first_column = self.parse_column(start.get_constant())
        self.last_column = self.parse_column(end.get_constant())+1
        self.first_row = self.parse_row(start.get_constant())
        self.last_row = self.parse_row(end.get_constant())

    @staticmethod
    def parse_row(descriptor:str):
        # descriptor example : A1
        m = re.match(r"([A-Z]+)(\d+)", descriptor)
        if m:
            return int(m.group(2))
        raise PyxlSqlParseError(f"Illegal cell row '{descriptor}'", "DATABASE")

    @staticmethod
    def parse_column(descriptor: str):
        # descriptor example : A1
        m = re.match(r"([A-Z])?([A-Z])(\d+)", descriptor)
        if m:
            col0 = (m.group(1))
            col = 0 if col0 is None else (ord(col0[0]) - ord('A')+1)*(ord('Z')-ord('A')+1)
            col1 = (m.group(2))
            col += (ord(col1[0]) - ord('A')+1)
            return col

        raise PyxlSqlParseError(f"Illegal cell column '{descriptor}'", "DATABASE")

    @staticmethod
    def column_letters(number: int):
        c0 = number % 26
        r1 = int((number - c0)/26)
        c1 = r1 % 26
        r2 = int((r1 - c1)/26)
        c2 = r2 %26
        r3 = int((r2 - c2) / 26)
        c3 = r3 % 26
        v = chr(ord('A')+c0)
        if c1:
            v += chr(ord('A') + c2)
        if c2:
            v += chr(ord('A') + c2)
        if c3:
            v += chr(ord('A') + c3)
        return v

    def execute(self):
        c1 = self.column_letters(self.first_column)
        c2 = self.column_letters(self.last_column-1)
        print(f"EXECUTE {self.name} {self.sheet_name} START {c1}{self.first_row} END {c2}{self.last_row}")
        sheet = self.dst_wb.get_sheet(self.sheet_name, raise_exception=True,
                              first_row = self.first_row, last_row = self.last_row,
                              first_column = self.first_column, last_column = self.last_column)
        sheet.read_data(first_row = self.first_row, last_row = self.last_row,
                              first_column = self.first_column, last_column = self.last_column)

# --------------------------------------------------
# Clause
# --------------------------------------------------


class CommentsClause(Clause):
    name = "COMMENTS"
    help = "Comments"

    def __init__(self, command=None, _clause=None, _cells=None, field=None):
        super().__init__(command, first_arg=field)

    # does not define execute_clause()


class SetClause(Clause):
    name = "SET"
    help = "Updates the given field, maybe with condition"

    # Executes within an UPDATE, SELECT INTO or SELECT context

    def __init__(self, command, _clause, _cells, dst_arg: Arg, is_kwd, src_arg: Arg,
                 cond_kwd=None, third_arg=None):
        super().__init__(command, first_arg=dst_arg, second_arg=src_arg, third_arg=third_arg)
        self.when_expr = None
        self.aggregate_expr = None

        assert isinstance(is_kwd, CstArg), "INTERNAL, SetClause CstArg"
        if is_kwd.get_constant() == "AGGREGATES":
            assert isinstance(cond_kwd, CstArg), "INTERNAL, SetClause cond_kwd"
            assert cond_kwd.get_constant() == "WITH", "INTERNAL, SetClause get_constant"
            self.aggregate_expr = third_arg
        elif is_kwd.get_constant() == "COUNT":
            self.aggregate_expr = AggregateExprArg(self.command, "$= len(#$)")
        elif is_kwd.get_constant() == "AVERAGE":
            self.aggregate_expr = AggregateExprArg(self.command, "$= sum(#$)/len(#$) if len(#$) else 0")
        elif is_kwd.get_constant() == "MIN":
            self.aggregate_expr = AggregateExprArg(self.command, "$= functools.reduce(min, #$)")  # noqa
        elif is_kwd.get_constant() == "MAX":
            self.aggregate_expr = AggregateExprArg(self.command, "$= functools.reduce(max, #$)")  # noqa
        elif is_kwd.get_constant() == "SUM":
            self.aggregate_expr = AggregateExprArg(self.command, "$= sum(#$)")  # noqa

        # TODO: Add the other keywords

        elif is_kwd.get_constant() == '=':
            if cond_kwd is not None:
                assert isinstance(cond_kwd, CstArg), "INTERNAL, SetClause cond_kwd is None"
                assert cond_kwd.get_constant() == "WHEN", "INTERNAL, SetClause When"
                self.when_expr = third_arg
        else:
            raise PyxlSqlParseError("Illegal aggregate function", is_kwd.get_constant())

        dst_arg.verify_fields(not_in_src=True)
        self.dst_field, _ = dst_arg.find_name_and_sheet(not_in_src=True)
        src_arg.verify_fields()
        self.src_field, self.src_sheet = src_arg.find_name_and_sheet()
        # third_arg.verify_fields()  # NEVER, because this is NOT an expression
        command.add_set(self)

    def eval_clause(self, inputs: AbstractResult, outputs: AbstractResult):
        if self.when_expr is not None:
            condition = self.when_expr.evaluate(inputs, outputs)
            if not condition:
                return

        results_list = inputs.evaluate_expr(self.second_arg, outputs)
        if not isinstance(inputs, GroupResult):
            assert len(results_list) == 1 , "INTERNAL, eval_clause len"
            new_value = results_list[0]
            # if isinstance(inputs, GroupResult):
            #     inputs = inputs.outputs[0]
        else:
            assert isinstance(inputs, GroupResult), "INTERNAL, eval_clause GroupResult"
            if self.aggregate_expr is None:
                #  all results are supposed to be identical
                if not all(item == results_list[0] for item in results_list):
                    raise PyxlSqlExecutionError("SET without an aggregate expression, but results not identical",
                                                self.first_arg.get_constant())
                new_value = results_list[0]
            else:
                assert isinstance(self.aggregate_expr, AggregateExprArg), "INTERNAL, eval_clause AggregateExprArg"
                new_value = self.aggregate_expr.eval_reduce(results_list)
            inputs = inputs.outputs[0]
        if not isinstance(inputs, EnvResult):
            raise PyxlSqlInternalError("inputs is not an EnvResult")

        assert isinstance(self.first_arg, FieldArg), "INTERNAL, eval_clause FieldArg"
        assert isinstance(outputs, ValueResult), "INTERNAL, eval_clause ValueResult"

        if isinstance(new_value, str) and len(new_value) > 0 and new_value[0] == '=':
            # EVAL 2nd arg is a Formula ! will be set in the INTO pass
            outputs.set_excel_formula(self.first_arg, new_value)
        else:
            outputs.set_value(self.first_arg, new_value)

    def execute_clause(self, inputs: AbstractResult, dst_row: int):
        if dst_row == -1:
            return
        dst_sheet = self.command.dst_sheet_arg.get_sheet()
        inputs.execute_set(self.first_arg, dst_sheet, self.dst_field, dst_row)


class FormatClause(Clause):
    name = "FORMAT"
    help = """a format specification for the field, specified with an example."""

    def __init__(self,command: Cmd, _clause, cells, field, _is_kwd, _example):
        # _example is the value, which we don't care, only its format is useful
        super().__init__(command, _cells=cells, first_arg=field)

        self.number_format = cells[2].number_format
        self.style = cells[2].style
        self.fill = copy(cells[2].fill)
        self.font = copy(cells[2].font)

        field.verify_fields(not_in_src=True)
        self.dst_field, _ = field.find_name_and_sheet(not_in_src=True)

        command.add_set(self)

    def eval_clause(self, inputs: AbstractResult, outputs: AbstractResult):
        pass

    def execute_clause(self, inputs: AbstractResult, dst_row: int):
        if dst_row == -1:
            return
        cell = self.command.dst_sheet_arg.get_sheet().get_cell(dst_row, self.first_arg.get_constant())
        cell.style = self.style
        cell.number_format = self.number_format
        cell.font = self.font
        cell.fill = self.fill


# UID_clause     := "UNIQUE ID" dst_field "=" example
# 'example' is a string containing '@', which wil be replaced by a unique number
class UidClause(Clause):
    name = "UID"
    help = "Generates an UID for the given field, starting from an example"

    def __init__(self,command: Cmd, _clause, _cells, dst_arg: Arg, _is_kwd, src_arg: Arg):
        super().__init__(command, first_arg=dst_arg, second_arg=src_arg)
        self.count = 0

        dst_arg.verify_fields(not_in_src=True)
        self.dst_field, _ = dst_arg.find_name_and_sheet(not_in_src=True)
        src_arg.verify_fields(not_in_dst=True)
        command.add_set(self)

    def eval_clause(self, inputs: AbstractResult, outputs: AbstractResult):
        new_value = re.sub('@', str(self.count), self.second_arg.get_constant())
        # TODO: eval on the first_arg, so that we can choose the number of digits of @, with format !
        self.count += 1
        assert isinstance(self.first_arg, FieldArg), "INTERNAL, eval_clause first_arg"
        assert isinstance(outputs, ValueResult),  "INTERNAL, eval_clause ValueResult"
        outputs.set_value(self.first_arg, new_value)

    def execute_clause(self, inputs: AbstractResult, dst_row: int):
        dst_sheet = self.command.dst_sheet_arg.get_sheet()
        assert isinstance(inputs, ValueResult), "INTERNAL, execute_clause inputs"
        new_value = inputs.get_field_value(self.first_arg)
        dst_sheet.set_value(dst_row, self.first_arg.get_constant(), new_value)


# From_clause    := "FROM" src_sheet
class FromClause(Clause):
    name = "FROM"
    help = "Specifies the source for select"

    def __init__(self, command: Cmd, _clause, _cells, src_sheet: SheetArg,
                 _as_token=None, sheet_alias: Optional[CstArg] = None):
        super().__init__(command)  # unused
        # src_sheet.verify_fields(not_in_src=True)  # NO: it is a sheet
        command.add_from(src_sheet)
        if sheet_alias:
            src_sheet.add_alias(sheet_alias.get_constant())

    # does not define execute_clause()


# Join_clause    := Join_key src_sheet "ON" first_expr(1) "=" second_expr(2)
class JoinClause(Clause):
    name = "FULL JOIN"
    help = """JOIN clause
           """

    def __init__(self, command: Cmd, _clause, _cells, src_arg_sheet,
                 _as_token=None, sheet_alias: Optional[CstArg] = None):
        super().__init__(command, first_arg=src_arg_sheet)
        command.add_join(self)
        self.first_arg: SheetArg
        if sheet_alias:
            src_arg_sheet.add_alias(sheet_alias.get_constant())
        # src_arg_sheet.verify_fields(not_in_src=True)  # NO: only sheets

    def add_on(self, second_arg, third_arg):
        self.second_arg = second_arg
        self.third_arg = third_arg

    def build_stage(self, first_stage: Stage, second_stage: Stage):
        assert isinstance(self.second_arg, ExprArg) or isinstance(self.second_arg, FieldArg), "INTERNAL, build_stage"
        assert isinstance(self.third_arg, ExprArg) or isinstance(self.second_arg, FieldArg), "INTERNAL, build_stage"
        return FullJoinStage(first_stage, second_stage, self.second_arg, self.third_arg)


class InnerJoinClause(JoinClause):
    name = "INNER JOIN"

    def __init__(self,  command: Cmd, clause, cells, src_arg_sheet,
                 _as_token=None, sheet_alias: Optional[CstArg] = None):
        super().__init__(command, clause, cells, src_arg_sheet, _as_token, sheet_alias)

    def build_stage(self, first_stage: Stage, second_stage: Stage):
        assert isinstance(self.second_arg, ExprArg) or isinstance(self.second_arg, FieldArg), "INTERNAL, build_stage"
        assert isinstance(self.third_arg, ExprArg) or isinstance(self.second_arg, FieldArg), "INTERNAL, build_stage"
        return InnerJoinStage(first_stage, second_stage, self.second_arg, self.third_arg)


class LeftJoinClause(JoinClause):
    name = "LEFT JOIN"

    def __init__(self, command: Cmd, clause, cells, src_arg_sheet,
                 _as_token=None, sheet_alias: Optional[CstArg] = None):
        super().__init__(command, clause, cells, src_arg_sheet, _as_token, sheet_alias)

    def build_stage(self, first_stage: Stage, second_stage: Stage):
        assert isinstance(self.second_arg, ExprArg) or isinstance(self.second_arg, FieldArg), "INTERNAL, build_stage"
        assert isinstance(self.third_arg, ExprArg) or isinstance(self.second_arg, FieldArg), "INTERNAL, build_stage"
        return LeftJoinStage(first_stage, second_stage, self.second_arg, self.third_arg)


class RightJoinClause(JoinClause):
    name = "RIGHT JOIN"
    help = """JOIN clause
           """

    def __init__(self, command: Cmd, clause, cells, src_arg_sheet,
                 _as_token=None, sheet_alias: Optional[CstArg] = None):
        super().__init__(command, clause, cells, src_arg_sheet, _as_token, sheet_alias)

    def build_stage(self, first_stage: Stage, second_stage: Stage):
        assert isinstance(self.second_arg, ExprArg) or isinstance(self.second_arg, FieldArg), "INTERNAL, build_stage"
        assert isinstance(self.third_arg, ExprArg) or isinstance(self.second_arg, FieldArg), "INTERNAL, build_stage"
        return RightJoinStage(first_stage, second_stage, self.second_arg, self.third_arg)


# On_clause := "ON" first_expr(1) "=" second_expr(2)
class OnClause(Clause):
    name = "ON"
    help = """ON clause
           """

    def __init__(self, command: Cmd, clause, _cells, on_left_expr, _equals_kwd, on_right_expr):
        super().__init__(command)
        on_left_expr.verify_fields(not_in_dst=True)
        on_right_expr.verify_fields(not_in_dst=True)
        clause.add_on(on_left_expr, on_right_expr)


# Where_clause   := "WHERE" expr
class WhereClause(Clause):
    name = "WHERE"
    help = """only lines that satisfy the 'WHERE' clause are updated/copied
       Syntax: WHERE src_expr
       the clause is evaluated in the source environment"""

    def __init__(self, command: Cmd, _clause, _cells, first_expr):
        super().__init__(command, first_arg=first_expr)
        first_expr.verify_fields(not_in_dst=True)
        command.add_where(self)

    def build_stage(self, input_stage: Stage):
        assert isinstance(self.first_arg, ExprArg), "INTERNAL, build_stage"
        return WhereStage(input_stage, self.first_arg)

    # does not define execute_clause()


# Group_clause   := "GROUP BY" dst_expr *
class GroupClause(Clause):
    name = "GROUP BY"
    help = """Regroups lines with the same field"""

    def __init__(self, command: Cmd, _clause, _cells, first_expr: Arg):
        super().__init__(command, first_arg=first_expr)
        first_expr.verify_fields(not_in_dst=True)
        command.add_group(self)

    def build_stage(self, input_stage: Stage):
        assert isinstance(self.first_arg, FieldArg) or isinstance(self.first_arg, ExprArg), "INTERNAL, build_stage"
        return GroupByStage(input_stage, self.first_arg)


# Having_clause  := "HAVING" expr
class HavingClause(Clause):
    name = "HAVING"
    help = """test to filter out some groups"""

    def __init__(self, command: Cmd, _clause, _cells, first_expr: Arg):
        super().__init__(command, first_arg=first_expr)
        first_expr.verify_fields(not_in_src=True)
        command.add_having(self)

    def build_stage(self, input_stage: Stage):
        assert isinstance(self.first_arg, ExprArg), "INTERNAL, build_stage"
        return HavingStage(input_stage, self.first_arg)


# Order_by_clause  := "ORDER BY" expr
class OrderByClause(Clause):
    name = "ORDER BY"
    help = """Order output"""

    def __init__(self, command: Cmd, _clause, _cells, first_expr: Arg):
        super().__init__(command, first_arg=first_expr)
        first_expr.verify_fields(not_in_src=True)
        command.add_order_by(self)

    def build_stage(self, input_stage: Stage):
        assert isinstance(self.first_arg, FieldArg) or isinstance(self.first_arg, ExprArg), "INTERNAL, build_stage"
        return OrderByStage(input_stage, self.first_arg)
