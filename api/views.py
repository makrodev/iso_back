from openpyxl import Workbook
from openpyxl.styles import Alignment, PatternFill, Border, Side, Font
from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.models import Token

from main import settings
from .models import *
from .serializers import *
from .helpers import *
from .utils import *


def CustomDoesNotExist(model):
    return f"{model} does not exist"


# Button
class ButtonAPIView(APIView):
    def get(self, request):
        buttons = Button.objects.all()
        serializer = ButtonSerializer(buttons, many=True)
        message = serializer.data
        return Response(message, status=status.HTTP_200_OK)


# Content
class ContentAPIView(APIView):
    def get(self, request):
        buttons = Content.objects.all()
        serializer = ContentSerializer(buttons, many=True)
        message = serializer.data
        return Response(message, status=status.HTTP_200_OK)


# Regions API -------------------------------------
class RegionAPIView(APIView):
    def get(self, request, *args, **kwargs):
        regions = Region.objects.all()
        serializer = RegionSerializer(regions, many=True)
        message = serializer.data
        return Response(message, status=status.HTTP_200_OK)


class RegionByNameAPIView(APIView):
    def get(self, request):
        serializer = RegionByNameSerializer(data=request.data)
        if serializer.is_valid():
            try:
                region = Region.objects.filter(name=request.data['name']).get()
                serializer = RegionByNameSerializer(region, many=False)
                message = serializer.data
                status_code = status.HTTP_200_OK
            except Region.DoesNotExist:
                message = CustomDoesNotExist("Region")
                status_code = status.HTTP_404_NOT_FOUND
        else:
            message = serializer.errors
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(message, status=status_code)


class RegionDetailAPIView(APIView):
    def get(self, request, id):
        try:
            region = Region.objects.get(id=id)
            serializer = RegionSerializer(region, many=False)
            message = serializer.data
            status_code = status.HTTP_200_OK
        except Region.DoesNotExist:
            message = CustomDoesNotExist("Region")
            status_code = status.HTTP_404_NOT_FOUND
        return Response(message, status=status_code)


# Shops API -------------------------------------
class ShopAPIView(APIView):
    def get(self, request):
        shops = Shop.objects.all()
        serializer = ShopSerializer(shops, many=True)
        message = serializer.data
        status_code = status.HTTP_200_OK
        return Response(message, status_code)


class ShopDetailAPIView(APIView):
    def get(self, request, id):
        try:
            shop = Shop.objects.get(id=id)
            serializer = ShopSerializer(shop, many=False)
            message = serializer.data
            status_code = status.HTTP_200_OK
        except Shop.DoesNotExist:
            message = CustomDoesNotExist("Shop")
            status_code = status.HTTP_404_NOT_FOUND
        return Response(message, status=status_code)


class ShopByRegionAPIView(APIView):
    def get(self, request):
        serializer = ShopByPropSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            shops = Shop.objects.filter(region_id=request.data['region']).all()
            serializer = ShopByPropSerializer(shops, many=True)
            message = serializer.data
            status_code = status.HTTP_200_OK
        else:
            message = serializer.errors
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(message, status=status_code)


class ShopByNameAPIView(APIView):
    def get(self, request):
        serializer = ShopByPropSerializer(data=request.data)
        if serializer.is_valid():
            try:
                shop = Shop.objects.get(
                    name=request.data['name'],
                    region=request.data['region'],
                )
                serializer = ShopByPropSerializer(shop, many=False)
                message = serializer.data
                status_code = status.HTTP_200_OK
            except Shop.DoesNotExist:
                message = CustomDoesNotExist("Shop")
                status_code = status.HTTP_404_NOT_FOUND
        else:
            message = serializer.errors
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(message, status=status_code)


# Departments API -------------------------------------
class DepartmentAPIView(APIView):
    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        message = serializer.data
        status_code = status.HTTP_200_OK
        return Response(message, status=status_code)


class DepartmentDetailAPIView(APIView):
    def get(self, request, id):
        try:
            department = Department.objects.get(id=id)
            serializer = DepartmentSerializer(department, many=False)
            message = serializer.data
            status_code = status.HTTP_200_OK
        except Department.DoesNotExist:
            message = CustomDoesNotExist("Department")
            status_code = status.HTTP_404_NOT_FOUND
        return Response(message, status=status_code)


class DepartmentByTitleAPIView(APIView):
    def get(self, request):
        serializer = DepartmentByTitleSerializer(data=request.data)
        if serializer.is_valid():
            try:
                department = Department.objects.get(title=request.data['title'])
                serializer = DepartmentByTitleSerializer(department, many=False)
                message = serializer.data
                status_code = status.HTTP_200_OK
            except Department.DoesNotExist:
                message = CustomDoesNotExist("Department")
                status_code = status.HTTP_404_NOT_FOUND
        else:
            message = serializer.errors
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(message, status=status_code)


# Problems API -------------------------------------
class ProblemAPIView(APIView):
    def get(self, request):
        problems = Problem.objects.all()
        serializer = ProblemSerializer(problems, many=True)
        message = serializer.data
        status_code = status.HTTP_200_OK
        return Response(message, status=status_code)


