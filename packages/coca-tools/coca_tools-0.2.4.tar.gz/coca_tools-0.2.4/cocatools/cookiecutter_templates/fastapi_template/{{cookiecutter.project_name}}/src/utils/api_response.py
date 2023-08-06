# -*- coding: utf-8 -*-
from typing import Any, List

from .base_model import CustomBaseModel


class ApiResponse(CustomBaseModel):
    success: bool = True
    data: List[Any] = []
    length: int = 0
    message: str = ''
    code: int = 0

    def valid(self):
        if self.data and isinstance(
            self.data(
                list,
                tuple,
            )
        ):
            self.length = len(self.data)
