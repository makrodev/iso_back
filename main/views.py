import csv
import os
import random
import datetime

from django.core.files.base import ContentFile, File
from django.db import connection
from django.shortcuts import redirect
from PIL import Image
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

    Admin.objects.create_superuser(
        phone=admin_data['login'],
        password=admin_data['login'],
    )

    for i in range(1, 5):
        admin_data = {"login": f"ali{i}"}

        Admin.objects.create_is_staff(
            phone=admin_data['login'],
            password=admin_data['login'],
        )

    print("Admin import successfully!", end="\n\n")


def clientSeed():
    truncate("client")
    for i in range(1, 15):
        Client.objects.create(
            phone=998971111110 + i,
            tg_id=1 + i,
            name="client" + str(i)
        )
    print("Client was create successfully")


def violationSeed():
    truncate("violation")
    with open("media/test/test.png", 'rb') as f:

        for i in range(1, 3000):
            client_list = Client.objects.values_list('id')
            client_id = random.choice(client_list)[0]

            region_list = Region.objects.values_list('id')
            region_id = random.choice(region_list)[0]

            shop_list = Shop.objects.filter(region_id=region_id).values_list('id')
            shop_id = random.choice(shop_list)[0]

            department_list = Department.objects.values_list('id')
            department_id = random.choice(department_list)[0]

            problem_list = Problem.objects.values_list('id')
            problem_id = random.choice(problem_list)[0]

            disparity_list = Disparity.objects.filter(problem_id=problem_id).values_list('id')
            disparity_id = random.choice(disparity_list)[0]

            processes = Process.objects.values_list('id')
            random_process_id = random.choice(processes)[0]

            admins = Admin.objects.values_list('id')
            random_admins_id = random.choice(admins)[0]

            statuses = Status.objects.values_list('id')
            random_statuses_id = random.choice(statuses)[0]

            comment = "test_comment"

            Violation.objects.create(
                region_id=region_id,
                shop_id=shop_id,
                department_id=department_id,
                problem_id=problem_id,
                disparity_id=disparity_id,
                comment=comment,
                client_id=client_id,
                process_id=random_process_id,
                response_admin_id=random_admins_id,
                status_id=random_statuses_id,
                photo=File(f, name=f"test{i}.png"),
            )

    change_date_violation()
    print("Violation import successfully!", end="\n\n")


def change_date_violation():
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
    print("Violation date change successfully!", end="\n\n")


def violation_response_admin_random():
    admins = Admin.objects.filter(is_staff=1, is_superuser=0).all()
    admin_list = []
    for admin in admins:
        admin_list.append(admin.id)

    violations = Violation.objects.all()
    for violation in violations:
        admin_id = random.choice(admin_list)
        violation_row = Violation.objects.get(id=violation.id)
        violation_row.response_admin_id = admin_id
        violation_row.response_person_description = f"response_description {violation_row.id}"
        violation_row.result_action = f"result_action {violation_row.id}"
        violation_row.save()

    print("Violation response admin was changed")


def clear_data():
    truncate("client")
    truncate("violation")


def dbSeed():
    check_foreign_key(0)
    # adminSeed()
    # clientSeed()
    # processAdminSeed()
    # statusAdminSeed()
    buttonSeed()
    contentSeed()
    # regionSeed()
    # shopSeed()
    # departmentSeed()
    # problemSeed()
    # disparitySeed()
    # violationSeed()
    # violation_response_admin_random()
    # clear_data()
    check_foreign_key(1)
    print("OK!")