class ProblemDetailAPIView(APIView):
    def get(self, request, id):
        try:
            problem = Problem.objects.get(id=id)
            serializer = ProblemSerializer(problem, many=False)
            message = serializer.data
            status_code = status.HTTP_200_OK
        except Problem.DoesNotExist:
            message = CustomDoesNotExist("Problem")
            status_code = status.HTTP_404_NOT_FOUND
        return Response(message, status=status_code)


class ProblemByTitleAPIView(APIView):
    def get(self, request):
        serializer = ProblemByTitleSerializer(data=request.data)
        if serializer.is_valid():
            try:
                problem = Problem.objects.get(title=request.data['title'])
                serializer = ProblemByTitleSerializer(problem, many=False)
                message = serializer.data
                status_code = status.HTTP_200_OK
            except Problem.DoesNotExist:
                message = CustomDoesNotExist("Problem")
                status_code = status.HTTP_404_NOT_FOUND
        else:
            message = serializer.errors
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(message, status=status_code)


# Disparities API -------------------------------------
class DisparityAPIView(APIView):
    def get(self, request):
        disparities = Disparity.objects.all()
        serializer = DisparitySerializer(disparities, many=True)
        message = serializer.data
        status_code = status.HTTP_200_OK
        return Response(message, status_code)


class DisparityDetailAPIView(APIView):
    def get(self, request, id):
        try:
            disparity = Disparity.objects.get(id=id)
            serializer = ProblemSerializer(disparity, many=False)
            message = serializer.data
            status_code = status.HTTP_200_OK
        except Disparity.DoesNotExist:
            message = CustomDoesNotExist("Disparity")
            status_code = status.HTTP_404_NOT_FOUND
        return Response(message, status=status_code)


class DisparityByProblemAPIView(APIView):
    def get(self, request):
        serializer = DisparitySerializer(data=request.data)
        if serializer.is_valid():
            disparities = Disparity.objects.filter(problem_id=request.data['problem']).all()
            serializer = DisparitySerializer(disparities, many=True)
            message = serializer.data
            status_code = status.HTTP_200_OK
        else:
            message = serializer.errors
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(message, status=status_code)


class DisparityByTitleAPIView(APIView):
    def get(self, request):
        serializer = DisparityByTitleSerializer(data=request.data)
        if serializer.is_valid():
            try:
                disparity = Disparity.objects.get(
                    title=request.data['title'],
                    problem_id=request.data['problem'],
                )
                serializer = DisparityByTitleSerializer(disparity, many=False)
                message = serializer.data
                status_code = status.HTTP_200_OK
            except Disparity.DoesNotExist:
                message = CustomDoesNotExist("Disparity")
                status_code = status.HTTP_404_NOT_FOUND
        else:
            message = serializer.errors
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(message, status=status_code)


# Client API -------------------------------------
class ClientAPIView(APIView):
    def get(self, request):
        client = Client.objects.all()
        serializer = ClientSerializer(client, many=True)
        message = serializer.data
        status_code = status.HTTP_200_OK
        return Response(message, status=status_code)

    def post(self, request):
        try:
            client = Client.global_objects.get(phone=request.data['phone'])
            if client.is_deleted == 1:
                client.is_deleted = 0
                client.save()
            serializer = ClientSerializer(client, many=False)
            message = serializer.data
            status_code = status.HTTP_200_OK
        except Client.DoesNotExist:
            serializer = ClientSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                message = serializer.data
                status_code = status.HTTP_201_CREATED
            else:
                message = serializer.errors
                status_code = status.HTTP_400_BAD_REQUEST
        return Response(message, status=status_code)


class ClientDetailAPIView(APIView):
    def get(self, request, id):
        try:
            client = Client.objects.get(id=id)
            serializer = ClientSerializer(client, many=False)
            message = serializer.data
            status_code = status.HTTP_200_OK
        except Client.DoesNotExist:
            message = CustomDoesNotExist("Client")
            status_code = status.HTTP_404_NOT_FOUND
        return Response(message, status=status_code)


class AdminAPIView(APIView):
    def get(self, request):
        admins = Admin.objects.filter(is_staff=1).all()
        serializer = AdminSerializer(admins, many=True)
        message = serializer.data
        status_code = status.HTTP_200_OK
        return Response(message, status=status_code)

    def post(self, request):
        try:
            admin = Admin.objects.get(phone=request.data['phone'])
            message = {"message": "This admin is already exist"}
            status_code = status.HTTP_409_CONFLICT
        except Admin.DoesNotExist:
            serializer = AdminSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                message = serializer.data
                status_code = status.HTTP_200_OK
            else:
                message = serializer.errors()
                status_code = status.HTTP_400_BAD_REQUEST
        return Response(message, status=status_code)


