# -*- coding: utf-8 -*-
from typing import List, Optional, Tuple

from .base_settings_mixin import BaseSettingMixin


class RedisSetting(BaseSettingMixin):
    REDIS_ENABLE: bool = False
    REDIS_HOST: Optional[str] = 'localhost'
    REDIS_PORT: Optional[int] = 6379
    REDIS_DB: Optional[int] = 0
    REDIS_AUTH: Optional[str] = None

    REDIS_SENTINEL_ENABLE: bool = False
    REDIS_SENTINEL_SERVERS: List[Tuple[str, int]] = []
    REDIS_SENTINEL_NAME: Optional[str] = None
    REDIS_SENTINEL_REDIS_DB: Optional[int] = 0
    REDIS_SENTINEL_REDIS_PASSWORD: Optional[str] = None

    def get_redis_server_url(self) -> str:
        return f'redis://:{self.REDIS_AUTH}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}'

    def get_redis_sentinel_urls(self) -> str:
        # return self.REDIS_SENTINEL_URLS
        pass
