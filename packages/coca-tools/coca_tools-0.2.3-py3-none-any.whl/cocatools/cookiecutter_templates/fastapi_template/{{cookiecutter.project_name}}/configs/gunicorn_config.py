# -*- coding: utf-8 -*-
from src.settings import settings  # noqa # isort:skip
from core.templates.gunicorn import create_gunicorn_config  # noqa

gconfig = create_gunicorn_config(settings)

locals().update(gconfig)
