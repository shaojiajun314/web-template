from django.urls import path

from .views import (
    RegisterView,
    UserView,
    LoginView,
)

def get_urls():
    urls = [
        path(
            r'login/',
            LoginView.as_view()
        ),
        path(
            r'register/',
            RegisterView.as_view({'post': 'create'})
        ),
        path(
            r'info/',
            UserView.as_view({'get': 'retrieve'})
        ),
    ]
    return urls
