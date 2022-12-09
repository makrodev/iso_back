from django.contrib import admin
from .models import *


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
    ]


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'region',
    ]
    list_filter = ["region"]


@admin.register(Button)
class ButtonAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "key",
        "title",
    ]


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "key",
        "title",
    ]


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
    ]


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
    ]


@admin.register(Disparity)
class DisparityAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "problem",
    ]
    list_filter = ["problem"]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "phone",
        "tg_id",
        "status",
        "created_at",
        "updated_at",
    ]


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "phone",
        "name",
        "is_staff",
        "is_superuser",
        "is_active",
        "created_at",
        "updated_at",
    ]


@admin.register(Violation)
class ViolationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "client",
        "region",
        "shop",
        "department",
        "problem",
        "disparity",
        "comment",
        "photo",
        "is_no_violation",
        "is_active",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "region",
        "shop",
        "department",
        "problem",
        "disparity",
        "is_active",
    ]


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
    ]


