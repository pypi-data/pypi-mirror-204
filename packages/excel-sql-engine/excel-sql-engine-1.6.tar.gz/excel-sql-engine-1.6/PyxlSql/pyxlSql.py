# ---------------------------------------------------------------------------------------------------------------
# PyxlSQL project
# This program and library is licenced under the European Union Public Licence v1.2 (see LICENCE)
# developed by fabien.battini@gmail.com
# ---------------------------------------------------------------------------------------------------------------


import argparse
import os
import re
from typing import Optional
from PyxlSql.pyxlErrors import PyxlSqlError
from PyxlSql.pyxlSheets import PyxlSheet
from PyxlSql.pyxlWorkbook  import   PyxlWorkbook
from PyxlSql.pyxlEngine import AbstractStatement
from PyxlSql.pyxlGrammar import Parser
from PyxlSql.pyxlAbstracts import AbstractRunner

# how to get openpyxl, pytest etc.,
# shell>python -m pip install --upgrade openpyxl pytest setuptools wheel tox pytest-flakes pytest-cov sphinx gitpython

# how to test: (cf tox.ini, which does everything)
# (venv) PyxlSQL> pyxlSql -f tests/Test_pyxlsql.xlsx  #noqa
# (venv) PyxlSQL> pytest --cache-clear --ff
# (venv) PyxlSQL> pytest --flakes
# (venv) PyxlSQL> pytest --cov --cov-report html --cov-report term
# (venv) PyxlSQL> sphinx-build source build/html -W -b html
# or:
# (venv) PyxlSQL> tox



# ----------------------- General behavior
# REQ 0001: PyxlSQL uses openPyxl to read excel files
# REQ 0002: PyxlSQL statements are stored 'Pyxl SQL' sheet
# REQ 0003: Sheet are described as 'sheet name' or 'filename.xlsx[sheet name]'
# REQ 0004: remove start/trailing spaces for Command, Clause, field names, it is a common error, hard to find
# REQ 0005: Import functools automatically, otherwise MIN/MAX do not work
# REQ 0006: Requirements and FIX ME should be extracted automatically from the source code and published in doc
# Req 0007: Use API token to upload on Pypi. see  https://pyptoxi.org/help/#apitoken and https://pypi.org/manage/account/token/
# REQ 0008: Generate to do.rst through tox, using parse_requirements.py
# REQ 0009: publish also htmlcov on gitlab.io
# REQ 0010: create a downloadable executable for windows user : python -m pip install PyInstaller #
# TODO: REQ 0011: create a doc specific to windows user that do not know python
# REQ 0012: manage also .ods files from LibreOffice: NO, this is NOT possible, OpenPyxl does NOT read .ods format
# REQ 0013: LAZY reading of sheets: only sheets that are referred by the SQL commands are read.

# TODO: 100% coverage: most of not covered lines are defensive code which is unreachable by design
# TODO: Update current documentation xxx.rst because @ is often replaced by # in examples, due to more strict typing


# ----------------------- Cmdline arguments
# REQ 1001: --dir/-d directory: processes all Excel files in the directory
# REQ 1002: --file/-f file (multiple times): process this file
# REQ 1003: --filepath/-p dir (multiple times): adds directory to path for included Excel files
# REQ 1004: the directory of the file being processed is added in the filepath
# TODO: REQ 1005: --data-only: reads excel file with the data-only flag

# ----------------------- Commands

# REQ 2001: Select_cmd     := "SELECT INTO"  dst_sheet: string  ("AS" Alias)
#             SELECT INTO adds a FORMULA and a FORMAT clause if the 1st data line is filled with examples-2,
#             then erases this line
# REQ 2002: Update_cmd     := "UPDATE" dst_sheet: string
# REQ 2003: Import_cmd     := "IMPORT" module ("SUBS" sub_modules)
#           Behavior: allows to use more features in the EXPRESSION clauses by importing python libs
# REQ 2004: Delete_cmd     := "DELETE" dst_sheet
#           Behavior : remove a sheet, e.g. the Micro SQL sheet
# REQ 2005: Save_cmd       := "SAVE" filename ("FROM" Workbook)
#           Behavior: file saved is writen with the same directory than the original file
#           If workbook is specified, then this workbook is saved (which has little use)
# REQ 2006: Rename_cmd      := "RENAME" dst_sheet "AS" new_name
# REQ 2007: SELECT

# HOW TO do a multiple stages approach
# ------------------------------------
#    For instance, to save intermediate stages, or to cut processing into several sheets
#    Rationale:
#       OpenPyxlSQL will execute the ONLY first sheet in "Pyxl SQL", "Pyxl SQL 1" ... "Pyxl SQL 9"
#       So: remove the executed stage, save the file and reload it
#    Example
#       DELETE "Pyxl SQL"
#       SAVE "initial_file_stage_2"
#       LOAD "initial_file_stage_2"

