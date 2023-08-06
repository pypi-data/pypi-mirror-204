# -*- coding: utf-8 -*-
from typing import List, Optional

from .base_settings_mixin import BaseSettingMixin


class FastApiAppSetting(BaseSettingMixin):
    FASTAPI_DEBUG: bool = False
    FASTAPI_RELOAD: bool = False
    FASTAPI_SECRET_KEY: Optional[str] = "None"
    FASTAPI_OPEN_API_URL: Optional[str] = None  # "/openapi.json"
    FASTAPI_DOCS_URL: Optional[str] = None  # "/docs"
    FASTAPI_REDOC_URL: Optional[str] = None  # "/redoc"

    # -----------------fastapi middleware-----------------
    FASTAPI_MIDDLEWARE_ENABLE_BruteForceDefenderMiddleware: bool = False
    FASTAPI_MIDDLEWARE_ENABLE_IpProtectionMiddleware: bool = False
    FASTAPI_MIDDLEWARE_ENABLE_TrustedHostMiddleware: bool = False
    FASTAPI_MIDDLEWARE_ENABLE_CORSMiddleware: bool = True
    FASTAPI_MIDDLEWARE_ENABLE_SessionMiddleware: bool = False

    FASTAPI_MIDDLEWARE_TRUSTED_HOST: List[str] = ["localhost", "127.0.0.1"]
    FASTAPI_MIDDLEWARE_LOCAL_IPS: List[str] = ["127.0.0.1", "localhost"]
    FASTAPI_MIDDLEWARE_ADMIN_IPS: List[str] = ["172.30.12.137", "172.30.12.138"]

    FASTAPI_MIDDLEWARE_CORS_ALLOW_ORIGINS: List[str] = ["*"]
    FASTAPI_MIDDLEWARE_CORS_ALLOW_METHODS: List[str] = ["*"]
    FASTAPI_MIDDLEWARE_CORS_ALLOW_HEADERES: List[str] = ["*"]
    # -----------------end-----------------
