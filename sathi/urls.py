from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import read

urlpatterns = [
    path('read/', read, name="read"),
]