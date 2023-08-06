# -*- coding: utf-8 -*-
from typing import Any, List


class ErrorResponseException(Exception):
    def __init__(
        self, message: str, success: bool = False, data: List[Any] = [], code: int = 200, http_status_code: int = 200
    ):
        self.message = message
        self.success = success
        self.data = data
        self.code = code
        self.length = len(self.data) if isinstance(self.data, (tuple, list)) else 0
        self.http_status_code = http_status_code

    def dict(self):
        return {
            'success': self.success,
            'data': self.data,
            'length': self.length,
            'message': self.message,
            'code': self.code,
        }
