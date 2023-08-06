# -*- coding: utf-8 -*-
import os
from .teamplates import (
    AppServiceSetting,
    AppSocketIoSetting,
    FastApiAppSetting,
    GunicornSetting,
    DatabaseMongoSetting,
    RedisSetting,
)

SELECTED_ENV_NAME = os.environ.get("APP_ENV_NAME")


class AppSettings(
    AppServiceSetting,
    GunicornSetting,
    DatabaseMongoSetting,
    RedisSetting,
    AppSocketIoSetting,
    FastApiAppSetting,
):
    pass


__env_file_path = AppSettings.get_env_file_path(AppSettings.get_selected_env())
settings = AppSettings(_env_file=__env_file_path)
settings.setup(__env_file_path)
