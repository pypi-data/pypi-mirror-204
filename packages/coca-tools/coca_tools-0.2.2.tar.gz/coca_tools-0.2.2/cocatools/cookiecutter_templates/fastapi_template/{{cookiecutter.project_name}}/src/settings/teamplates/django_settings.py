# -*- coding: utf-8 -*-
from typing import Dict, List, Optional, Tuple

from .base_settings_mixin import BaseSettingMixin


class DjangoSetting(BaseSettingMixin):

    DJANGO_DEBUG: bool = False
    DJANGO_SECRET_KEY: Optional[str] = None
    DJANGO_SETTINGS_IMPORT: Optional[str] = 'src.dj_project.settings.local'

    DJANGO_USE_TZ: bool = False
    DJANGO_TIMEZONE: str = 'UTC'

    DJANGO_STATIC_URL: str = 'static/'
    DJANGO_MEDIA_URL: str = 'media/'
    DJANGO_ADMIN_URL: str = 'admin/'

    DJANGO_ALLOWED_HOSTS: List[str] = ['*']

    DJANGO_CORS_ALLOWED_ORIGINS: List[str] = []
    DJANGO_CORS_ALLOWED_METHOD: List[str] = []

    # debug apps, will be append to INSTALLED_APPS
    DJANGO_DEBUG_APPS: List[str] = []

    # django app utilities
    DJANGO_ALLOW_ASYNC_UNSAFE: bool = False
    DJANGO_EMAIL_BACKEND: str = 'django.core.mail.backends.smtp.EmailBackend'
    DJANGO_EMAIL_HOSTS: str = 'mailhog'
    DJANGO_EMAIL_PORT: int = 1025
    DJANGO_DEFAULT_FROM_EMAIL: str = "chat_service <noreply@portal.sop-fpt.online>"

    # django all-auth
    DJANGO_ACCOUNT_ALLOW_REGISTRATION: bool = True
    DJANGO_ACCOUNT_AUTHENTICATION_METHOD: str = 'username'

    #
    DJANGO_SECURE_PROXY_SSL_HEADER: Tuple[str, str] = ("HTTP_X_FORWARDED_PROTO", "https",)
    DJANGO_SECURE_SSL_REDIRECT: bool = False
    DJANGO_SESSION_COOKIE_SECURE: bool = True
    DJANGO_CSRF_COOKIE_SECURE: bool = True
    DJANGO_SECURE_HSTS_SECONDS: int = 60
    DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS: bool = True
    DJANGO_SECURE_HSTS_PRELOAD: bool = True
    DJANGO_SECURE_CONTENT_TYPE_NOSNIFF: bool = True

    # Django Postgresql
    DJANGO_DB_MASTER_ENABLE: bool = True
    DJANGO_DB_MASTER_NAME: Optional[str] = None
    DJANGO_DB_MASTER_USERNAME: Optional[str] = None
    DJANGO_DB_MASTER_PASSWORD: Optional[str] = None
    DJANGO_DB_MASTER_HOST: Optional[str] = None
    DJANGO_DB_MASTER_PORT: Optional[str] = None

    # Django Database
    DJANGO_DB_MASTER_ENABLE: bool = True
    DJANGO_DB_MASTER_ENGINE: Optional[str] = None
    DJANGO_DB_MASTER_NAME: Optional[str] = None
    DJANGO_DB_MASTER_USERNAME: Optional[str] = None
    DJANGO_DB_MASTER_PASSWORD: Optional[str] = None
    DJANGO_DB_MASTER_HOST: Optional[str] = None
    DJANGO_DB_MASTER_PORT: Optional[str] = None

    DJANGO_DB_REPLICA_01_ENABLE: bool = False
    DJANGO_DB_REPLICA_01_ENGINE: Optional[str] = None
    DJANGO_DB_REPLICA_01_NAME: Optional[str] = None
    DJANGO_DB_REPLICA_01_USERNAME: Optional[str] = None
    DJANGO_DB_REPLICA_01_PASSWORD: Optional[str] = None
    DJANGO_DB_REPLICA_01_HOST: Optional[str] = None
    DJANGO_DB_REPLICA_01_PORT: Optional[str] = None

    DJANGO_DB_REPLICA_02_ENABLE: bool = False
    DJANGO_DB_REPLICA_02_NAME: Optional[str] = None
    DJANGO_DB_REPLICA_02_ENGINE: Optional[str] = None
    DJANGO_DB_REPLICA_02_USERNAME: Optional[str] = None
    DJANGO_DB_REPLICA_02_PASSWORD: Optional[str] = None
    DJANGO_DB_REPLICA_02_HOST: Optional[str] = None
    DJANGO_DB_REPLICA_02_PORT: Optional[str] = None

    def create_django_databases(self) -> Dict:
        dbs = {}
        # roles = ('MASTER', 'REPLICA_01', 'REPLICA_02')
        for role in ('MASTER', 'REPLICA_01', 'REPLICA_02'):
            attr_enable = f'DJANGO_DB_{role}_ENABLE'
            if not getattr(self, attr_enable):
                continue
            attr_engine = f'DJANGO_DB_{role}_ENGINE'
            attr_name = f'DJANGO_DB_{role}_NAME'
            attr_username = f'DJANGO_DB_{role}_USERNAME'
            attr_password = f'DJANGO_DB_{role}_PASSWORD'
            attr_host = f'DJANGO_DB_{role}_HOST'
            attr_port = f'DJANGO_DB_{role}_PORT'

            dbs.update({
                'default' if role == 'MASTER' else role: {
                    'ENGINE': getattr(self, attr_engine),
                    'NAME': getattr(self, attr_name),
                    'USER': getattr(self, attr_username),
                    'PASSWORD': getattr(self, attr_password),
                    'HOST': getattr(self, attr_host),
                    'PORT': getattr(self, attr_port),
                    'ATOMIC_REQUESTS': True,
                    'CONN_MAX_AGE': 60
                }
            })
        # print('created database', dbs)
        return dbs
