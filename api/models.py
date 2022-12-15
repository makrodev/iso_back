from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django_softdelete.models import SoftDeleteModel, SoftDeleteQuerySet
from django.contrib.auth.models import PermissionsMixin
from rest_framework.authtoken.models import Token


class Status(SoftDeleteModel):
    title = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Process(SoftDeleteModel):
    title = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']
        verbose_name = 'Процесс'
        verbose_name_plural = 'Процессы'


class CustomAdminManager(BaseUserManager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model).filter(is_deleted=False)

    def create_token(self, user_id):
        token, is_created = Token.objects.get_or_create(user_id=user_id)
        return token

    def create_superuser(self, phone, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Staff must be assigned to is_staff=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')
        user = self.model(phone=phone, **other_fields)
        user.set_password(password)
        user.save()
        self.create_token(user_id=user.id)
        return user

    def create_is_staff(self, phone, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', False)
        other_fields.setdefault('is_active', True)

        if not phone:
            raise ValueError("You must provide an phone number")

        user = self.model(phone=phone, **other_fields)
        user.set_password(password)
        user.save()
        self.create_token(user_id=user.id)
        return user

    def create_user(self, phone, password, **other_fields):
        if not phone:
            raise ValueError("You must provide an phone number")

        user = self.model(phone=phone, **other_fields)
        user.set_password(password)
        user.save()
        return user


class Admin(SoftDeleteModel, AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True)
    tg_id = models.CharField(max_length=40)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomAdminManager()

    def __str__(self):
        return str(self.phone)

    class Meta:
        ordering = ['id']
        verbose_name = 'администратора'
        verbose_name_plural = 'Администраторы'


class Button(SoftDeleteModel):
    key = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.key

    class Meta:
        ordering = ['id']
        verbose_name = 'Кнопку'
        verbose_name_plural = 'Кнопки'


class Content(SoftDeleteModel):
    key = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.key

    class Meta:
        ordering = ['id']
        verbose_name = 'Контент'
        verbose_name_plural = 'Контенты'


class Region(SoftDeleteModel):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'


class Shop(SoftDeleteModel):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.region}"

    class Meta:
        ordering = ['id']
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'


class Department(SoftDeleteModel):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'


class Problem(SoftDeleteModel):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']
        verbose_name = 'Проблему'
        verbose_name_plural = 'Проблемы'


class Disparity(SoftDeleteModel):
    title = models.CharField(max_length=100)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.problem}"

    class Meta:
        ordering = ['id']
        verbose_name = 'Несоответствие'
        verbose_name_plural = 'Несоответствия'


class Client(SoftDeleteModel):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12, unique=True)
    tg_id = models.CharField(max_length=40)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = 'Клиента'
        verbose_name_plural = 'Клиенты'


class Violation(SoftDeleteModel):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    problem = models.ForeignKey(Problem, on_delete=models.SET_NULL, null=True)
    disparity = models.ForeignKey(Disparity, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(null=True)
    photo = models.FileField(upload_to='uploads/photo/', null=True)
    response_admin = models.ForeignKey("Admin", on_delete=models.SET_NULL, null=True, blank=True)
    response_person_description = models.TextField(null=True, blank=True)
    result_action = models.TextField(null=True, blank=True)
    status = models.ForeignKey("Status", on_delete=models.SET_NULL, null=True, default=1)
    process = models.ForeignKey("Process", on_delete=models.SET_NULL, null=True, blank=True)
    is_no_violation = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.client} - {self.region}"

    class Meta:
        ordering = ['-id']
        verbose_name = 'Нарушение'
        verbose_name_plural = 'Нарушения'
