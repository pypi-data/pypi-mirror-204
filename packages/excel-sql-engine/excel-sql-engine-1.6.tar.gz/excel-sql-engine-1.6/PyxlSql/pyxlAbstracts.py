# ---------------------------------------------------------------------------------------------------------------
# PyxlSQL project
# This program and library is licenced under the European Union Public Licence v1.2 (see LICENCE)
# developed by fabien.battini@gmail.com
# ---------------------------------------------------------------------------------------------------------------

from typing import Optional
from PyxlSql.pyxlErrors import PyxlSqlError, PyxlSqlInternalError
from PyxlSql.pyxlSheets import PyxlSheet


class AbstractRunner:
    def __init__(self, arguments=None):
        self.arguments = arguments

    def run_first(self):
        raise PyxlSqlInternalError(f"AbstractRunner.run_first() on {self.name}")

    def build(self, arguments=None):
        raise PyxlSqlInternalError(f"AbstractRunner.build() on {self.name}")

# ---------------------------------------------------------------------------------------------------------------
# Forward declaration of Statement, because used in the Parser code
# ---------------------------------------------------------------------------------------------------------------


class AbstractStatement:
    """
    The instance of each line of the PyxlSql program
    with the actual arguments
    can be a Command, a Clause or None
    """
    name = "Statement"
    help = "Empty Help string"
    descriptor = []

    def __init__(self):
        self.current_line = PyxlSqlError.current_line
        # Under NORMAL conditions, a statement is created through the parser,
        # and the parser should have initiated the current_line
        # so, we just have to remember that stage
    def is_a_command(self):
        return False

    def execute(self):
        raise PyxlSqlInternalError("Execute an illegal Statement, i.e. Cmd or Clause")

    def build_sheet_number(self):
        raise PyxlSqlInternalError("Illegal build_sheet_number")


# ---------------------------------------------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------------------------------------------

class Index:
    def __init__(self, row: int, sheet_arg):
        self.row = row
        self.sheet_arg = sheet_arg
        self.signature = f"{sheet_arg.get_sheet_name()}({row}), "


class AbstractResult:
    """Holds the results of evaluations, select..."""
    def __init__(self):
        self.signature = "Result"

    def __iter__(self):
        raise PyxlSqlInternalError("Illegal Result.__iter__()")

    def __next__(self):
        raise PyxlSqlInternalError("Illegal Result.__next__()")

    def get_row(self, sheet):
        raise PyxlSqlInternalError("Illegal Result.get_row()")

    def get_first_row(self):
        raise PyxlSqlInternalError("Illegal Result.get_first_row()")

    def evaluate_expr(self, _expr, _outputs):
        raise PyxlSqlInternalError("Illegal Result.evaluate_expr()")

    def get_index_list(self):
        raise PyxlSqlInternalError("Illegal Result.get_index_list()")

    def get_all_env(self) -> list:  # list[Result]
        raise PyxlSqlInternalError("Illegal Result.get_all_env()")

    def get_field_value(self, field_arg):
        raise PyxlSqlInternalError("Illegal Result.get_field_value()")

    def execute_set(self, field_arg, dst_sheet, field_name, dst_row: int):
        raise PyxlSqlInternalError("Illegal Result.execute_set()")

    def __add__(self, other):
        raise PyxlSqlInternalError("Illegal Result.__add__()")

    def set_all_values(self, alias_table, eval_values):
        raise PyxlSqlInternalError("Illegal Result.set_all_values()")

# ---------------------------------------------------------------------------------------------------------------
# Arg
# ---------------------------------------------------------------------------------------------------------------


class Arg(AbstractStatement):
    name = "Generic ARG"
    """A Statement that describes an actual argument"""

    def __init__(self, command, specification: str):
        """
        :param command: Cmd : self is an argument to a clause inside this command
        :param specification: str : the initial specification of the argument as found in the Excel file (or similar)
        """
        super().__init__()
        self.command = command
        self.dst_sheet_arg: Optional[PyxlSheet]  # TODO: Remove this, which is confusing
        if command is None:  # MUST use this syntax to have correct type inference
            self.dst_sheet_arg = None
        else:
            self.dst_sheet_arg = command.dst_sheet_arg

        self.specification = specification

    def evaluate(self, _inputs: AbstractResult, _outputs: AbstractResult):
        raise PyxlSqlInternalError(f"Arg.evaluate() on {self.name}")

    def get_constant(self):
        raise PyxlSqlInternalError(f"Arg.get_constant() on {self.name}")

    def find_name_and_sheet(self, not_in_src=False):
        raise PyxlSqlInternalError(f"Arg.find_name_and_sheet() on {self.name}")

    def set_sheet_number(self, nb: int):
        raise PyxlSqlInternalError(f"Arg.set_sheet_number() on {self.name}")

    def get_sheet_name(self) -> str:
        raise PyxlSqlInternalError(f"Arg.get_sheet_name() on {self.name}")

    def get_sheet(self) -> PyxlSheet:
        raise PyxlSqlInternalError(f"Arg.get_sheet() on {self.name}")

    def verify_fields(self, not_in_src=False, not_in_dst=False):
        raise PyxlSqlInternalError(f"Arg.verify_fields() on {self.name}")


# ---------------------------------------------------------------------------------------------------------------
# Clause
# ---------------------------------------------------------------------------------------------------------------

class Clause(AbstractStatement):
    name = "ERROR"

    def __init__(self, command, _clause=None, _cells=None,
                 first_arg: Optional[Arg] = None,
                 second_arg: Optional[Arg] = None,
                 third_arg: Optional[Arg] = None):
        super().__init__()
        self.command = command
        self.first_arg: Optional[Arg] = first_arg
        self.second_arg: Optional[Arg] = second_arg
        self.third_arg: Optional[Arg] = third_arg

    # A Clause that can be used in a SelectCmd MUST return True is a value was inserted

    def eval_clause(self, inputs: AbstractResult, outputs: AbstractResult):
        """eval_clause is called ONCE, it prepares data common to all execute_clause calls"""
        raise PyxlSqlInternalError(f"{self.name}.eval_clause()")

    def execute_clause(self, inputs: AbstractResult, row_nb: int):
        """execute_clause is called for each row.
        It computes the output of the clause and writes the result
        """
        raise PyxlSqlInternalError(f"{self.name}.execute_clause()")

    def set_current_line(self):
        raise PyxlSqlInternalError(f"{self.name}.set_current_line()")

    def add_when(self, when_clause):
        raise PyxlSqlInternalError("WHEN on a non FIELD clause")
