from . import helpers as api_helpers
from . import models as api_models


class ExcelUtils:
    def __init__(self, year, month, wb):
        self.year = year
        self.month = month
        self.wb = wb

    def report_market_func(self):
        created_at_from = api_helpers.ExcelHelpers.created_at_from_to_generate(self, self.year, self.month)['from']
        created_at_to = api_helpers.ExcelHelpers.created_at_from_to_generate(self, self.year, self.month)['to']

        ws_name = "Отчет по маркетам"
        ws = self.wb.create_sheet(ws_name)

        # HEADER
        row = 3

        cell = {
            "A": "Наименование магазина",
            "B": "Количество несоответствия",
        }
        api_helpers.ExcelHelpers.sheet_title(self, ws, cell, row)

        # BODY
        violations = api_models.Violation.objects.filter(
            created_at__gte=created_at_from,
            created_at__lte=created_at_to,
        )

        shops = {}
        for violation in violations:
            if violation.shop.name in shops.keys():
                shops[violation.shop.name] += 1
            else:
                shops[violation.shop.name] = 1
        shops = dict(sorted(shops.items(), key=lambda item: item[1], reverse=True))

        for shop in shops:
            row += 1
            cell = {
                "A": f"{shop}",
                "B": shops[shop],
            }
            api_helpers.ExcelHelpers.sheet_text(self, ws, cell, row)

        # FOOTER
        row += 1
        cell = {
            "A": "Общий итог",
            "B": violations.count(),
        }
        api_helpers.ExcelHelpers.sheet_title(self, ws, cell, row)
        api_helpers.ExcelHelpers.sheet_width(self, ws, cell)

    def report_process_func(self):
        created_at_from = api_helpers.ExcelHelpers.created_at_from_to_generate(self, self.year, self.month)['from']
        created_at_to = api_helpers.ExcelHelpers.created_at_from_to_generate(self, self.year, self.month)['to']
        days_in_month_list = api_helpers.ExcelHelpers.days_in_month_func(self, self.year, self.month)

        report_process_sheet_name = "Отчет процессы"
        report_process_sheet = self.wb.create_sheet(report_process_sheet_name)

        all_week_data_list = []
        process_count_list = []

        row = 1

        cell = {
            "A": "Процесс",
            "B": "Кол-во",
            "C": "100%",
            "D": f"{days_in_month_list[0][0]}-{days_in_month_list[0][-1]}.{self.month}.{self.year}",
            "E": "100%",
            "F": f"{days_in_month_list[1][0]}-{days_in_month_list[1][-1]}.{self.month}.{self.year}",
            "G": "100%",
            "H": f"{days_in_month_list[2][0]}-{days_in_month_list[2][-1]}.{self.month}.{self.year}",
            "I": "100%",
            "J": f"{days_in_month_list[3][0]}-{days_in_month_list[3][-1]}.{self.month}.{self.year}",
            "K": "100%",
        }
        api_helpers.ExcelHelpers.sheet_title(self, report_process_sheet, cell, row)


        processes = api_models.Process.objects.values("title")
        processes = [process['title'] for process in processes]
        all_processes_title = "Все"
        processes.append(all_processes_title)
        violations_count = api_models.Violation.objects.filter(
            created_at__gte=created_at_from,
            created_at__lte=created_at_to,
        ).count()

        for process in processes:
            if process != all_processes_title:
                process_id = api_models.Process.objects.get(title=process)
                violation_count = api_models.Violation.objects.filter(
                    process_id=process_id,
                    created_at__gte=created_at_from,
                    created_at__lte=created_at_to,
                ).count()
                violation_percent = 0
                if violation_percent > 0:
                    violation_percent = violation_count * 100 / violations_count
                row += 1
                cell = {
                    "A": process,
                    "B": violation_count,
                    "C": violation_percent,
                }
                api_helpers.ExcelHelpers.sheet_text(self, report_process_sheet, cell, row)

        row += 1
        cell = {
            "B": violations_count,
        }
        api_helpers.ExcelHelpers.sheet_text(self, report_process_sheet, cell, row)

        # all weeks loop
        # for day_in_week in days_in_month:
        #     created_at_list = []
        #     one_week_data_dict = {}
        #
        #     for day in day_in_week:
        #         created_at_list.append(f'{year}-{month}-{day} 00:00:00.000000')
        #
        #     violations = Violation.objects.filter(
        #         created_at__gte=created_at_list[0],
        #         created_at__lte=created_at_list[-1],
        #     )
        #
        #     for violation in violations:
        #         try:
        #             if one_week_data_dict[violation.process.title]:
        #                 one_week_data_dict[violation.process.title] += 1
        #         except KeyError:
        #             one_week_data_dict[violation.process.title] = violation.process.title
        #             one_week_data_dict[violation.process.title] = 1
        #
        #     for key in one_week_data_dict:
        #         row += 1
        #         cell = {
        #             "A": key,
        #             "B": one_week_data_dict[key],
        #         }
        #         sheet_text(report_process_sheet, cell, row)
        #
        #     process_count_list.append(violations.count())

        # row += 1
        # cell = {
        #            "A": violation.process.title,
        #            "B":,
        #        "C": "Процент",
        #             "D": process_count_list[0],
        # "E": "Процент",
        # "F": process_count_list[1],
        # "G": "Процент",
        # "H": process_count_list[2],
        # "I": "Процент",
        # "J": process_count_list[3],
        # "K": "Процент",
        # }
        # sheet_text(report_process_sheet, cell, row)

    def report_department_func(self):
        report_department_sheet_name = "Отчет по департаментам"
        report_department_sheet = self.wb.create_sheet(report_department_sheet_name)
        return report_department_sheet

    def report_attendance_func(self):
        report_attendance_sheet_name = "Отчет по посещаемости"
        report_attendance_sheet = self.wb.create_sheet(report_attendance_sheet_name)

    def report_general_func(self):
        general_sheet_name = "Общее"
        general_sheet = self.wb.create_sheet(general_sheet_name)

    # def report_weeks_func(self):
    #     week_list = api_helpers.ExcelHelpers.days_in_month_func(self, self.year, self.month)
    #     for week in week_list:
    #         week_sheet_name = f"{week_list[week][0]}-{week_list[week][-1]}.{self.month}.{self.year}"
    #         week_sheet = self.wb.create_sheet(week_sheet_name)

