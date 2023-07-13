from django.urls import path
from django.conf.urls import include

from .v1.routers import get_urls as v1_urls


def get_urls():
    urls = [
        path(r'v1/', include(v1_urls())),
    ]
    return urls