# REQ 2008: Load_cmd       := "LOAD" filename              #  loads file, and executes it.
# TODO: REQ 2009: Insert_cmd     := "INSERT" dst_sheet "AS" new_name

# REQ 2010: Pivot_cmd      := "PIVOT" dst_field "FROM" src_sheet
# TODO: REQ 2011: Load_data_cmd  := "LOAD DATA" filename  # loads a file, with data_only set to True
# REQ 2012: Database_cmd   := src_sheet "START" cell "END" cell # changes the default area for a sheet
# REQ 2013: Export_cmd     := "EXPORT HTML" filename "FROM" workbook #  builds a .html from the workbook, with formats
# TODO: REQ 2014: "EXPORT HTML" should also generate a GIF for the PIVOT

# ----------------------- Clauses
# REQ 3000: Set_clause     := "SET" dst_field ( "=" src_expr(1,2)
# REQ 3001:                                                        ["WHEN" src_expr(1,2)]  |
#           Set_clause executed only if src_expr evaluates to true (in Python sense)
# REQ 3002:                                         "AGGREGATES" expr() "WITH" red_expr   |
# REQ 3003:                                         Aggregation_key expr()                )

# REQ 3004: UID_clause     := "UID" dst_field "=" example
# REQ 3005: Format_clause  := "FORMAT" dst_field "=" example [WHEN expr]
# REQ 3006: From_clause    := "FROM" src_sheet ["AS" alias]
# REQ 3007: Join_clause    := "LEFT JOIN" src_sheet ["AS" alias]
# REQ 3008: Join_clause    := "RIGHT JOIN" src_sheet ["AS" alias]
# REQ 3009: Join_clause    := "INNER JOIN" src_sheet ["AS" alias]
# REQ 3010: Join_clause    := "FULL JOIN" src_sheet ["AS" alias]

# REQ 3011: on_clause      := "ON" first_expr(1) "=" second_expr(2)
# REQ 3012: Where_clause   := "WHERE" expr(0,1,2)
#           if expression evaluates to True, the command is executed
# REQ 3013: Group_clause   := "GROUP BY" expr(1,2)
# REQ 3014: Order_clause   := "ORDER BY" expr(0)
# REQ 3015: Having_clause  := "HAVING" expr(0)
# REQ 3016: Comment_clause := "COMMENT" Any *


# TODO: REQ 3017: Clause "COLUMN" dst_field
#           a Clause for "INSERT", specifying a new column for the newly created table
# TODO: REQ 3018: ORDER BY @best{Mean} should sort numerically when ORDER BY #best{Mean} should sort with string compare
# TODO: REQ 3100: Several Select can be pipelined.

# REQ 3500: Fields can be named as
#       'field name'
#       '(@|#)N{field name}', with N a sheet number, 0=destination, 1,2etc = sources
#       '(@|#)alias{field name}, with alias an alisa declared in the 'AS' statement
#        # means: a number. in this case, the value will be (float)value
#        @ or nothing means : a string
# It is preferable to 'type' the variables, because the conventions for 'empty cell'
#    for Excel: empty is 0 or ""
#    for python, empty is None, and None cannot be part of expressions with strings or numbers
#  If there is an ambiguity in the filed name, then an error is raised

# ----------------------- Error generation
# REQ 4001: Trap read-only output files
# TODO: REQ 4010: Add an error "clause without command", and a test for it
# TODO: REQ 4011: test if clause is accepted by Cmd, and generate an error otherwise

# TODO: REQ 4012: Validate all Sheets, and Fields before Exec
#                  Do the verifications in 1st pass, executions in 2nd pass
# TODO: REQ 4013: Trap execution errors in Exec()


# ----------------------- Testing
# cf https://openpyxl.readthedocs.io/en/stable/development.html#coding-style
# REQ 5001 : run tests using pytest
# REQ 5002 : use tox to tests code for different submissions
# REQ 5003 : Use pytest as the tests runner with pytest-cov for coverage information
# REQ 5004 : Use pytest-flakes for static code analysis.
# TODO: REQ 5006 : use the python pympler package to profile the memory usage

# TODO: REQ 5007 : test case for PyxlSqlSheetError
# TODO: REQ 5008 : test case for PyxlSqlCellError
# TODO: REQ 5009 : test case for PyxlSqlExecutionError
# TODO: REQ 5010 : test case for "too much errors"

# TODO: REQ 5011 : Test case for EXPRESSION with a reference to a formula in a cell
# REQ 5012 : test case for RIGHT JOIN
# REQ 5013 : remove pytest-cov warning for PyxlSqlInternalError


