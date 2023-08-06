# -*- coding: utf-8 -*-
import uvloop
import uvicorn
from src.settings import settings


uvloop.install()


if __name__ == '__main__':
    uvicorn.run(
        'src.main:app',
        loop='uvloop',
        reload=False,
        host=settings.SERVICE_HOST,
        port=int(settings.SERVICE_PORT),
        reload_dirs=None,
        timeout_keep_alive=0
    )
