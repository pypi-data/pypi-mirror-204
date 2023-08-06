# -*- coding: utf-8 -*-
from typing import Optional

from .base_settings_mixin import BaseSettingMixin


class MinIOSetting(BaseSettingMixin):
    MINIO_ENABLE: bool = False
    MINIO_DOMAIN: Optional[str]
    MINIO_HOST: Optional[str] = 'http://172.24.222.114'
    MINIO_PORT: Optional[int] = 9000
    MINIO_ACCESS_KEY: Optional[str]
    MINIO_SECRET_KEY: Optional[str]
    MINIO_API: Optional[str]
    MINIO_PATH: Optional[str] = 'auto'
    MINIO_SECURE: Optional[bool] = False
    MINIO_BUCKET_NAME: Optional[str]
    MINIO_BUCKET_LOCAL: Optional[str] = None
    MINIO_PUBLIC_DOMAIN: Optional[str] = None

    def get_minio_server_url(self) -> str:
        if self.MINIO_DOMAIN:
            return self.MINIO_DOMAIN
        return f'{self.MINIO_HOST}:{self.MINIO_PORT}'