# ----------------------- Bugs
# REQ 9000 : BUG: 2nd SET clause cannot use items computed in a previous SET

# ---------------------------------------------------------------------------------------------------
# class SqlWb
# ---------------------------------------------------------------------------------------------------


class SqlWb(PyxlWorkbook):
    column_names = 'STATEMENT', 'First', 'KEY', 'Second', 'CONDITION', 'Third'
    sql_sheet_name = 'Pyxl SQL'

    def __init__(self, runner: AbstractRunner, file_name, file_path=None):
        super().__init__(file_name, file_path=file_path)
        self.runner = runner
        self.parser = Parser(runner)
        self.parse_commands()

    def parse_commands(self):
        current_command: Optional[AbstractStatement] = None
        active_sheet: PyxlSheet
        for post in ["", " 0", " 1", " 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9"]:
            active_sheet: PyxlSheet = self.get_sheet(SqlWb.sql_sheet_name + post, raise_exception=False)
            if active_sheet:
                break
        if active_sheet is None:
            PyxlSqlError.warning(f"file '{self.filename}' does not hold any '{SqlWb.sql_sheet_name}' sheet")
            return

        for row in active_sheet.get_row_range():
            word = active_sheet.get_val(row, self.column_names[0])
            if word is None:
                if current_command is not None and current_command.is_a_command():
                    try:
                        current_command.execute()
                    except PyxlSqlError as error:
                        error.print("Executing")
                current_command = None
                continue

            values = []
            cells = []
            for param in self.column_names[1:]:
                val = active_sheet.get_val(row, param)
                cell = active_sheet.get_cell(row, param)
                if val is None:
                    break
                values.append(val)
                cells.append(cell)

            PyxlSqlError.set_line(self.filename + ':[' + SqlWb.sql_sheet_name + ']', row, [word]+values)
            try:
                all_vals = [v.strip() if isinstance(v,str) else v for v in [word]+values] # R E Q 0004
                new_item = self.parser.parse(active_sheet, all_vals, cells)
            except PyxlSqlError as current_error:
                current_error.print()
                continue

            if new_item.is_a_command():
                if current_command is not None and current_command.is_a_command():
                    current_command.execute()
                current_command = new_item

        if current_command is not None and current_command.is_a_command():
            current_command.execute()


# ------------------------------------------------------------
# Class PyxlSqlRunner
# ------------------------------------------------------------


class PyxlRunner(AbstractRunner):
    def __init__(self, arguments=None):
        super().__init__()
        self.parser = argparse.ArgumentParser(description='execute PyxlSql commands in Excel files')
        self.parser.add_argument('--filepath', '-p', help="path for included files", type=str, action='append')
        self.parser.add_argument('--files', '-f', help="(multiple times): process this file",
                                 type=str, dest='files', action='append')
        self.parser.add_argument('--dir', '-d', help="process all excel files in the directory",
                                 type=str, dest='dir', action='store')

        self.parser.add_argument('--licence', help="prints the LICENCE", action='store_true')
        self.parser.add_argument('--full-help', help="prints the complete help, and exits", action='store_true')
        self.parser.add_argument('--parse-only', help="parse PyxlSql commands, verifies syntax only, and exits",
                                 action='store_true')

        self.args = self.parser.parse_args() if arguments is None else self.parser.parse_args(arguments)

        d = self.args.dir or "."
        self.dir = d if d[-1] == "/" or d[-1] == '\\' else d+"/"
        file_path = self.args.filepath or [self.dir]
        self.file_path = list(map(lambda f: f if f[-1] == "/" or f[-1] == '\\' else f+"/", file_path))
        self.files = self.args.files or list(map(lambda f: self.dir + f, os.listdir(self.dir)))

    def build(self, arguments=None):
        return PyxlRunner(arguments)

    def run(self):
        for existing_file in self.files:
            if os.path.isfile(existing_file):
                if re.match(r".*\.xls(x|m|)$", existing_file):
                    SqlWb(self, existing_file, file_path=self.file_path)
            else:
                PyxlSqlError("Non existing file", '{' + existing_file + '}')

    def run_first(self):
        """Used for tests with pytest"""
        for existing_file in self.files:
            if os.path.isfile(existing_file) and re.match(r".*\.xls(x|m|)$", existing_file):
                return SqlWb(self, existing_file, file_path=self.file_path)
        raise PyxlSqlError("No file to process", '{' + self.files[0] + '}')

def run_pyxl_sql():
    my_runner = PyxlRunner()
    my_runner.run()

if __name__ == "__main__":
    run_pyxl_sql()
