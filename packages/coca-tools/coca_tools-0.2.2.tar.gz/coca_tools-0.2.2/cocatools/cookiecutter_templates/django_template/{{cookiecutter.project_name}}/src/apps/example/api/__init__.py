# -*- coding: utf-8 -*-
from django.urls import path

from . import example


urlpatterns = [
    path('unauth_example/', example.get_example_unauthenticated_api, name='unauth_example'),
    path('auth_example/', example.get_example_authenticated_api, name='auth_example'),
]
