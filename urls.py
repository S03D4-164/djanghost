from django.contrib import admin
from django.urls import path
from .docker_ghost import ghost_api

urlpatterns = [
    path('ghost/', ghost_api),
]
