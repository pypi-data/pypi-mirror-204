# -*- coding: utf-8 -*-
import ujson
from pydantic import BaseModel


class CustomBaseModel(BaseModel):
    """Custom Base Model with ujson configuration for dumps/loads and alias for some fileds

    Args:
        BaseModel (object): pydantic BaseModel

    Returns:
        object: an instance of a verified model
    """

    class Config:
        json_loads = ujson.loads
        json_dumps = ujson.dumps
        fields = {
            # "from_": "from",
        }

    def dict(self, args, *kwargs):
        kwargs.update({'by_alias': True})
        return super().dict(*args, **kwargs)

    def bytes(self) -> bytes:
        return self.json().encode()
