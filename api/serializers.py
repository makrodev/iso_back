import requests
from rest_framework import serializers

from django.contrib.auth.models import User

from main import settings
from .models import *
from .helpers import *


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
            # "result_action",
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
            # "result_action",
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
        instance = ViolationHelpers.update(self, instance=instance, validated_data=validated_data)

        try:
            if validated_data['status'].pk == 2:
                ViolationHelpers.send_bot_violation_message(self, instance=instance)
        except KeyError:
            pass

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
