# -*- coding: utf-8 -*-
# flake8: noqa
from typing import Optional

from src import constants

from .base_settings_mixin import BaseSettingMixin


class ExampleSetting(BaseSettingMixin):
    EXAMPLE_FB_FANPAGE_ID: Optional[str] = None
    EXAMPLE_FB_FANPAGE_ACCESS_TOKEN: Optional[str] = None
    EXAMPLE_FB_RECIPIENT_ID: Optional[str] = None

    EXAMPLE_ZL_OA_ACCESS_TOKEN: Optional[str] = None
    EXAMPLE_ZL_OA_REFRESH_TOKEN: Optional[str] = None
    EXAMPLE_ZL_APP_ID: Optional[str] = None
    EXAMPLE_ZL_APP_SECRET: Optional[str] = None
