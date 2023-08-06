# -*- coding: utf-8 -*-
import os

from .templates import (
    AppServiceSetting,
    CelerySetting,
    DjangoSetting,
    ElasticseaerchSetting,
    FacebookSetting,
    GunicornSetting,
    MinIOSetting,
    RedisSetting,
    ZaloSetting,
)

SELECTED_ENV_NAME = os.environ.get('APP_ENV_NAME')


class EnvironmentSettings(
    AppServiceSetting,
    GunicornSetting,
    RedisSetting,
    DjangoSetting,
    CelerySetting,
    FacebookSetting,
    ZaloSetting,
    MinIOSetting,
    ElasticseaerchSetting,
):
    pass


# Even when using a dotenv file, pydantic will still read environment variables as well as the dotenv file,
# environment variables will always take priority over values loaded from a dotenv file.
__env_file_path = EnvironmentSettings.get_env_file_path(EnvironmentSettings.get_selected_env())
env_settings = EnvironmentSettings(_env_file=__env_file_path)
env_settings.setup(__env_file_path)
