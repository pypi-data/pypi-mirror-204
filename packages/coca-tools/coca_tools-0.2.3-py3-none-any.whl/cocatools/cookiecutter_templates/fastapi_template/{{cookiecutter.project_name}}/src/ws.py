# -*- coding: utf-8 -*-
import logging

from src import constants
from src.utils.app_creators import create_socketio_app

logger = logging.getLogger(constants.CONSOLE_LOGGER)


def initialize_socketio_event_handlers(sio):
    from src.ws_events import ws_event_mapping

    for event_name, event_config in ws_event_mapping.items():
        sio.on(
            event_name,
            event_config.get('handler'),
            event_config.get('namespace'),
        )
        logger.info(f'add socketio event {event_name} -> {event_config}')


sio, sio_app = create_socketio_app()
