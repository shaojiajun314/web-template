from datetime import datetime

from libs.drf.mixins import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.views import ObtainJSONWebToken


from rest_framework_jwt.settings import api_settings
from django.db.models import Q

from permissions import IsLogin
from .serializers import  (
    UserSerializer,
    RegisterUserSerializer,
    JSONWebTokenSerializer,
)

from django.contrib.auth import get_user_model
User = get_user_model()


jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class RegisterView(
    GenericViewSet,
    CreateModelMixin
    ):
    serializer_class = RegisterUserSerializer


class UserView(
    GenericViewSet,
    RetrieveModelMixin
    ):
    serializer_class = UserSerializer
    permission_classes = [IsLogin]
    def get_object(self):
        return self.request.user


class LoginView(ObtainJSONWebToken):
    serializer_class = JSONWebTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(
                {
                    'code': 0,
                    'message': 'success',
                    'data': response_data,
                },
            )
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=False)
            return response
        return Response(
            {
                'code': 1,
                'message': '账号或者密码错误',
            },
            status=status.HTTP_200_OK
        )