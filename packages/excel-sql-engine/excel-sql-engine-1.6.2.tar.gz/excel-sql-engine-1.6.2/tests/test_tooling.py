# ---------------------------------------------------------------------------------------------------------------
# PyxlSQL project
# This program and library is licenced under the European Union Public Licence v1.2 (see LICENCE)
# developed by fabien.battini@gmail.com
# ---------------------------------------------------------------------------------------------------------------

import inspect
from itertools import repeat
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from PyxlSql.pyxlSql import  SqlWb, PyxlRunner
from PyxlSql.pyxlErrors import PyxlSqlError


class TestedWb:
    @staticmethod
    def build(args):
        cmdline = PyxlRunner(args)
        sql: SqlWb = cmdline.run()
        return sql

    @staticmethod
    def get_line(sql: SqlWb, sheet_name: str, row: int):
        if sql is None:
            assert sql is not None
        sheet = sql.get_sheet(sheet_name)
        columns = sheet.columns
        res = [sheet.get_val(row, field) for field in columns]
        return res

    @staticmethod
    def assert_equal(expected, actual, context: str, delta=0.0):
        if expected is None:
            msg = f"Line:{str(inspect.currentframe().f_lineno)}: {context} {str(actual)} should be None"
            assert actual is None, msg
            return

        msg = f"Line:{str(inspect.currentframe().f_lineno)}: {context} {str(actual)} should Not be None"
        assert actual is not None, msg

        if isinstance(expected, str):
            msg = f"Line:{str(inspect.currentframe().f_lineno)}: {context} string '{str(actual)}' should be '{str(expected)}'"
            assert isinstance(actual, str) and expected == actual, msg
            return

        msg = f"Line:{str(inspect.currentframe().f_lineno)}: {context} '{str(actual)}' should not be a string, but a {type(expected)}"
        assert not isinstance(actual, str), msg

        msg = f"Line:{str(inspect.currentframe().f_lineno)}: {context} {str(actual)} should de {str(expected)} +/- {delta}"
        assert ((expected - delta) <= actual <= (expected + delta)), msg

    @staticmethod
    def assert_sheet_exists(sql: SqlWb, sheet_name: str):
        sheet = sql.get_sheet(sheet_name, False)
        msg = f"Line:{str(inspect.currentframe().f_lineno)}: Sheet '{str(sheet_name)}' should exist"
        assert sheet is not None, msg

    @staticmethod
    def assert_sheet_does_not_exists(sql: SqlWb, sheet_name: str):
        sheet = sql.get_sheet(sheet_name, raise_exception=False)
        msg = f"Line:{str(inspect.currentframe().f_lineno)}: Sheet '{str(sheet_name)}' should not exist"
        assert sheet is None, msg

    @staticmethod
    def assert_line(sql: SqlWb, sheet_name: str, row: int, expected: list, delta=0.0):
        values = TestedWb.get_line(sql, sheet_name, row)
        sheet = sql.get_sheet(sheet_name)
        columns = sheet.columns
        context = [f"[{sheet_name}]'{field}':{row}" for field in columns]

        list(map(TestedWb.assert_equal, expected, values, context, repeat(delta)))

    @staticmethod
    def assert_value(sql: SqlWb, sheet_name: str, field: str, row: int, expected, context: str, delta=0):
        sheet = sql.get_sheet(sheet_name)
        TestedWb.assert_equal(sheet.get_val(row, field), expected, context, delta)

    @staticmethod
    def assert_format(sql: SqlWb,
                      sheet_name1: str, field1: str, row1: int,
                      sheet_name2: str, field2: str, row2: int,
                      number_format=None, style=None, fill=None, font=None):
        sheet1 = sql.get_sheet(sheet_name1)
        cell1 = sheet1.get_cell(row1, field1)
        msg = f"[{sheet_name1}]'{field1}':{row1}"

        context = f"Line:{str(inspect.currentframe().f_lineno)}: {msg}"
        sheet2 = sql.get_sheet(sheet_name2)
        cell2 = sheet2.get_cell(row2, field2)

        if number_format:
            TestedWb.assert_equal(cell1.number_format, cell2.number_format, context + ' number_format')
        if style:
            TestedWb.assert_equal(cell1.style, cell2.style, context + ' style')
        if font:
            TestedWb.assert_equal(cell1.font.name, cell2.font.name, context + ' font')
        if fill:
            TestedWb.assert_equal(cell1.fill.tagname, cell2.fill.tagname, context + ' fill')

    @staticmethod
    def assert_not_none(sql: SqlWb, sheet_name: str, field: str, row: int):
        sheet = sql.get_sheet(sheet_name)
        context = f"[{sheet_name}]{field}:{row}"

        expected = sheet.get_val(row, field)
        msg = f"Line:{str(inspect.currentframe().f_lineno)}: {context} {str(expected)} != None"
        assert expected is not None, msg

    @staticmethod
    def assert_error_start(err_nb: int, start: str):

        msg = f"Line:{str(inspect.currentframe().f_lineno)}: Error[{err_nb}] not reached"
        assert PyxlSqlError.error_count >= err_nb, msg
        if PyxlSqlError.error_count < err_nb:
            return
        err = PyxlSqlError.error_list[err_nb]
        msg = f"Line:{str(inspect.currentframe().f_lineno)}: Error[{err_nb}] '{err[:40]}' != '{start[:40]}' "
        assert PyxlSqlError.error_list[err_nb].startswith(start), msg

    @staticmethod
    def assert_error_number(err_nb: int):
        msg = f"Line:{str(inspect.currentframe().f_lineno)}: Error[{err_nb}] is not the max[{PyxlSqlError.error_count}]"
        assert PyxlSqlError.error_count == err_nb, msg

    @staticmethod
    def assert_warning_start(warning_nb: int, start: str):
        msg = f"Line:{str(inspect.currentframe().f_lineno)}: Warning[{warning_nb}] not reached"

        assert PyxlSqlError.warning_count >= warning_nb, msg
        if PyxlSqlError.warning_count < warning_nb:
            return
        warning = PyxlSqlError.warning_list[warning_nb]
        msg = f"Line:{str(inspect.currentframe().f_lineno)}: Warning[{warning_nb}] '{warning[:40]}' != '{start[:40]}' "
        assert PyxlSqlError.warning_list[warning_nb].startswith(start), msg

    @staticmethod
    def assert_warning_number(warning_nb: int):
        msg = f"Line:{str(inspect.currentframe().f_lineno)}: " + \
              f"Error[{warning_nb}] is not the max[{PyxlSqlError.warning_count}]"
        assert PyxlSqlError.warning_count == warning_nb, msg
