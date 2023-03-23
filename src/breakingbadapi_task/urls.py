"""breakingbadapi_task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views import debug
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from helpers.utils import HttpSchemaGenerator


schema_view = get_schema_view(
    openapi.Info(
        title="GiG API",
        default_version="v1",
        description="API Documentation for the GiG API",
        contact=openapi.Contact(email="njoagwuanidavid@gmail.com"),
    ),
    public=True,
    generator_class=HttpSchemaGenerator,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("", debug.default_urlconf),
    path('admin/', admin.site.urls),
       path(
        "docs",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="doc-ui",
    ),
    path("api/v1/", include("breaking_bad.urls"))
]
