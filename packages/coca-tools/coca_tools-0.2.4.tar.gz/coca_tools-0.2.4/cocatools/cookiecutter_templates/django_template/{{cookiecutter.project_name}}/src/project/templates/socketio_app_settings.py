# -*- coding: utf-8 -*-
from typing import List, Union

from .base_settings_mixin import BaseSettingMixin


class AppSocketIoSetting(BaseSettingMixin):
    WS_SERVER_ENABLE: bool = False
    WS_SERVER_ENABLE_DEBUGGING: bool = False
    # ``'*'`` to allow all origins, or to ``[]`` to disable CORS handling, tested
    WS_SERVER_CORS_ORIGINS: Union[str, List] = '*'
    WS_SERVER_MOUNT_LOCATION: str = '/ws'
    WS_SERVER_SOCKETIO_PATH: str = 'socket.io'
    WS_SERVER_KEEP_ALIVE: int = 120
    WS_SERVER_MAX_FILE_SIZE: int = 90 * (10**6)  # bytes  -> 10 Mb
    WS_SERVER_PING_TIMEOUT: int = 5  # s        -> 30 s
    WS_SERVER_PING_INTERVAL: int = 25  # s        -> 30 s

    class Config:
        case_sensitive = True
        validate_assignment = True
