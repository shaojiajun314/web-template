from django.urls import path
from django.conf.urls import include

from .user.routers import get_urls as user_urls


def get_urls():
    urls = [
        path(r'user/', include(user_urls())),
    ]
    return urls
