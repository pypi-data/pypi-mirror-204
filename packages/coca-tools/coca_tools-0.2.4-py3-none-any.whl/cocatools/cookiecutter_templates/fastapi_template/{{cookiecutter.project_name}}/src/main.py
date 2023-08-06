# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from src import constants
from src.events import shutdown_events, startup_events
from src.settings import settings

default_page = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    </head>
    <body>
        Hello, welcome to {project_name} {service_name}
    </body>
    </html>
"""

ws_connector_page = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta property="zalo-platform-site-verification" content="zalo_domain_verification_code" />
    </head>

    <body>
    Hello, this is test websocket page
    </body>
    <script
        src="https://cdn.socket.io/4.5.0/socket.io.min.js"
        integrity="sha384-7EyYLQZgWBi67fBtVxw60/OWl1kjsfrPFcaU0pp0nAh+i8FD068QogUvg85Ewy1k"
        crossorigin="anonymous"
    >
        </script>    # noqa
    <script>
        const page_origin = window.location.origin
        const socket = io(page_origin, {path: "/x-service-path/ws/socket.io", transports: ["websocket"]});
        socket.on("connect", () => {console.log(socket.id)});

        socket.on("disconnect", () => {console.log(socket.id)});
    </script>
    </html>
"""

_PROJECT_NAME = '{{cookiecutter.project_name}}'
_PROJECT_DESCRIPTION = '{{cookiecutter.project_short_description}}'
_PROJECT_SLUG = '{{cookiecutter.project_slug}}'


app = FastAPI(
    title=_PROJECT_NAME,
    description=_PROJECT_DESCRIPTION,
    on_startup=startup_events,
    on_shutdown=shutdown_events,
)

# mount static files
app.mount('/static', StaticFiles(directory='static'), name='static')


# home pages
service_home_page = default_page.format(
    project_name=_PROJECT_NAME,
    service_name=_PROJECT_SLUG,
)


@app.get('/', response_class=HTMLResponse)
async def app_root():
    return service_home_page


@app.get('/set_log_level')
async def app_service_set_log_level(name: str, level: int = logging.INFO):
    if level not in (logging.DEBUG, logging.INFO, logging.WARNING, logging.CRITICAL, logging.ERROR):
        return {'success': False}
    if name not in (constants.DEBUG_LOGGER, constants.CONSOLE_LOGGER):
        return {'success': False}
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return {'success': True}


# health-check endpoint


@app.get('/server-info')
async def traefik_heath_check():
    resp = {
        'status': 'running',
        'info': {'name': _PROJECT_NAME, 'port': 8000, 'code': _PROJECT_SLUG},
        'date': datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'
        #  "2022-10-18T04:40:40.207Z"
    }
    return resp


# Api App
if settings.SERVICE_ENABLE_API:
    api_mount_path = settings.SERVICE_API_MOUNT_PATH
    if not api_mount_path.startswith('/'):
        api_mount_path = '/' + api_mount_path
    from src.api import api_app

    app.mount(api_mount_path, api_app)

# Websocket App
if settings.WS_SERVER_ENABLE:
    from src.ws import initialize_socketio_event_handlers, sio, sio_app

    socketio_mount_path = settings.SERVICE_SOCKETIO_MOUNT_PATH
    if not socketio_mount_path.startswith('/'):
        socketio_mount_path = '/' + socketio_mount_path

    if sio_app and sio and initialize_socketio_event_handlers:
        app.mount(socketio_mount_path, sio_app)

        initialize_socketio_event_handlers(sio)

        # add websocket page
        @app.get('/ws_test_page')
        async def ws_test_page():
            _html = ws_connector_page.replace('/x-service-path', '')
            return Response(content=_html)
