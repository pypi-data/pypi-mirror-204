# -*- coding: utf-8 -*-
from django.urls import include, path

url_djviews = []


urlpatterns = url_djviews + [path('api/', include('src.apps.example.api'))]
