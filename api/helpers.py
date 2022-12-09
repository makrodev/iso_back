import calendar
from openpyxl.styles import Alignment, PatternFill, Border, Side, Font

from datetime import date

from openpyxl.utils import get_column_letter


class ExcelHelpers:
    def sheet_title(self, ws, cell, row):
        font = Font(
            bold=True,
        )

        side = Side(border_style="thick", color="000000")
        border = Border(
            top=side,
            bottom=side,
            left=side,
            right=side,
        )

        fill = PatternFill("solid", fgColor="00C0C0C0")
        align = Alignment(vertical='center')

        for key in cell:
            ws[f'{key}{row}'] = cell[key]
            ws[f'{key}{row}'].font = font
            ws[f'{key}{row}'].border = border
            ws[f'{key}{row}'].fill = fill
            ws[f'{key}{row}'].alignment = align

    def sheet_text(self, ws, cell, row):
        font = Font(
            bold=True,
        )

        for key in cell:
            ws[f'{key}{row}'] = cell[key]
            ws[f'{key}{row}'].font = font

    def sheet_width(self, ws, cell):
        for key in cell:
            ws.column_dimensions[key].width = 26

    def created_at_from_to_generate(self, year, month):
        year2 = year
        if month < 12:
            month2 = int(month) + 1
        else:
            month2 = 1
            year2 = int(year) + 1

        result = {
            "from": f"{year}-{month}-01 00:00:00.000000",
            "to": f"{year2}-{month2}-01 00:00:00.000000",
        }
        return result

    def days_in_month_func(self, year, month):
        days_in_month_list = []
        days_in_week_list = []
        last_day_of_month = calendar.monthrange(year, month)[1]
        for day in range(1, last_day_of_month):
            intDay = date(year=year, month=month, day=day).weekday()
            if intDay in [0, 1, 2, 3, 4]:
                days_in_week_list.append(day)
            else:
                if days_in_week_list:
                    days_in_month_list.append(days_in_week_list)
                days_in_week_list = []

        return days_in_month_list
