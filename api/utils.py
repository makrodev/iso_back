from . import helpers as api_helpers
from . import models as api_models


class ExcelUtils:
    def __init__(self, year, month, wb, created_at_from, created_at_to, days_in_month_list):
        self.year = year
        self.month = month
        self.wb = wb
        self.created_at_from = created_at_from
        self.created_at_to = created_at_to
        self.days_in_month_list = days_in_month_list

    def report_market_func(self):
        ws_name = "Отчет по маркетам"
        ws = self.wb.create_sheet(ws_name)
        width = 0

        # HEADER
        row = 1

        cell = {
            "A": "Наименование магазина",
            "B": "Посетитель",
            "C": "Количество несоответствия",
        }

        width = api_helpers.ExcelHelpers.get_max_width(self, cell, width)

        api_helpers.ExcelHelpers.sheet_title(self, ws, cell, row)

        # BODY
        violations = api_models.Violation.objects.filter(
            created_at__gte=self.created_at_from,
            created_at__lte=self.created_at_to,
            is_no_violation=0,
        ).order_by("shop")
        data_list = []
        for violation in violations:
            data = {
                "shop": violation.shop.name,
                "client": violation.client.name,
            }

            if data not in data_list:
                data_list.append(data)

        for data in data_list:
            data["count"] = api_models.Violation.objects.filter(shop__name=data['shop'],
                                                                client__name=data['client']).count()

        data_list = sorted(data_list, key=lambda d: d['count'], reverse=True)

        for data in data_list:
            row += 1
            cell = {
                "A": data['shop'],
                "B": data['client'],
                "C": data['count'],
            }
            width = api_helpers.ExcelHelpers.get_max_width(self, cell, width)
            api_helpers.ExcelHelpers.sheet_text(self, ws, cell, row)

        # FOOTER
        row += 1
        cell = {
            "A": "Общий итог",
            "B": "",
            "C": violations.count(),
        }
        width = api_helpers.ExcelHelpers.get_max_width(self, cell, width)
        api_helpers.ExcelHelpers.sheet_title(self, ws, cell, row)
        api_helpers.ExcelHelpers.sheet_width(self, ws, cell, width=width + 1)

    def report_process_func(self):

        ws_name = "Отчет процессы"
        ws = self.wb.create_sheet(ws_name)
        width = 0

        # HEADER
        row = 1

        cell = {
            "A": "Процесс",
            "B": "Кол-во",
            "C": "100%",
            "D": f"{self.days_in_month_list[0][0]}-{self.days_in_month_list[0][-1]}.{self.month}.{self.year}",
            "E": "100%",
            "F": f"{self.days_in_month_list[1][0]}-{self.days_in_month_list[1][-1]}.{self.month}.{self.year}",
            "G": "100%",
            "H": f"{self.days_in_month_list[2][0]}-{self.days_in_month_list[2][-1]}.{self.month}.{self.year}",
            "I": "100%",
            "J": f"{self.days_in_month_list[3][0]}-{self.days_in_month_list[3][-1]}.{self.month}.{self.year}",
            "K": "100%",
            "L": f"{self.days_in_month_list[4][0]}-{self.days_in_month_list[4][-1]}.{self.month}.{self.year}",
            "M": "100%",
        }
        width = api_helpers.ExcelHelpers.get_max_width(self, cell, width)
        api_helpers.ExcelHelpers.sheet_width(self, ws, cell, width=width + 6)
        api_helpers.ExcelHelpers.sheet_title(self, ws, cell, row)

        # BODY
        processes = api_models.Process.objects.all()

        # ALL COUNT
        violation_all_count = api_models.Violation.objects.filter(
            created_at__gte=self.created_at_from,
            created_at__lte=self.created_at_to,
        ).count()

        week_count_list = api_helpers.ExcelHelpers.violation_weeks_count(
            self, year=self.year, month=self.month, days_in_month_list=self.days_in_month_list,
        )

        for process in processes:
            # ALL DATA
            violation_process_all_count = api_models.Violation.objects.filter(
                created_at__gte=self.created_at_from,
                created_at__lte=self.created_at_to,
                process_id=process.id,
            ).count()

            week_process_count_list = api_helpers.ExcelHelpers.violation_weeks_count(
                self, year=self.year, month=self.month, days_in_month_list=self.days_in_month_list,
                process_id=process.id
            )

            row += 1
            cell = {
                "A": process.title,
                "B": violation_process_all_count,
                "C": f"{api_helpers.ExcelHelpers.percent_count(self, violation_process_all_count, violation_all_count)}%",
                "D": week_process_count_list[0],
                "E": f"{api_helpers.ExcelHelpers.percent_count(self, week_process_count_list[0], week_count_list[0])}%",
                "F": week_process_count_list[1],
                "G": f"{api_helpers.ExcelHelpers.percent_count(self, week_process_count_list[1], week_count_list[1])}%",
                "H": week_process_count_list[2],
                "I": f"{api_helpers.ExcelHelpers.percent_count(self, week_process_count_list[2], week_count_list[2])}%",
                "J": week_process_count_list[3],
                "K": f"{api_helpers.ExcelHelpers.percent_count(self, week_process_count_list[3], week_count_list[3])}%",
            }
            try:
                cell.update({
                    "L": week_process_count_list[4],
                    "M": f"{api_helpers.ExcelHelpers.percent_count(self, week_process_count_list[4], week_count_list[4])}%",
                })
            except IndexError:
                pass
            api_helpers.ExcelHelpers.sheet_text(self, ws, cell, row)

        row += 1
        cell = {
            "B": violation_all_count,
            "D": week_count_list[0],
            "F": week_count_list[1],
            "H": week_count_list[2],
            "J": week_count_list[3],
        }
        try:
            cell.update({
                "L": week_count_list[4],
            })
        except IndexError:
            pass
        api_helpers.ExcelHelpers.sheet_text(self, ws, cell, row)

    def report_department_func(self):
        ws_name = "Отчет по департаментам"
        ws = self.wb.create_sheet(ws_name)

        width = 0

        # HEADER
        row = 1
        cell = {
            "A": "Статус",
            "B": "Ответственный департамент",
            "C": "Имя магазина",
            "D": "Количество несоответствий",

            "F": "Ответственный департамент",
            "G": "Количество несоответсвий",
        }

        width = api_helpers.ExcelHelpers.get_max_width(self, cell, width)
        api_helpers.ExcelHelpers.sheet_width(self, ws, cell, width=width + 6)
        api_helpers.ExcelHelpers.sheet_title(self, ws, cell, row)

        # BODY
        statuses = api_models.Status.objects.all()

        for status in statuses:
            violations_by_status = api_models.Violation.objects.filter(
                created_at__gte=self.created_at_from,
                created_at__lte=self.created_at_to,
                status_id=status.id,
            ).order_by("response_admin_id")
            for violation in violations_by_status:
                print(violation.response_admin.name)
                row += 1
                cell = {
                    "A": violation.status.title,
                    "B": violation.response_admin.name,
                    "C": violation.shop.name,
                    "D": 10,
                }
                api_helpers.ExcelHelpers.sheet_text(self, ws, cell, row)

        # FOOTER
        violations_count = api_models.Violation.objects.filter(
            created_at__gte=self.created_at_from,
            created_at__lte=self.created_at_to,
        ).count()
        row += 1
        cell = {
            "A": "Общий итог",
            "B": "",
            "C": "",
            "D": violations_count,
        }
        api_helpers.ExcelHelpers.sheet_title(self, ws, cell, row)


    def report_attendance_func(self):
        ws_name = "Отчет по посещаемости"
        ws = self.wb.create_sheet(ws_name)
        width = 0

        # HEADER
        row = 1
        cell = {
            "A": "Имя посещаемого",
            "B": "Кол-во посещений",
            "C": f"1 неделя ({self.days_in_month_list[0][0]}-{self.days_in_month_list[0][-1]}.{self.month}.{self.year})",
            "D": f"2 неделя ({self.days_in_month_list[1][0]}-{self.days_in_month_list[1][-1]}.{self.month}.{self.year})",
            "E": f"3 неделя ({self.days_in_month_list[2][0]}-{self.days_in_month_list[2][-1]}.{self.month}.{self.year})",
            "F": f"4 неделя ({self.days_in_month_list[3][0]}-{self.days_in_month_list[3][-1]}.{self.month}.{self.year})",
            "G": f"5 неделя ({self.days_in_month_list[4][0]}-{self.days_in_month_list[4][-1]}.{self.month}.{self.year})",
        }

        width = api_helpers.ExcelHelpers.get_max_width(self, cell, width)
        api_helpers.ExcelHelpers.sheet_width(self, ws, cell, width=width + 6)
        api_helpers.ExcelHelpers.sheet_title(self, ws, cell, row)

        # BODY
        violations = api_models.Violation.objects.filter(
            created_at__gte=self.created_at_from,
            created_at__lte=self.created_at_to,
            is_no_violation=0,
        )

        client_list = []
        for violation in violations:
            if violation.client.name not in client_list:
                client_list.append(violation.client.name)

        for client in client_list:
            row += 1
            violation_count_by_client = api_models.Violation.objects.filter(client__name=client).count()

            shops_week_list = []
            for day_in_month in self.days_in_month_list:
                violations_week_list = api_models.Violation.objects.filter(
                    client__name=client, created_at__gte=f"{self.year}-{self.month}-{day_in_month[0]}",
                    created_at__lte=f"{self.year}-{self.month}-{day_in_month[-1]}",
                ).all()
                shops_week_string = ""
                shops_week_cycle_list = []
                for violations_week in violations_week_list:
                    if violations_week.shop.name not in shops_week_cycle_list:
                        if shops_week_cycle_list:
                            shops_week_string += "\n" + violations_week.shop.name
                        else:
                            shops_week_string += violations_week.shop.name
                        shops_week_cycle_list.append(violations_week.shop.name)

                shops_week_list.append(shops_week_string)

            cell = {
                "A": client,
                "B": violation_count_by_client,
                "C": shops_week_list[0],
                "D": shops_week_list[1],
                "E": shops_week_list[2],
                "F": shops_week_list[3],
                "G": shops_week_list[4],
            }
            api_helpers.ExcelHelpers.sheet_text(self, ws, cell, row)


    def report_general_func(self):
        ws_name = "Общее"
        ws = self.wb.create_sheet(ws_name)

        width = 0

        # HEADER
        row = 1
        cell = {
            "A": "ID",
            "B": "Автор",
            "C": "Нет нарушений",
            "D": "Дата посещения",
            "E": "Регион",
            "F": "Магазин",
            "G": "Департамент",
            "H": "Проблема",
            "J": "Несоответствие",
            "K": "Коммент",
            "L": "Фото",
            "M": "Процесс",
            "N": "Ответственный отдел",
            "O": "Отчет от ответственного отдела",
            "P": "Корректирующее действие",
            "Q": "Статус",
            "R": "Дата закрытия нарушения",
        }

        width = api_helpers.ExcelHelpers.get_max_width(self, cell, width)
        api_helpers.ExcelHelpers.sheet_width(self, ws, cell, width=width + 6)
        api_helpers.ExcelHelpers.sheet_title(self, ws, cell, row)

        # BODY
        violations = api_models.Violation.objects.filter(
            created_at__gte=self.created_at_from,
            created_at__lte=self.created_at_to,
            is_no_violation=0,
        )

        for violation in violations:
            row += 1
            cell = {
                "A": violation.id,
                "B": violation.client.name,
                "C": api_helpers.ExcelHelpers.is_no_violation_text(self, violation.is_no_violation),
                "D": api_helpers.ExcelHelpers.datetime_to_text(self, violation.created_at),
                "E": violation.region.name,
                "F": violation.shop.name,
                "G": violation.department.title,
                "H": violation.problem.title,
                "J": violation.disparity.title,
                "K": violation.comment,
                "L": str(violation.photo),
                "M": violation.process.title,
                "N": violation.response_admin.name,
                "O": violation.response_person_description,
                "P": violation.result_action,
                "Q": violation.status.title,
                "R": api_helpers.ExcelHelpers.datetime_to_text(self, violation.updated_at),
            }
            api_helpers.ExcelHelpers.sheet_text(self, ws, cell, row, align_horizontal="center")

# def report_weeks_func(self):
#     week_list = api_helpers.ExcelHelpers.days_in_month_func(self, self.year, self.month)
#     for week in week_list:
#         week_sheet_name = f"{week_list[week][0]}-{week_list[week][-1]}.{self.month}.{self.year}"
#         week_sheet = self.wb.create_sheet(week_sheet_name)
