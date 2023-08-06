# ---------------------------------------------------------------------------------------------------------------
# PyxlSQL project
# This program and library is licenced under the European Union Public Licence v1.2 (see LICENCE)
# developed by fabien.battini@gmail.com
# ---------------------------------------------------------------------------------------------------------------

class PyxlFullHelp:
    def __init__(self):
        pass

    @staticmethod
    def print():
        print("Grammar of pyxlSQL")			# noqa
        print("##################")			# noqa
        print("")			# noqa
        print("Column names")			# noqa
        print("*************")			# noqa
        print("")			# noqa
        print("Column names are defined as::")			# noqa
        print("")			# noqa
        print("    Column names :  \"STATEMENT\" \"First\"  \"KEY\" \"Second\"  \"CONDITION\" \"third\"")			# noqa
        print("    Column names starting with # are comments")			# noqa
        print("    Row    names starting with # are comments")			# noqa
        print("")			# noqa
        print("Values")			# noqa
        print("******")			# noqa
        print("")			# noqa
        print("THe values used by all clauses and commands are defined by::")			# noqa
        print("")			# noqa
        print("    Aggregation_key :=  \"COUNT\" | \"MIN\" | \"MAX\" | \"SUM\" | \"AVG\"")			# noqa
        print("    Join_key        :=  \"LEFT JOIN\" | \"RIGHT JOIN\" | \"INNER JOIN\" | \"FULL JOIN\"")			# noqa
        print("                        # Not implemented:  \"CROSS JOIN\"")			# noqa
        print("      ")			# noqa
        print("    field            A constant that must be a field name")			# noqa
        print("      ")			# noqa
        print("    expr()           is a PYTHON expression")			# noqa
        print("                     starts with \":= \"")			# noqa
        print("                     A PYTHON expression that evaluates to something within an environment")			# noqa
        print("                     indexes indicate in which context the expression can be evaluated.")			# noqa
        print("                     O = destination")			# noqa
        print("                     1 = first source")			# noqa
        print("                     2 = second source etc.")			# noqa
        print("     ")			# noqa
        print("     ")			# noqa
        print("    red_expr()       is a PYTHON expression used for reduction after a 'GROUP BY'")			# noqa
        print("                     starts with \"$= \"")			# noqa
        print("                     Example: \"$= functools.reduce(min, #$)\" is the expression used to build MIN")			# noqa
        print("                     #$ of @$ will be replaced by the list of values to be reduced")			# noqa
        print("     ")			# noqa
        print("     ")			# noqa
        print("    formula          starts with '='")			# noqa
        print("                     An EXCEL formula, will be evaluated by excel next time the file is loaded by excel")			# noqa
        print("                     Example: '=IF(NOT(ISERROR(FIND(\"Nag\",H2))),\"Nag\",IF(NOT(ISERROR(FIND(\"Con\",H2))),\"Con\", \"\"))'")			# noqa
        print("                     Example: '=SUM(M2:Q2)/SUM(R2:V2)'")			# noqa
        print("                     Example: '=J2/K2'")			# noqa
        print("    ")			# noqa
        print("    Unless stated otherwise, items are strings that are not evaluated")			# noqa
        print("")			# noqa
        print("    right_value     := field | expr | formula                    # To do a constant, use an expr. e.g: ':= 2021'")			# noqa
        print("    left_value      := field | expr                              # the expression MUST evaluate to a field name")			# noqa
        print("")			# noqa
        print("    dst_sheet, src_sheet are descriptors of sheets that must exist when the statement is reached")			# noqa
        print("    src_field is a field that must exist in the src sheet")			# noqa
        print("    dst_field is a field in the destination that will be created if not existing")			# noqa
        print("    src_expr is an expression that will be evaluated in the context of the source sheet")			# noqa
        print("    dst_expr is an expression that will be evaluated in the context of the destination sheet")			# noqa
        print("    expr is is an expression that will be evaluated in the context of BOTH source and destination")			# noqa
        print("    filename follows a valid filename syntax")			# noqa
        print("    cell is a string that describes an Excel cell in the Column-letter+Row Number method, such as 'A1'")			# noqa
        print("")			# noqa
        print("")			# noqa
        print("Clauses")			# noqa
        print("*******")			# noqa
        print("")			# noqa
        print("Clauses are a parts of commands, put on a separate line::")			# noqa
        print("")			# noqa
        print("    # According to https://www.sqlservertutorial.net/sql-server-basics/sql-server-update-join/")			# noqa
        print("    # when UPDATE is used joining the src table with itself,")			# noqa
        print("    # we simply write it again in the From clause")			# noqa
        print("    # cf https://www.w3schools.com/sql/sql_having.asp for the order of clauses")			# noqa
        print("")			# noqa
        print("    Set_clause     := \"SET\" dst_field ( \"=\" src_expr(1,2) [\"WHEN\" src_expr(1,2)]  |")			# noqa
        print("                                        \"AGGREGATES\" expr() \"WITH\" red_expr   |")			# noqa
        print("                                        Aggregation_key expr()                )")			# noqa
        print("    UID_clause     := \"UID\" dst_field \"=\" example")			# noqa
        print("    Format_clause  := \"FORMAT\" dst_field \"=\" example [WHEN expr]")			# noqa
        print("    From_clause    := \"FROM\" src_sheet [\"AS\" alias]")			# noqa
        print("    Join_clause    := Join_key src_sheet [\"AS\" alias]  ")			# noqa
        print("    on_clause      := \"ON\" first_expr(1) \"=\" second_expr(2)")			# noqa
        print("    Where_clause   := \"WHERE\" expr(0,1,2)")			# noqa
        print("    Group_clause   := \"GROUP BY\" red_expr(1,2)")			# noqa
        print("    Order_clause   := \"ORDER BY\" expr(0) ")			# noqa
        print("    Having_clause  := \"HAVING\" expr(0)")			# noqa
        print("    Comment_clause := \"COMMENT\" Any *")			# noqa
        print("")			# noqa
        print("Commands")			# noqa
        print("********")			# noqa
        print("")			# noqa
        print("Commands are the top level component::")			# noqa
        print("")			# noqa
        print("    Select_cmd     := \"SELECT INTO\"  dst_sheet: string  (\"AS\" alias) {")			# noqa
        print("                       Set_clause *")			# noqa
        print("                       UID_clause *")			# noqa
        print("                       Format_clause *")			# noqa
        print("                       From_clause ?")			# noqa
        print("                       Join_clause *")			# noqa
        print("                       Where_clause ?")			# noqa
        print("                       Group_clause ?")			# noqa
        print("                       Having_clause ?}")			# noqa
        print("")			# noqa
        print("    Update_cmd     := \"UPDATE\" dst_sheet: string {")			# noqa
        print("                       Set_clause *")			# noqa
        print("                       UID_clause *")			# noqa
        print("                       Format_clause *")			# noqa
        print("                       From_clause    # if From_clause absent, then  this is a self join")			# noqa
        print("                       Join_clause *")			# noqa
        print("                       Where_clause ?")			# noqa
        print("                       Group_clause ?")			# noqa
        print("                       Having_clause ?}")			# noqa
        print("                    ")			# noqa
        print("    Import_cmd     := \"IMPORT\" module (\"SUBS\" sub_modules)")			# noqa
        print("")			# noqa
        print("    Delete_cmd     := \"DELETE\" dst_sheet")			# noqa
        print("")			# noqa
        print("    Save_cmd       := \"SAVE\" filename (\"FROM\" Workbook)")			# noqa
        print("")			# noqa
        print("    Rename_cmd     := \"RENAME\" dst_sheet \"AS\" new_name")			# noqa
        print("")			# noqa
        print("    Load_cmd       := \"LOAD\" filename")			# noqa
        print("")			# noqa
        print("    Pivot_cmd      := \"PIVOT\" dst_field \"FROM\" src_sheet")			# noqa
        print("")			# noqa
        print("    Dababase_cmd   := \"DATABASE\" src_sheet \"START\" cell \"END\" cell")			# noqa
        print("")			# noqa
        print("    Export_cmd     := \"EXPORT HTML\" filename (\"FROM\" dst_sheet)")			# noqa
        print("")			# noqa
        print("Commands not implemented::")			# noqa
        print("==========================")			# noqa
        print("These commands are in the roadmap,  but not yet implemented::")			# noqa
        print("")			# noqa
        print("    Insert_cmd     := \"INSERT\" dst_sheet \"AS\" new_name")			# noqa
        print("")			# noqa
    # End of patched text
