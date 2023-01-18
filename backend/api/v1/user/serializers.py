from django.db import transaction
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.serializers import (
    JSONWebTokenSerializer as JWTJSONWebTokenSerializer
)


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'uuid',
            'nickname',
            'roles'
        )
        read_only_fields = (
            'username',
            'uuid',
            'nickname',
            'roles'
        )


class RegisterUserSerializer(serializers.ModelSerializer):

    def save(self):
        with transaction.atomic():
            instance = User.objects.create_user(
                self.validated_data['username'],
                self.validated_data['password'],
            )
        return instance

    class Meta:
        model = User
        fields = (
            'username',
            'password',
        )
        extra_kwargs = {
            'password': {'required': True},
            'username': {'required': True},
        }


class JSONWebTokenSerializer(JWTJSONWebTokenSerializer):
    def validate(self, attrs):
        username = attrs.get(self.username_field)
        try:
            u = User.objects.get(**{self.username_field: username})
        except User.DoesNotExist:
            raise ValidationError('账号不存在')
        return super().validate({
            'password': attrs.get('password'),
            self.username_field: getattr(u, self.username_field)
        })