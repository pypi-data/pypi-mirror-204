# -*- coding: utf-8 -*-
from typing import Optional

from .base_settings_mixin import BaseSettingMixin


class FacebookSetting(BaseSettingMixin):
    FACEBOOK_VERIFICATION_HUB_MODE: Optional[str] = 'subscribe'
    FACEBOOK_VERIFICATION_HUB_TOKEN: Optional[str] = 'Jw!1*wM32qNt'

    FACEBOOK_APP_ID: Optional[str] = None
    FACEBOOK_APP_SECRET: Optional[str] = None
    FACEBOOK_DOMAIN: Optional[str] = "https://facebook.com"
    FACEBOOK_GRAPH_API_DOMAIN: Optional[str] = "https://graph.facebook.com"
    FACEBOOK_GRAPH_API_VERSION: Optional[str] = "v14.0"
    FACEBOOK_GRAPH_API_SEND_MESSAGE: Optional[str] = 'https://graph.facebook.com/me/messages'

    FACEBOOK_GET_PAGE_URL_FIELDS: Optional[str] = 'picture,link'
    FACEBOOK_SUBSCRIBE_PAGE_URL_FIELDS: Optional[str] = 'messages,messaging_postbacks,feed,inbox_labels,message_reads'
    FACEBOOK_USER_PROFILE_FIELDS: Optional[str] = 'first_name,last_name,profile_pic,gender,name'
