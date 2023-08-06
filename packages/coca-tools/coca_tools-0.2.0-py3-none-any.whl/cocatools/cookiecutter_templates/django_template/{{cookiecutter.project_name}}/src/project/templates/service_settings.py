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

    {% if cookiecutter.enable_api_app == 'yes' %}
    SERVICE_ENABLE_API: bool = True
    {% else %}
    SERVICE_ENABLE_API: bool = False
    {% endif %}
    SERVICE_API_MOUNT_PATH: Optional[str] = '{{ cookiecutter.api_app_mount_path }}'


    {% if cookiecutter.enable_ws_app == 'yes' %}
    SERVICE_SOCKETIO_ENABLE: bool = True
    {% else %}
    SERVICE_SOCKETIO_ENABLE: bool = False
    {% endif %}
    SERVICE_SOCKETIO_MOUNT_PATH: Optional[str] = '{{ cookiecutter.ws_app_mount_path }}'


    def get_service_info(self) -> Dict:
        return {
            'name': self.PROJECT_NAME,
            'port': self.SERVICE_PORT,
            'code': self.SERVICE_CODE
        }

    class Config:
        case_sensitive = True
        validate_assignment = True
