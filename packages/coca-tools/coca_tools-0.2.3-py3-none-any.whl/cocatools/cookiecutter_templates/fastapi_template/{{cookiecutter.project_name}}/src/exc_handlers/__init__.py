# -*- coding: utf-8 -*-
from fastapi.exceptions import RequestValidationError
from src.exceptions import ErrorResponseException

from .error_response_handler import error_response_exception_handler
from .request_validation_error_handler import request_validation_error_exception_handler

custom_exc_handlers = {
    ErrorResponseException: error_response_exception_handler,
    RequestValidationError: request_validation_error_exception_handler,
}
