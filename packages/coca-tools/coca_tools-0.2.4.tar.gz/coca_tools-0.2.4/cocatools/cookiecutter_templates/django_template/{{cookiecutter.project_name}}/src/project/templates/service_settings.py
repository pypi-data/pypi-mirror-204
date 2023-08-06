# -*- coding: utf-8 -*-
import logging
import os
from datetime import timezone
from typing import Dict, Optional

from .base_settings_mixin import BaseSettingMixin


class AppServiceSetting(BaseSettingMixin):
    SERVICE_BASE_DIR: Optional[str] = os.getcwd()
    SERVICE_LOG_LEVEL: int = logging.INFO

    # Service time and timezone
    SERVICE_USE_TZ: Optional[bool] = True
    SERVICE_TIMEZONE: Optional[timezone] = timezone.utc

    # Service info
    SERVICE_HOST: Optional[str] = '{{ cookiecutter.host }}'
    SERVICE_PORT: Optional[int] = {{ cookiecutter.port }}
    SERVICE_DOMAIN: Optional[str] = '{{ cookiecutter.domain }}'
    SERVICE_CODE: Optional[str] = 'python-fastapi'

    # Project
    PROJECT_NAME: Optional[str] = '{{ cookiecutter.project_name }}'
    PROJECT_DESCRIPTION: str = '{{ cookiecutter.project_short_description }}'

    # Service proxy
    SERVICE_USE_PROXY: Optional[bool] = False
    SERVICE_PROXY_ADDR: Optional[str] = ''
    SERVICE_NO_PROXY: Optional[str] = ''

    def get_service_info(self) -> Dict:
        return {
            'name': self.PROJECT_NAME,
            'port': self.SERVICE_PORT,
            'code': self.SERVICE_CODE
        }

    class Config:
        case_sensitive = True
        validate_assignment = True
