# -*- coding: utf-8 -*-
import json

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


# for RequestValidationError
async def request_validation_error_exception_handler(request: Request, exception: RequestValidationError):
    details = json.loads(exception.json())[0]
    err_msg = f"{details.get('loc')[-1]} - {details.get('msg')}"
    return JSONResponse(
        status_code=200,
        content={
            'success': False,
            'data': None,
            'length': 0,
            'message': err_msg,
            'code': 4000100,
        },
    )
