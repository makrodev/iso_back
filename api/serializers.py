import requests
from rest_framework import serializers

from django.contrib.auth.models import User

from main import settings
from .models import *


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = [
            "id",
            "phone",
            "name",
            "is_staff",
            "is_superuser",
            "is_active",
            "created_at",
        ]

    def create(self, validated_data):
        admin = Admin.objects.create(**validated_data)
        admin.set_password("admin")
        admin.is_active = 1
        admin.is_staff = 1
        admin.save()
        return admin


class AdminCheckViolationSerializer(serializers.Serializer):
    violation = serializers.IntegerField(min_value=1, max_value=400000000000)
    tg_id = serializers.IntegerField(min_value=1, max_value=400000000000)


# Button
class ButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Button
        fields = ("id", "key", "title")


# Content
class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ("id", "key", "title")


# Region
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ("id", "name")


class RegionByNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ("id", "name")


# Shop
class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = [
            "id",
            "name",
            "region",
        ]


class ShopByPropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = [
            "id",
            "name",
            "region",
        ]


# Department
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("id", "title")


class DepartmentByTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("id", "title")
        extra_kwargs = {
            'id': {'read_only': True}
        }


# Problem
class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ("id", "title")


class ProblemByTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("id", "title")
        extra_kwargs = {
            'id': {'read_only': True}
        }


# Disparity
class DisparitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Disparity
        fields = ("id", "title", "problem")
        extra_kwargs = {
            'title': {'read_only': True}
        }


class DisparityByTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disparity
        fields = ("id", "title", "problem")


# Client
class ClientSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=255)
    class Meta:
        model = Client
        fields = (
            "id",
            "name",
            "phone",
            "tg_id",
        )

    def create(self, validated_data):
        client = Client.objects.create(**validated_data)
        return client


# Status
class StatusSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = [
            "id",
            "title",
        ]


# Process
class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = (
            "id",
            "title",
        )


# Violation
class ViolationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Violation
        fields = (
            "id",
            "client",
            "region",
            "shop",
            "department",
            "problem",
            "disparity",
            "comment",
            "photo",
            "response_admin",
            "response_person_description",
            "status",
            "process",
            "is_no_violation",
            "is_active",
            "created_at",
        )


class ViolationAPISerializer(serializers.ModelSerializer):
    photo_url = serializers.CharField(max_length=255, read_only=True)
    class Meta:
        model = Violation
        fields = [
            "id",
            "client",
            "region",
            "shop",
            "department",
            "problem",
            "disparity",
            "comment",
            "photo",
            "photo_url",
            "response_admin",
            "response_person_description",
            "status",
            "process",
            "is_no_violation",
            "is_active",
            "created_at",
        ]

        read_only_fields = [
            'id',
            'created_at',
        ]

    def create(self, validated_data):
        violation = Violation.objects.create(**validated_data)
        return violation

    def update(self, instance, validated_data):
        instance.client = validated_data.get('client', instance.client)
        instance.region = validated_data.get('region', instance.region)
        instance.shop = validated_data.get('shop', instance.shop)
        instance.department = validated_data.get('department', instance.department)
        instance.problem = validated_data.get('problem', instance.problem)
        instance.disparity = validated_data.get('disparity', instance.disparity)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.response_admin = validated_data.get('response_admin', instance.response_admin)
        instance.response_person_description = validated_data.get('response_person_description', instance.response_person_description)
        instance.status = validated_data.get('status', instance.status)
        instance.process = validated_data.get('process', instance.process)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()

        if validated_data['status'].pk == 2:
            # BOT SETTINGS
            command_violation = Content.objects.get(key="commands_violation")

            bot_message = f"Вам пришло новое сообщение о нарушении\nНажмите сюда {command_violation.title}{instance.pk} чтобы ответить на него"

            base_url = f'{settings.TELEGRAM_DOMAIN}/bot{settings.BOT_KEY}/sendMessage?chat_id={instance.response_admin.tg_id}&text={bot_message}'
            requests.get(url=base_url)

        return instance


class ExcelSerializer(serializers.Serializer):
    file = serializers.CharField(max_length=255)


class LoginSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=0, max_value=40000000000)
    name = serializers.CharField(max_length=12)
    phone = serializers.CharField(max_length=12)
    token = serializers.CharField(max_length=200)
    is_staff = serializers.IntegerField(min_value=0, max_value=1)
    is_superuser = serializers.IntegerField(min_value=0, max_value=1)
    is_active = serializers.IntegerField(min_value=0, max_value=1)
    created_at = serializers.CharField(max_length=200)
