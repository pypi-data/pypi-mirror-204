# -*- coding: utf-8 -*-`
from datetime import datetime
from typing import Callable, List, Optional, Tuple

from fastapi import APIRouter, FastAPI
from fastapi.middleware import Middleware
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from socketio import ASGIApp, AsyncServer

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
    ></script>    # noqa
    <script>
        const page_origin = window.location.origin
        const socket = io(page_origin, {path: "/x-service-path/ws/socket.io", transports: ["websocket"]});
        socket.on("connect", () => {console.log(socket.id)});

        socket.on("disconnect", () => {console.log(socket.id)});
    </script>
    </html>
"""


def create_api_app(
    router: APIRouter = None,
    middlewares: List[Middleware] = [],
    docs_url: str = '/docs',
    redoc_url: str = '/redoc',
    openapi_url: str = '/openapi.json',
):
    api_app = FastAPI(
        middleware=middlewares,
        docs_url=docs_url,
        redoc_url=redoc_url,
        openapi_url=openapi_url
    )
    if router and isinstance(router, APIRouter):
        api_app.include_router(router)

    return api_app


def create_socketio_app(
    socketio_path: str = 'socket.io',
    # ``'*'`` to allow all origins, or to ``[]`` to disable CORS handling, tested,
    cors_allowed_origins: str | List[str] = '*',
    enable_debug: bool = False,
    enable_engineio_debug: bool = False,
    max_http_buffer_size: int = 10 * (10**6),  # bytes  -> 10 Mb,
    ping_timeout: int = 5,      # seconds
    ping_interval: int = 25     # seconds
) -> Tuple[AsyncServer, ASGIApp]:
    sio = AsyncServer(
        async_mode="asgi",
        cors_allowed_origins=cors_allowed_origins,
        logger=enable_debug,  # for debbuging
        engineio_logger=enable_engineio_debug,  # for debugging
        max_http_buffer_size=max_http_buffer_size,  # for upload file size limitation
        ping_timeout=ping_timeout,
        ping_interval=ping_interval,
    )
    sio_app = ASGIApp(socketio_server=sio, socketio_path=socketio_path)
    return sio, sio_app


def create_fastapi_app(
    enable_api: bool = True,
    api_router: APIRouter = None,
    api_mount_path: Optional[str] = None,
    title: str = "FastAPI",
    description: str = "Description",
    middlewares: List[Middleware] = [],
    startup_events: List[Callable] = [],
    shutdown_events: List[Callable] = [],
    docs_url: str = '/docs',
    redoc_url: str = '/redoc',
    openapi_url: str = '/openapi.json',

    enable_ws: bool = False,
    socketio_ins: AsyncServer = None,
    socketio_app: ASGIApp = None,
    socketio_mount_path: Optional[str] = None,
    socketio_extra_mount_path: Optional[str] = None,
    ws_event_handlers_initializer: Callable = None,

    project_name: str = 'project-x',
    service_path: str = 'service-x',
    service_port: int = '8000',
    service_code: str = 'service-x 8000',

    **kwargs
):
    app = FastAPI(
        title=title,
        description=description,
        docs_url=docs_url,
        redoc_url=redoc_url,
        openapi_url=openapi_url,
        on_startup=startup_events,
        on_shutdown=shutdown_events,
    )

    # mount static files
    app.mount('/statics', StaticFiles(directory="statics"), name='statics')

    # home pages
    service_home_page = default_page.format(
        project_name=project_name,
        service_name=service_path,
        zalo_domain_verification_code=kwargs.get(
            'zalo_domain_verification_code')
    )

    @app.get("/", response_class=HTMLResponse)
    async def app_root():
        return service_home_page

    @app.get(f"/{service_path}", response_class=HTMLResponse)
    async def app_service_root():
        return service_home_page

    # health-check endpoint
    @app.get("/server-info")
    async def traefik_heath_check():
        resp = {
            "status": "running",
            "info": {
                "name": service_path,
                "port": service_port,
                "code": service_code
            },
            "date": datetime.utcnow().isoformat(timespec='milliseconds') + "Z"
            #  "2022-10-18T04:40:40.207Z"
        }
        return resp

    # Api App
    if enable_api:
        if not api_mount_path:
            api_mount_path = f'{service_path}/api'
        if not api_mount_path.startswith('/'):
            api_mount_path = '/' + api_mount_path
        api_app = create_api_app(
            api_router, middlewares, docs_url, redoc_url, openapi_url)
        app.mount(api_mount_path, api_app)

    # Websocket App
    if enable_ws:
        if not callable(ws_event_handlers_initializer):
            raise ValueError(
                'expected ws_event_handlers_initializer is a callable object')

        if not socketio_mount_path:
            socketio_mount_path = f'{service_path}/ws'
        if not socketio_mount_path.startswith('/'):
            socketio_mount_path = '/' + socketio_mount_path

        if socketio_ins and socketio_app and ws_event_handlers_initializer:
            app.mount(socketio_mount_path, socketio_app)

            # for extra path, in SOP, it provide fchat public path without authentication
            if socketio_extra_mount_path:
                if not socketio_extra_mount_path.startswith('/'):
                    socketio_extra_mount_path = '/' + socketio_extra_mount_path
                app.mount(socketio_extra_mount_path, socketio_app)

            ws_event_handlers_initializer(socketio_ins)

            # add websocket page
            @app.get("/ws_test_page")
            async def ws_test_page():
                _html = ws_connector_page.replace(
                    'x-service-path',
                    service_path
                ).replace(
                    'zalo_domain_verification_code',
                    kwargs.get('zalo_domain_verification_code') or ""
                )
                return Response(content=_html)

    return app, {
        'app': app,
        'api_app': api_app if 'api_app' in locals() else None,
        'socketio_ins': socketio_ins,
        'socketio_app': socketio_app
    }
