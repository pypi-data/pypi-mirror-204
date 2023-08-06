# -*- coding: utf-8 -*-
from .client_events import example_client_event      # noqa
from .server_events import example_server_event      # noqa

ws_event_mapping = {
    #
    #   Websocket Server
    # '*': {'handler': all_event, 'namespace': None},
    "example_client_event": {"handler": example_client_event, "namespace": None},
    'example_server_event': {'handler': example_server_event, 'namespace': None},
}
