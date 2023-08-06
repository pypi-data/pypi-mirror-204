# -*- coding: utf-8 -*-
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from src.settings import settings
from starlette.middleware.sessions import SessionMiddleware

# enable or disable middleware from app.config
# in settings with variables startswith FASTAPI_MIDDLEWARE_ENABLE_xxx
middleware_controller = (
    {
        "enable": settings.FASTAPI_MIDDLEWARE_ENABLE_TrustedHostMiddleware,
        "middleware": Middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.FASTAPI_MIDDLEWARE_TRUSTED_HOST,
            www_redirect=True,
        ),
    },
    {
        "enable": settings.FASTAPI_MIDDLEWARE_ENABLE_CORSMiddleware,
        "middleware": Middleware(
            CORSMiddleware,
            # : typing.Sequence[str]
            allow_origins=settings.FASTAPI_MIDDLEWARE_CORS_ALLOW_ORIGINS,
            # : typing.Sequence[str]
            allow_methods=settings.FASTAPI_MIDDLEWARE_CORS_ALLOW_METHODS,
            # : typing.Sequence[str]
            allow_headers=settings.FASTAPI_MIDDLEWARE_CORS_ALLOW_HEADERES,
            allow_credentials=False,  # : bool
            allow_origin_regex=None,  # : str
            expose_headers=(),  # : typing.Sequence[str]
            max_age=600,  # : int
        ),
    },
    {
        "enable": settings.FASTAPI_MIDDLEWARE_ENABLE_SessionMiddleware,
        "middleware": Middleware(
            SessionMiddleware,
            # : typing.Union[str, Secret]
            secret_key=settings.FASTAPI_SECRET_KEY,
            session_cookie="session",  # : str
            max_age=14 * 24 * 60 * 60,  # : int # 14 days, in seconds
            same_site="lax",  # : str
            https_only=False,  # : bool
        ),
    },
)

# do not change middlewares variable
middlewares = [config.get("middleware") for config in middleware_controller if config.get("enable")]
