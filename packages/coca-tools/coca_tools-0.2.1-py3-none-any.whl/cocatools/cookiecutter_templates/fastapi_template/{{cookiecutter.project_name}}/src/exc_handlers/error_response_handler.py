# -*- coding: utf-8 -*-
import json

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.exceptions import ErrorResponseException


# for ErrorResponseException
async def error_response_exception_handler(request: Request, exception: ErrorResponseException):
    return JSONResponse(
        status_code=exception.http_status_code,
        content={
            'success': exception.success,
            'data': exception.data,
            'length': exception.length,
            'message': exception.message,
            'code': exception.code,
        },
    )
