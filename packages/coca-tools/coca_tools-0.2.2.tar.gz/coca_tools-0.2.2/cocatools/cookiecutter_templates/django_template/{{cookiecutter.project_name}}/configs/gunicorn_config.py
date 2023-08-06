# -*- coding: utf-8 -*-
import json
import multiprocessing
import os
from src.project.env_settings import env_settings  # noqa # isort:skip
from src.project.templates import GunicornSetting


def create_gunicorn_config(settings: GunicornSetting = GunicornSetting()):
    # create gunicorn directory if neccessary
    log_dir = os.path.join(os.getcwd(), 'log', 'gunicorn')
    _worker_tmp_dir = os.path.join(os.getcwd(), 'log', 'gunicorn', 'tmp')
    for i in (log_dir, _worker_tmp_dir):
        if not os.path.isdir(i):
            os.makedirs(i)

    workers_per_core_str = os.getenv("WORKERS_PER_CORE", "1")
    max_workers_str = os.getenv("MAX_WORKERS")
    use_max_workers = None
    if max_workers_str:
        use_max_workers = int(max_workers_str)

    web_concurrency_str = os.getenv("GUNICORN_WORKER_CONCURRENCY", settings.GUNICORN_WORKER_CONCURRENCY)

    host = os.getenv("HOST", settings.GUNICORN_HOST)
    port = os.getenv("PORT", settings.GUNICORN_PORT)
    bind_env = os.getenv("GUNICORN_BIND_PATH", settings.GUNICORN_BIND_PATH)
    use_loglevel = os.getenv("LOG_LEVEL", "info")
    if bind_env:
        use_bind = bind_env
    else:
        use_bind = f"{host}:{port}"

    cores = multiprocessing.cpu_count()
    workers_per_core = float(workers_per_core_str)
    default_web_concurrency = workers_per_core * cores
    if web_concurrency_str:
        web_concurrency = int(web_concurrency_str)
        assert web_concurrency > 0
    else:
        web_concurrency = max(int(default_web_concurrency), 2)
        if use_max_workers:
            web_concurrency = min(web_concurrency, use_max_workers)
    accesslog_var = os.getenv("ACCESS_LOG", os.path.join(log_dir, 'access.log'))
    use_accesslog = accesslog_var or None
    errorlog_var = os.getenv("ERROR_LOG", os.path.join(log_dir, 'error.log'))
    use_errorlog = errorlog_var or None
    graceful_timeout_str = os.getenv("GRACEFUL_TIMEOUT", "120")
    timeout_str = os.getenv("TIMEOUT", "120")
    keepalive_str = os.getenv("KEEP_ALIVE", "120")

    # Gunicorn config variables
    loglevel = use_loglevel
    workers = web_concurrency
    bind = use_bind
    errorlog = use_errorlog
    worker_tmp_dir = _worker_tmp_dir
    accesslog = use_accesslog
    graceful_timeout = int(graceful_timeout_str)
    timeout = int(timeout_str)
    keepalive = int(keepalive_str)
    limit_request_line = 0

    # gunicorn config
    gconfig = {
        "loglevel": loglevel,
        "workers": workers,
        "bind": bind,
        "graceful_timeout": graceful_timeout,
        "timeout": timeout,
        "keepalive": keepalive,
        "errorlog": settings.GUNICORN_ERROR_LOG if settings.GUNICORN_ERROR_LOG else errorlog,
        "accesslog": settings.GUNICORN_ACCESS_LOG if settings.GUNICORN_ACCESS_LOG else accesslog,
        # capture_output = True,        # capture print or other to error log
        'worker_tmp_dir': worker_tmp_dir,
        'limit_request_line': limit_request_line,
        # Additional, non-gunicorn variables
        "workers_per_core": workers_per_core,
        "use_max_workers": use_max_workers,
        "host": host,
        "port": port,
    }
    print(json.dumps(gconfig))
    print('Gunicorn Started with bind ', use_bind)

    return gconfig


gconfig = create_gunicorn_config(env_settings)

locals().update(gconfig)
