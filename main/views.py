import csv
import os
import random
import datetime

from django.db import connection
from django.shortcuts import redirect
from rest_framework.authtoken.models import Token

from main.settings import BASE_DIR
from api.models import *


def index(request):
    return redirect('admin/')


def check_foreign_key(check_num):
    cursor = connection.cursor()
    cursor.execute(f"SET FOREIGN_KEY_CHECKS = {check_num};")
    print(f"FOREIGN_KEY_CHECKS = {check_num}")


def truncate(table):
    cursor = connection.cursor()
    cursor.execute(f"TRUNCATE TABLE api_{table}")
    print(f"api_{table} truncated successfully")


def truncate_token():
    cursor = connection.cursor()
    cursor.execute(f"TRUNCATE TABLE authtoken_token")
    print(f"authtoken_token truncated successfully")


def processAdminSeed():
    truncate("process")
    with open(os.path.join(BASE_DIR, 'media/csv/process.csv'), 'r', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file)

        for line in csv_reader:
            Process.objects.create(
                title=line[0],
            )
    print("Process import successfully!", end="\n\n")


def statusAdminSeed():
    truncate("status")
    with open(os.path.join(BASE_DIR, 'media/csv/status.csv'), 'r', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file)

        for line in csv_reader:
            Status.objects.create(
                title=line[0],
            )
    print("Status import successfully!", end="\n\n")


def buttonSeed():
    truncate("button")
    with open(os.path.join(BASE_DIR, 'media/csv/buttons.csv'), 'r', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file)

        for line in csv_reader:
            Button.objects.create(
                key=line[1],
                title=line[2],
            )
    print("Buttons import successfully!", end="\n\n")


def contentSeed():
    truncate("content")
    with open(os.path.join(BASE_DIR, 'media/csv/contents.csv'), 'r', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file)

        for line in csv_reader:
            Content.objects.create(
                key=line[1],
                title=line[2],
            )
    print("Contents import successfully!", end="\n\n")


def regionSeed():
    truncate("region")
    with open(os.path.join(BASE_DIR, 'media/csv/regions.csv'), 'r', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file)

        for line in csv_reader:
            Region.objects.create(
                name=line[1],
            )
    print("Regions import successfully!", end="\n\n")


def shopSeed():
    truncate("shop")
    with open(os.path.join(BASE_DIR, 'media/csv/shops.csv'), 'r', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file)

        for line in csv_reader:
            if line[6].lower() == "null":
                line[6] = None

            Shop.objects.create(
                name=line[2],
                region_id=line[6],
            )
    print("Shops import successfully!", end="\n\n")


def departmentSeed():
    truncate("department")
    with open(os.path.join(BASE_DIR, 'media/csv/departments.csv'), 'r', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file)

        for line in csv_reader:
            Department.objects.create(
                title=line[1],
            )
    print("Department import successfully!", end="\n\n")


def problemSeed():
    truncate("problem")
    with open(os.path.join(BASE_DIR, 'media/csv/problems.csv'), 'r', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file)

        for line in csv_reader:
            Problem.objects.create(
                title=line[1],
            )
    print("Problem import successfully!", end="\n\n")


def disparitySeed():
    truncate("disparity")
    with open(os.path.join(BASE_DIR, 'media/csv/disparities.csv'), 'r', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file)

        for line in csv_reader:
            Disparity.objects.create(
                title=line[1],
                problem_id=line[5],
            )
    print("Disparity import successfully!", end="\n\n")


def adminSeed():
    truncate_token()
    truncate("admin")

    admin_data = {"login": "admin"}

    admin = Admin(
        phone=admin_data['login'],
        is_superuser=1,
    )
    admin.set_password(admin_data['login'])
    admin.save()

    token = Token.objects.create(user_id=admin.id)

    print("Admin import successfully!", end="\n\n")


def violationSeed():
    # truncate("violation")
    # with open(os.path.join(BASE_DIR, 'media/csv/violations.csv'), 'r', encoding="utf8") as csv_file:
    #     csv_reader = csv.reader(csv_file)
    #
    #     for line in csv_reader:
    #         if line[11] is not None and line[12] is not None and line[13] is not None and \
    #                 line[14] is not None and line[4] is not None and line[1] is not None and line[3] is not None:
    #             try:
    #                 client = Client.objects.get(phone=line[3])
    #             except Client.DoesNotExist:
    #                 client = Client.objects.create(
    #                     name=line[1],
    #                     phone=line[3],
    #                     tg_id=" ",
    #                 )
    #             try:
    #                 region_id = Shop.objects.get(id=line[11]).region_id
    #
    #                 processes = Process.objects.values_list('id')
    #                 random_process_id = random.choice(processes)[0]
    #
    #                 admins = Admin.objects.values_list('id')
    #                 random_admins_id = random.choice(admins)[0]
    #
    #                 statuses = Status.objects.values_list('id')
    #                 random_statuses_id = random.choice(statuses)[0]
    #
    #                 violation = Violation.objects.create(
    #                     region_id=region_id,
    #                     shop_id=line[11],
    #                     department_id=line[12],
    #                     problem_id=line[13],
    #                     disparity_id=line[14],
    #                     comment=line[4],
    #                     client_id=client.id,
    #                     process_id=random_process_id,
    #                     response_admin_id=random_admins_id,
    #                     status_id=random_statuses_id,
    #                 )
    #             except Shop.DoesNotExist:
    #                 pass

    violation_last = Violation.objects.order_by("-id").first().id

    def week_day_func(year, month, day):
        intDay = datetime.date(year=year, month=month, day=day).weekday()

        return intDay

    start_pk = 1
    end_pk = 10
    day = 0
    month = 1
    year = 2021
    while True:
        if start_pk <= violation_last:
            day += 1
            try:
                week_day = week_day_func(year, month, day)
                if week_day not in [5, 6]:
                    violations = Violation.objects.filter(pk__gte=start_pk, pk__lte=end_pk).update(
                        created_at=f"{year}-{month}-{day} 05:13:11.887018",
                        updated_at=f"{year}-{month}-{day} 05:13:11.887018",
                    )
                else:
                    continue
                start_pk += 10
                end_pk += 10
            except ValueError:
                day = 0
                month += 1
                if month == 12:
                    month = 1
                    year += 1
        else:
            return False

    print("Violation import successfully!", end="\n\n")


def clear_data():
    truncate("client")
    truncate("violation")


def dbSeed():
    check_foreign_key(0)
    adminSeed()
    # processAdminSeed()
    # statusAdminSeed()
    # buttonSeed()
    # contentSeed()
    # regionSeed()
    # shopSeed()
    # departmentSeed()
    # problemSeed()
    # disparitySeed()
    # violationSeed()
    clear_data()
    check_foreign_key(1)
    print("OK!")
