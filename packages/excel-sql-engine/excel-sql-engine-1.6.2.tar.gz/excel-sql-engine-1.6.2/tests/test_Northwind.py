# ---------------------------------------------------------------------------------------------------------------
# PyxlSQL project
# This program and library is licenced under the European Union Public Licence v1.2 (see LICENCE)
# developed by fabien.battini@gmail.com
# ---------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------
# test_Northwind.py
# ---------------------------------------------------------------------------------------------------------------
# This test is intended to be run from PyxlSQL directory by invoking pytest

from test_tooling import TestedWb
from PyxlSql.pyxlErrors import PyxlSqlError
from PyxlSql.pyxlWorkbook import PyxlWorkbook


def test_northwind():
    PyxlSqlError.reset()
    TestedWb.build(["tests/Environemental.xlsx"])  # noqa   should not contain any code
    TestedWb.assert_warning_start(0, 'file \'tests/Environemental.xlsx\' does not ')  # noqa
    TestedWb.assert_warning_number(1)
    PyxlSqlError.reset()

    tcl = TestedWb.build(["tests/Test_pyxlsql.xlsx"]) # noqa

    TestedWb.assert_line(tcl, "Auto", 2, ["Info 0", "Argentina", 10250, 12300, 14760, "=(C2+D2+E2)/3"], delta=1.0)
    TestedWb.assert_line(tcl, "Auto", 3, ["Info 1", "Austria",   22365, 26838, 32205, "=(C3+D3+E3)/3"], delta=1.0)
    TestedWb.assert_line(tcl, "Auto", 25, ["Info 23", "Venezuela", 35268, 42321, 50785, "=(C25+D25+E25)/3"], delta=1.0)
    TestedWb.assert_line(tcl, "Auto", 26, [None, None, None, None, None, None], delta=1.0)
    # testing propagation of formatting
    TestedWb.assert_format(tcl, "Auto", "2019", 3, "Auto", "2019", 2,
                           number_format=True, style=True, font=True, fill=True )

    TestedWb.assert_line(tcl, "Select", 2, ["Alfreds Futterkiste", None])                   # noqa
    TestedWb.assert_line(tcl, "Select", 3, ["Ana Trujillo Emparedados y helados", 10308])   # noqa
    TestedWb.assert_line(tcl, "Select", 5, ["Around the Horn", 10355])
    TestedWb.assert_line(tcl, "Select", 6, ["Around the Horn", 10383])
    TestedWb.assert_line(tcl, "Select", 100, ["La maison d'Asie", 10413])                   # noqa
    TestedWb.assert_line(tcl, "Select", 214, ["Wolski", 10374])                             # noqa
    TestedWb.assert_line(tcl, "Select", 215, [None, None])

    TestedWb.assert_line(tcl, "Right Join", 2, [None, "West", "Adam"])
    TestedWb.assert_line(tcl, "Right Join", 3, [10248, "Buchanan", "Steven"])
    TestedWb.assert_line(tcl, "Right Join", 4, [10249, "Suyama", "Michael"])                    # noqa
    TestedWb.assert_line(tcl, "Right Join", 100, [10345, "Fuller", "Andrew"])
    TestedWb.assert_line(tcl, "Right Join", 198, [10443, "Callahan", "Laura"])                  # noqa
    TestedWb.assert_line(tcl, "Right Join", 199, [None, None, None])

    TestedWb.assert_line(tcl, "Inner Join", 2, [10308, 	"Ana Trujillo Emparedados y helados"])  # noqa
    TestedWb.assert_line(tcl, "Inner Join", 3, [10365, "Antonio Moreno Taquería"])              # noqa
    TestedWb.assert_line(tcl, "Inner Join", 4, [10355, "Around the Horn"])                      # noqa
    TestedWb.assert_line(tcl, "Inner Join", 100, [10275, "Magazzini Alimentari Riuniti"])       # noqa
    TestedWb.assert_line(tcl, "Inner Join", 197, [10374, "Wolski"])                             # noqa
    TestedWb.assert_line(tcl, "Inner Join", 198, [None, None])

    TestedWb.assert_line(tcl, "Full Join", 2, [None, "Alfreds Futterkiste"])                    # noqa
    TestedWb.assert_line(tcl, "Full Join", 3, [10308, "Ana Trujillo Emparedados y helados"])    # noqa
    TestedWb.assert_line(tcl, "Full Join", 4, [10365, "Antonio Moreno Taquería"])               # noqa
    TestedWb.assert_line(tcl, "Full Join", 100, [10413, "La maison d'Asie"])                    # noqa
    TestedWb.assert_line(tcl, "Full Join", 214, [10374, "Wolski"])                              # noqa
    TestedWb.assert_line(tcl, "Full Join", 215, [None, None])

    TestedWb.assert_line(tcl, "Having", 2, ["UK",	7])
    TestedWb.assert_line(tcl, "Having", 3, ["Brazil",	9])
    TestedWb.assert_line(tcl, "Having", 4, ["Germany",	11])
    TestedWb.assert_line(tcl, "Having", 5, ["France", 11])
    TestedWb.assert_line(tcl, "Having", 6, ["USA", 13])

    TestedWb.assert_line(tcl, "GroupBy", 2, [1, "Administration", 2358, 4598, 3402])
    TestedWb.assert_line(tcl, "GroupBy", 3, [2, "Marketing", 1520, 3520, 2366])
    TestedWb.assert_line(tcl, "GroupBy", 4, [3, "Purchasing", 1584, 3652, 2517])
    TestedWb.assert_line(tcl, "GroupBy", 5, [4, "Sales", 1000, 5450, 2031])

    TestedWb.assert_line(tcl, "Order", 2, ["Argentina",
                                           "Cactus Comidas para llevar", 12, "Patricio Simpson"])      # noqa
    TestedWb.assert_line(tcl, "Order", 3, ["Argentina",
                                           "Océano Atlántico Ltda.", 54, "Yvonne Moncada"])            # noqa
    TestedWb.assert_line(tcl, "Order", 92, ["Venezuela",
                                            "LINO-Delicateses", 47, "Felipe Izquierdo"])               # noqa

    TestedWb.assert_line(tcl, "USA commands", 2,
                    [10262, "RATTC", "Rattlesnake Canyon Grocery", "Albuquerque"])  # noqa
    TestedWb.assert_line(tcl, "USA commands", 14,
                    [10329, "SPLIR", "Split Rail Beer & Ale", "Lander"])  # noqa
    TestedWb.assert_line(tcl, "USA commands", 122,
                    [11066, "WHITC", "White Clover Markets", "Seattle"])  # noqa
    # verify the last line
    TestedWb.assert_line(tcl, "USA commands", 123,
                         [11077, "RATTC", "Rattlesnake Canyon Grocery", "Albuquerque"])  # noqa
    TestedWb.assert_line(tcl, "USA commands", 124, [None, None, None, None])

    # testing direct formatting of cell
    TestedWb.assert_format(tcl, "USA commands", "Total", 3, "Header", "Value", 8,
                           number_format=True, style=True, font=True, fill=True )

    TestedWb.assert_not_none(tcl, "Market", "Country", 2)
    TestedWb.assert_not_none(tcl, "Header", "Value", 3)
    TestedWb.assert_not_none(tcl, "Header", "Value", 4)
    TestedWb.assert_not_none(tcl, "Header", "Value", 5)

    TestedWb.assert_sheet_does_not_exists(tcl, 'To be renamed')
    TestedWb.assert_sheet_exists(tcl,'After rename')

    TestedWb.assert_line(tcl, "Pivot", 2,
                         ["Medium",	"Y", "USA",	"= E2/$E$25"])
    TestedWb.assert_line(tcl, "Pivot", 3,
                         ["High", "Y", "Canada", "= E3/$E$25"])
    TestedWb.assert_line(tcl, "Pivot", 24,
                        [None,None, "Switzerland",	"= E24/$E$25"])

    step2 = PyxlWorkbook("tests/outputs/northwind-results-stage2.xlsx")  # noqa
    TestedWb.assert_not_none(step2, "Header", "Value", 2)
    TestedWb.assert_line(step2, "Best", 2, ["Info 9", "Finland", 12228.4586666667], delta = 0.5)
    TestedWb.assert_line(step2, "Best", 24, ["Info 22", "USA", 678008.24], delta = 0.5)

    PyxlSqlError.reset()
    TestedWb.build(["tests/test_errors.xlsx", "--full-help", "--version", "--licence"] )
    TestedWb.assert_error_start(0, 'tests/test_errors.xlsx:[Pyxl SQL]:3:  \'[\'WHERE\',')
    TestedWb.assert_error_start(1, 'tests/test_errors.xlsx:[Pyxl SQL]:5:  \'[\'UPDATE\', ')
    TestedWb.assert_error_start(2, 'tests/test_errors.xlsx:[Pyxl SQL]:6:  \'[\'LEFT JOIN\',')
    TestedWb.assert_error_start(3, 'tests/test_errors.xlsx:[Pyxl SQL]:11:  \'[\'EXAMPLE ERROR\',')

    TestedWb.assert_error_number(4)


if __name__ == "__main__":
    test_northwind()
