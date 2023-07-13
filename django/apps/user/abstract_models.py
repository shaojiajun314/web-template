from uuid import uuid4

from django.db import models
from django.utils import timezone
from django.contrib.auth import models as auth_models

from libs.db.models.fields import PhoneField

from .validators import is_username_validator


class UserManager(auth_models.BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(
            username=username,
            is_staff=False,
            is_active=True,
            is_superuser=False,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        u = self.create_user(username, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class AbstractUser(
    auth_models.AbstractBaseUser,
    auth_models.PermissionsMixin,
):
    uuid = models.UUIDField(
        auto_created=True,
        default=uuid4,
        editable=False
    )
    username = models.CharField(
        max_length=16,
        unique=True,
        validators=(is_username_validator, ),
        error_messages={
            'unique': '该账号已经被注册'
        },
    )
    password = models.CharField(
        max_length=128
    )
    nickname = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )
    mobile = PhoneField(
        max_length=11,
        null=True,
        unique=True
    )
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'username'
    objects = UserManager()

    class Meta:
        abstract = True