# """Web URL Configuration

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/4.1/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]


"""industry_chain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls import include

from api.routers import get_urls as api_urls

urlpatterns = [
    path(r'api/', include(api_urls())),
]

if settings.DEBUG:
    # swagger 文档部分
    from libs.swagger.views import get_schema_view
    from drf_yasg import openapi
    from rest_framework import permissions
    from rest_framework.documentation import include_docs_urls
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    schema_view = get_schema_view(
        openapi.Info(
            title="Swagger Doc",
            default_version='v1',
            description="description",
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )
    urlpatterns += [
        path('admin/', admin.site.urls),  # admin
        # swagger文档
        path(r'swagger(?P<format>\.json|\.yaml)',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path(r'swagger/', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
        path(r'redoc/', schema_view.with_ui('redoc',
            cache_timeout=0), name='schema-redoc'),
    ]
