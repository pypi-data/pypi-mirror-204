# -*- coding: utf-8 -*-
from typing import List, Optional, Tuple

from .base_settings_mixin import BaseSettingMixin


class NatsSetting(BaseSettingMixin):
    NATS_HOST: Optional[str] = 'localhost'
    NATS_PORT: Optional[int] = 4222
    NATS_USERNAME: Optional[str] = None
    NATS_PASSWORD: Optional[str] = None
    NATS_CLUSTER_SERVERS: List[Tuple[str, int]] = []

    def get_nats_auth(self):
        auth = ''
        if self.NATS_USERNAME and self.NATS_PASSWORD:
            auth = f'{self.NATS_USERNAME}:{self.NATS_PASSWORD}@'
        return auth

    def get_nats_server_url(self) -> str:
        return f"nats://{self.get_nats_auth()}{self.NATS_HOST}:{self.NATS_PORT}"

    def get_nats_cluster_urls(self) -> str:
        servers = ','.join([f'{i[0]}:{i[1]}' for i in self.NATS_CLUSTER_SERVERS])
        if servers:
            return f"nats://{self.get_nats_auth()}{servers}"

    def get_nats_cluster_servers(self) -> List[str]:
        return [
            f"nats://{self.get_nats_auth()}{svr[0]}:{svr[1]}"
            for svr in self.NATS_CLUSTER_SERVERS
        ]
