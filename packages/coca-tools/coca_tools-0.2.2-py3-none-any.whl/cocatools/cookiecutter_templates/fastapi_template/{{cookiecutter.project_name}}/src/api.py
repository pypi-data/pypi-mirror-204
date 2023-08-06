# -*- coding: utf-8 -*-
from src.exc_handlers import custom_exc_handlers
from src.middlewares import middlewares
from src.routers import api_router
from src.utils.app_creators import create_api_app

api_app = create_api_app(api_router, middlewares)


# add customs exception handlers
if custom_exc_handlers and isinstance(custom_exc_handlers, dict):
    for exc_class, exc_handler in custom_exc_handlers.items():
        if issubclass(exc_class, Exception) and callable(exc_handler):
            api_app.add_exception_handler(exc_class, exc_handler)
