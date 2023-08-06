# -*- coding: utf-8 -*-
from .base_settings_mixin import BaseSettingMixin


class DatabaseMongoSetting(BaseSettingMixin):
    DB_MONGO_ENABLE: bool = False
    DB_MONGO_HOST: str = 'localhost'
    DB_MONGO_PORT: int = 27017
    DB_MONGO_USERNAME: str = 'default'
    DB_MONGO_PASSWORD: str = 'default'
    DB_MONGO_DB_NAME: str = 'default'

    def get_mongo_uri(self) -> str:
        auth = ''
        if self.DB_MONGO_USERNAME and self.DB_MONGO_PASSWORD:
            auth = f'{self.DB_MONGO_DB_NAME}:{self.DB_MONGO_PASSWORD}@'
        return f'mongodb://{auth}{self.DB_MONGO_HOST}:{self.DB_MONGO_PORT}'