class AdminCheckViolationAPIView(APIView):
    def post(self, request):
        serializer = AdminCheckViolationSerializer(data=request.data)
        if serializer.is_valid():
            violation = Violation.objects.get(id=request.data['violation'])
            if violation.response_admin.tg_id == request.data['tg_id'] and violation.status.id == 2:
                message = "Authorized"
                status_code = status.HTTP_200_OK
            else:
                message = "Unauthorized"
                status_code = status.HTTP_401_UNAUTHORIZED
        else:
            message = serializer.errors
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(message, status=status_code)


# Status
class StatusAPIView(APIView):
    def get(self, request):
        statuses = Status.objects.all()
        serializer = StatusSerailizer(statuses, many=True)
        message = serializer.data
        status_code = status.HTTP_200_OK
        return Response(message, status=status_code)


# Process
class ProcessAPIView(APIView):
    def get(self, request):
        processes = Process.objects.all()
        serializer = ProcessSerializer(processes, many=True)
        message = serializer.data
        status_code = status.HTTP_200_OK
        return Response(message, status=status_code)


# Violation API -------------------------------------
class ViolationView(ModelViewSet):
    serializer_class = ViolationSerializer
    queryset = Violation.objects.all()


class ViolationAPIView(APIView):
    def get(self, request):
        violations = Violation.objects.all()
        serializer_list = []
        for violation in violations:
            serializer_list.append({
                "id": violation.id,
                "client": violation.client,
                "region": violation.region,
                "shop": violation.shop,
                "department": violation.department,
                "problem": violation.problem,
                "disparity": violation.disparity,
                "comment": violation.comment,
                "photo": violation.photo,
                "photo_url": f"{settings.CSRF_TRUSTED_ORIGINS[0]}/media/{violation.photo}",
                "response_admin_id": violation.response_admin_id,
                "response_person_description": violation.response_person_description,
                "status": violation.status,
                "process": violation.process,
                "is_no_violation": violation.is_no_violation,
                "is_active": violation.is_active,
                "created_at": violation.created_at,
            })

        serializer = ViolationAPISerializer(serializer_list, many=True)
        message = serializer.data
        status_code = status.HTTP_200_OK
        return Response(message, status=status_code)

    def post(self, request):
        serializer = ViolationAPISerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = serializer.data
            status_code = status.HTTP_200_OK
        else:
            message = serializer.errors
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(message, status=status_code)


class ViolationDetailAPIView(APIView):
    def get(self, request, id):
        try:
            violation = Violation.objects.get(id=id)
            serializer = ViolationAPISerializer(violation, many=False)
            message = serializer.data
            status_code = status.HTTP_200_OK
        except Violation.DoesNotExist:
            message = CustomDoesNotExist("Violation")
            status_code = status.HTTP_404_NOT_FOUND
        return Response(message, status=status_code)

    def put(self, request, id):
        try:
            violation = Violation.objects.get(id=id)
            serializer = ViolationAPISerializer(violation, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                message = serializer.data
                status_code = status.HTTP_200_OK
            else:
                message = serializer.errors
                status_code = status.HTTP_400_BAD_REQUEST
        except Violation.DoesNotExist:
            message = CustomDoesNotExist("Violation")
            status_code = status.HTTP_404_NOT_FOUND
        return Response(message, status=status_code)


class ViolationDaysView(APIView):
    def get(self, request, days):
        datetime_previous = str(datetime.today() - timedelta(days=days))
        date_previous = datetime_previous.split(" ")[0]

        violations = Violation.objects.filter(created_at__gte=date_previous, is_no_violation=0).all()
        serializer = ViolationSerializer(violations, many=True)
        message = serializer.data
        status_code = status.HTTP_200_OK
        return Response(message, status_code)


# Login
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, phone):
        try:
            admin = Admin.objects.get(phone=phone)
            token = Token.objects.get_or_create(user_id=admin.id)
            serializer_list = {
                "id": admin.id,
                "name": admin.name,
                "phone": admin.phone,
                "token": token[0],
                "is_staff": admin.is_staff,
                "is_superuser": admin.is_superuser,
                "is_active": admin.is_active,
                "created_at": admin.created_at,
            }
            serializer = LoginSerializer(serializer_list, many=False)
            message = serializer.data
            status_code = status.HTTP_200_OK
        except Admin.DoesNotExist:
            message = "Admin does not exist"
            status_code = status.HTTP_404_NOT_FOUND

        return Response(message, status=status_code)


class ExcelAPIView(APIView):

    def get(self, request, month, year):
        wb = Workbook()
        excel = ExcelUtils(year=year, month=month, wb=wb)

        excel.report_market_func()
        excel.report_process_func()
        excel.report_department_func()
        excel.report_attendance_func()
        excel.report_general_func()
        # report_weeks_func()

        if int(month) < 10:
            month = f"0{month}"

        excel_name = f"media/excel/report_data_{month}_{year}.xlsx"
        wb.save(excel_name)

        serializer_dict = {
            "file": f"{settings.CSRF_TRUSTED_ORIGINS[0]}/{excel_name}",
        }
        serializer = ExcelSerializer(serializer_dict, many=False)

        message = serializer.data
        status_code = status.HTTP_200_OK
        return Response(message, status=status_code)
