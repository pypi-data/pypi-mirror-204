# -*- coding: utf-8 -*-
from src.utils.base_model import CustomBaseModel


class GetInfoRequest(CustomBaseModel):
    user_id: str
