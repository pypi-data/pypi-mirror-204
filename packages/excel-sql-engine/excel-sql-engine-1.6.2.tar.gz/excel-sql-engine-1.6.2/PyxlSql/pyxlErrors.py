# ---------------------------------------------------------------------------------------------------------------
# PyxlSQL project
# This program and library is licenced under the European Union Public Licence v1.2 (see LICENCE)
# developed by fabien.battini@gmail.com
# ---------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------
# Management of exceptions for PyxlSql
# ---------------------------------------------------------------------------------------------------------------

import sys
class PyxlSqlError(Exception):
    """Base class for exceptions in this module."""
    current_line = ""
    error_count = 0
    error_list: list[str] = []
    warning_count = 0
    warning_list: list[str] = []

    def __init__(self, message: str, context: str):
        self.context = context
        self.message = message

    @staticmethod
    def reset():
        PyxlSqlError.current_line = ""
        PyxlSqlError.error_count = 0
        PyxlSqlError.error_list = []
        PyxlSqlError.warning_count = 0
        PyxlSqlError.warning_list = []

    @staticmethod
    def warning(msg):
        print(f"WARNING: {msg}")
        PyxlSqlError.warning_count += 1
        PyxlSqlError.warning_list.append(msg)

    @staticmethod
    def info(msg):
        print(f"Info: {msg}")

    def print(self, level="ERROR"):
        print(f"\n{level}: {PyxlSqlError.current_line or 'not a SQL statement'}")
        print(f"{level}:     {self.message}")
        print(f"{level}:     {self.context}\n", flush=True)
        sys.stdout.flush()
        PyxlSqlError.error_count += 1
        PyxlSqlError.error_list.append(PyxlSqlError.current_line + " " + self.message + " " + self.context)
        if PyxlSqlError.error_count > 20:
            print("\nFATAL ERROR: Too much errors, aborting", flush=True)
            exit(-1)

    @staticmethod
    def set_line(filename, line_number, *items):
        PyxlSqlError.current_line = f"{filename}:{line_number}: "
        for f in items:
            PyxlSqlError.current_line += " '" + str(f) + "'"

class PyxlSqlWarning(PyxlSqlError):
    def __init__(self, msg, context: str):
        super().__init__(msg, context)
        self.warning(msg)

class PyxlSqlInternalError(PyxlSqlError):
    def __init__(self, context: str):
        super().__init__("Internal ", context)
        self.print()


class PyxlSqlColumnError(PyxlSqlError):
    def __init__(self, column, context: str):
        super().__init__(f"unknown column '{column}'", context)
        self.print()


class PyxlSqlSheetError(PyxlSqlError):
    def __init__(self, sheet, context: str):
        super().__init__(f"unknown sheet '{sheet}'", context)
        self.print()


class PyxlSqlParseError(PyxlSqlError):
    def __init__(self, message, context: str):
        super().__init__("SQL SYNTAX : " + message, context)
        self.print()


class PyxlSqlExecutionError(PyxlSqlError):
    def __init__(self, message, context: str):
        super().__init__("PYTHON SYNTAX : " + message, context)
        self.print()


class PyxlSqlCmdlineError(PyxlSqlError):
    def __init__(self, message, context: str):
        super().__init__("Arguments : " + message, context)
        self.print()
