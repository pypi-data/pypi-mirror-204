# -*- coding: utf-8 -*-
from typing import Optional

from src import constants  # noqa

from .base_settings_mixin import BaseSettingMixin


class ZaloSetting(BaseSettingMixin):
    ZALO_DOMAIN_VERIFICATION_CODE: Optional[str] = 'super-secret-code'

    ZALO_APP_ID: Optional[str]
    ZALO_APP_SECRET_KEY: Optional[str]

    ZALO_OA_URL: Optional[str] = 'https://oa.zalo.me'
    ZALO_OA_OAUTH_API: Optional[str] = 'https://oauth.zaloapp.com/v4/oa'
    ZALO_OA_OPEN_API: Optional[str] = 'https://openapi.zalo.me/v2.0/oa'
    ZALO_OA_API_GET_FOLLOWERS_URL: Optional[str] = '/getfollowers'
    ZALO_OA_ACCESS_EXPIRED_IN: Optional[int] = 90000
    ZALO_OA_REFRESH_EXPIRED_IN: Optional[int] = 7889238

    ZALO_CHAT_DISTRIBUTION_ONLY_ME: Optional[str] = 'only_me'
    ZALO_CHAT_DISTRIBUTION_RANDOM: Optional[str] = 'random'
    ZALO_CHAT_DISTRIBUTION_ROTATION: Optional[str] = 'rotation'
