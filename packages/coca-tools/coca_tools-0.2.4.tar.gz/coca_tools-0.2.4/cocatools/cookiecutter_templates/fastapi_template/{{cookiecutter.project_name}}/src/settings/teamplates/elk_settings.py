# -*- coding: utf-8 -*-
from typing import Optional

from .base_settings_mixin import BaseSettingMixin


class ElasticseaerchSetting(BaseSettingMixin):

    ELASTIC_SEARCH_URL: Optional[str] = None
    ELASTIC_KIBANA_URL: Optional[str] = None

    ELASTIC_USER: Optional[str] = None
    ELASTIC_PASSWORD: Optional[str] = None

    ELASTIC_JOURNEY_LOGSTASH: Optional[str] = None
