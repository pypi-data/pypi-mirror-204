# -*- coding: utf-8 -*-
from typing import Dict, List, Optional, Tuple

from .base_settings_mixin import BaseSettingMixin


class CelerySetting(BaseSettingMixin):
    CELERY_BROKER_REDIS_ENABLE: bool = False
    CELERY_BROKER_REDIS_URL: Optional[str] = None

    CELERY_BROKER_SENTINEL_ENABLE: bool = False
    CELERY_BROKER_SENTINEL_SERVERS: List[Tuple[str, int]] = []  # [("sentinel_servers", port), ...]
    CELERY_BROKER_SENTINEL_NAME: Optional[str] = None
    CELERY_BROKER_SENTINEL_REDIS_DB: Optional[int] = 0
    CELERY_BROKER_SENTINEL_REDIS_PASSWORD: Optional[str] = None

    CELERY_BROKER_RABBITMQ_ENABLE: bool = False
    CELERY_BROKER_RABBITMQ_USERNAME: Optional[str] = None
    CELERY_BROKER_RABBITMQ_PASSWORD: Optional[str] = None
    CELERY_BROKER_RABBITMQ_HOST: Optional[str] = None
    CELERY_BROKER_RABBITMQ_PORT: Optional[str] = None
    CELERY_BROKER_RABBITMQ_VHOST: Optional[str] = None

    def get_celery_broker_url(self) -> str:
        if self.CELERY_BROKER_RABBITMQ_ENABLE:
            auth = ''
            if self.CELERY_BROKER_RABBITMQ_USERNAME and self.CELERY_BROKER_RABBITMQ_PASSWORD:
                auth = f'{self.CELERY_BROKER_RABBITMQ_USERNAME}:{self.CELERY_BROKER_RABBITMQ_PASSWORD}@'
            vhost = ''
            if self.CELERY_BROKER_RABBITMQ_VHOST:
                vhost = f'/{self.CELERY_BROKER_RABBITMQ_VHOST}'
            return f'amqp://{auth}{self.CELERY_BROKER_RABBITMQ_HOST}:{self.CELERY_BROKER_RABBITMQ_PORT}{vhost}'

        if self.CELERY_BROKER_REDIS_ENABLE and self.CELERY_BROKER_REDIS_URL:
            return self.CELERY_BROKER_REDIS_URL

        if self.CELERY_BROKER_SENTINEL_ENABLE:
            sentinel_servers = ''
            for server, port in self.CELERY_BROKER_SENTINEL_SERVERS:
                sentinel_servers += f'sentinel://{server}:{port}/{self.CELERY_BROKER_SENTINEL_REDIS_DB};'
            if sentinel_servers.endswith(';'):
                sentinel_servers = sentinel_servers[:-1]
            return sentinel_servers

        raise ValueError('missing environment for celery configurations')

    def get_celery_broker_transport_options_redis_sentinel(self) -> Dict:
        if not self.CELERY_BROKER_SENTINEL_ENABLE:
            return
        return {
            'master_name': self.CELERY_BROKER_SENTINEL_NAME,
            'sentinel_kwargs': {'password': self.CELERY_BROKER_SENTINEL_REDIS_PASSWORD, 'visibility_timeout': 3600},
        }
