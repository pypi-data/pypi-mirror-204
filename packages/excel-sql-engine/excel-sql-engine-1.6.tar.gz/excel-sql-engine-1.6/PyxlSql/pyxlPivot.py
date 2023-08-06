# ---------------------------------------------------------------------------------------------------------------
# PyxlSQL project
# This program and library is licenced under the European Union Public Licence v1.2 (see LICENCE)
# developed by fabien.battini@gmail.com
# ---------------------------------------------------------------------------------------------------------------

from openpyxl.chart import PieChart, Reference
from openpyxl.chart.marker import DataPoint
from openpyxl.drawing.colors import ColorChoice
from openpyxl.drawing.fill import PatternFillProperties
from PyxlSql.pyxlSheets import PyxlSheet

class Pivot:
    def __init__(self, dst_sheet: PyxlSheet, src_sheet : PyxlSheet,
                 first_col_name=None, use_formula=True, anonymized=False, labels_order=None):

        # row 2 can hold formats
        if labels_order is None:
            labels_order = []
        else:
            # If the Workbooks are NOT the same, then we HAVE TO anonymize
            anonymized = True
            use_formula = False

        if anonymized:
            use_formula = False

        first_column = 1 if first_col_name is None else dst_sheet.find_column(first_col_name)

        kpi = dst_sheet.get_val_by_nb(1, first_column)          # 1st column is the Field we want to filter on
        value = dst_sheet.get_val_by_nb(1, first_column + 1)    # 2nd column is the value of this field:
        # blank= No, Non blank = Yes
        labels = dst_sheet.get_val_by_nb(1, first_column + 2)   # 3rd column is row
        percent = dst_sheet.get_val_by_nb(1, first_column + 3)  # 4th column is percentage
        sums = dst_sheet.get_val_by_nb(1, first_column + 4)     # 5th column is sum of value
        field_to_filter = dst_sheet.get_val_by_nb(1, first_column + 5)
        no_value = dst_sheet.get_val_by_nb(1, first_column + 6)
        yes_value = dst_sheet.get_val_by_nb(1, first_column + 7)

        order_of_labels = list(labels_order)

        # Build the list of Filters Yes/No from Columns 5 to 7
        # and also the list of Labels to use
        yes_filters = {}
        no_filters = {}
        colors = {}

        for row_nb in dst_sheet.get_row_range():  # 2 to avoid header row
            field = None if field_to_filter is None else dst_sheet.get_string(row_nb, field_to_filter)
            yes_val = None if yes_value is None else dst_sheet.get_string(row_nb, yes_value)
            no_val = None if no_value is None else dst_sheet.get_string(row_nb, no_value)
            if field is not None and field != '' and yes_val != '':
                if field not in yes_filters:
                    yes_filters[field] = []
                yes_filters[field].append(yes_val)
            if field is not None and field != '' and no_val != '':
                if field not in no_filters:
                    no_filters[field] = []
                no_filters[field].append(no_val)

            label = dst_sheet.get_string(row_nb, labels)
            if label != '':
                order_of_labels.append(str(label))
                cell = dst_sheet.get_cell(row_nb, labels)
                colors[label] = dst_sheet.get_cell_color(cell)

        kpis = {}  # all possible KPIs
        kpi_row = 2
        table = {}  # table [Label][KPI]
        my_total = 0  # Grand Total, if we do not use formulas

        #
        #  Compute all values for each KPI, from the original Database
        #
        for row_nb in src_sheet.get_row_range():
            do_not_process = False
            my_kpi = src_sheet.get_string(row_nb, kpi)

            if my_kpi == "":
                my_kpi = "(blank)"

            my_label = src_sheet.get_string(row_nb, labels)
            if my_label == "":
                my_label = "(blank)"

            for label in yes_filters:
                val = src_sheet.get_string(row_nb, label)
                # TODO: instead a string comparison, eval an expression
                if val not in yes_filters[label]:
                    # TODO: issue warning, to be filtered out by a runtime flag
                    # sheet_name= src_sheet.full_name
                    # print(f"{sheet_name}[{row_nb}][{label}] = {val} not in {yes_filters[label]}: filtered out"
                    do_not_process = True
                    continue

            for label in no_filters:
                val = src_sheet.get_string(row_nb, label)
                # TODO: instead a string comparison, eval an expression
                if val in no_filters[label]:
                    # TODO: issue warning, to be filtered out by a runtime flag
                    # sheet_name = src_sheet.full_name
                    # print(f"{sheet_name}[{row_nb}][{label}] = {val}  in {no_filters[label]}: filtered out"
                    do_not_process = True
                    continue
            if do_not_process:
                continue

            if my_label not in table:
                table[my_label] = {}

            my_table = table[my_label]

            if my_kpi not in my_table:
                if use_formula:
                    my_table[my_kpi] = "0"
                else:
                    my_table[my_kpi] = 0

        #
            if my_kpi not in kpis:
                kpis[my_kpi] = kpi_row
                kpi_row += 1

            if use_formula:
                # here, sourceWb MUST == self
                my_value = src_sheet.get_reference(row_nb, sums, same_sheet=False)
                my_table[my_kpi] += " + " + my_value
            else:
                my_value = src_sheet.get_float(row_nb, sums)
                my_table[my_kpi] += my_value
                my_total += my_value

        # Create the KPI columns in destination
        for (my_kpi, row_nb) in kpis.items():
            dst_sheet.set_value(row_nb, kpi, my_kpi)
            dst_sheet.set_value(row_nb, value, 'Y')

        #
        for label in table.keys():
            if label not in order_of_labels:
                order_of_labels.append(label)

        row_nb = 2
        data_points = []

        for label in order_of_labels:
            if label not in table:
                continue
            my_table = table[label]
            dst_sheet.set_value(row_nb, labels, label)
            formula = "= 0 "
            for (kpi, kv) in my_table.items():
                if anonymized:
                    formula += '+ IF($B${} ="",0,{})'.format(kpis[kpi], 1000 * kv / my_total)
                else:
                    formula += '+ IF($B${} ="",0,{})'.format(kpis[kpi], kv)

            dst_sheet.set_value(row_nb, sums, formula)
            my_datapoint = DataPoint(idx=row_nb - 2)
            data_points.append(my_datapoint)
            row_nb += 1

        dst_sheet.set_value(row_nb, labels, 'TOTAL')
        max_row = row_nb

        formula = "=SUM({}:{})".format(dst_sheet.get_reference(2, sums),
                               dst_sheet.get_reference(max_row - 1, sums))
        dst_sheet.set_value(max_row, sums, formula)

        #
        for row_nb in range(2, max_row):
            formula = "= {}/{}".format(dst_sheet.get_reference(row_nb, sums, absolute=False),
                                       dst_sheet.get_reference(max_row, sums))
            dst_sheet.set_value(row_nb, percent, formula)

        formula = "=SUM({}:{})".format(dst_sheet.get_reference(2, percent),
                                       dst_sheet.get_reference(max_row - 1, percent))
        dst_sheet.set_value(max_row, percent, formula)

        #

        pie = PieChart()
        label_row = dst_sheet.find_column(labels)
        data_row = dst_sheet.find_column(percent)

        labels_ref = Reference(dst_sheet.openpyxl_sheet, min_col=label_row, min_row=2, max_row=max_row - 1)
        data_ref = Reference(dst_sheet.openpyxl_sheet, min_col=data_row, min_row=1, max_row=max_row - 1)  # CAVEAT: Min_row = 1 to get the label!!!

        pie.add_data(data_ref, titles_from_data=True)
        pie.set_categories(labels_ref)
        pie.separator = True
        pie.showBubbleSize = 30

        pie.title = sums + " by " + labels
        pie.series[0].data_points = data_points

        #
        # Colorize the chart, depending on background of Label column

        series = pie.series[0]
        prototypes = series.dPt

        for row_nb in dst_sheet.get_row_range():
            label = dst_sheet.get_string(row_nb, labels)
            if label is None or label == "TOTAL":
                continue
            color = colors[label] if label in colors else None
            if color is None or color == "000000":
                continue
            # print("row", label, row_nb, color)
            fill = PatternFillProperties("pct5")
            fill.foreground = ColorChoice(srgbClr=color)
            fill.background = ColorChoice(srgbClr=color)
            prototypes[row_nb - 2].graphicalProperties.pattFill = fill #noqa

        dst_sheet.openpyxl_sheet.add_chart(pie, "J2")
