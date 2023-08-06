# -*- coding: utf-8 -*-
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

# from src.chat.api.facebook_auth_view import FacebookViewSet


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


# router.register("users", UserViewSet)
# router.register("users", UserViewSet)


app_name = 'api'
urlpatterns = router.urls
