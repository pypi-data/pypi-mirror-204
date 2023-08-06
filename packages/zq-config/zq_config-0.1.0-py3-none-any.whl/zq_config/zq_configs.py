from typing import cast
from zq_config.backends import Backend, get_dependency

from zq_config.backends.backend_registry import BACKENDS_TYPES



class ZQ_Config:
    _backend: Backend = None
    _init: bool = False

    @classmethod
    def __init__(cls, backend_type, **kwargs) -> None:
        if cls._init:
            return
        if backend_type not in BACKENDS_TYPES:
            raise Exception("Not found backend {}".format(backend_type))

        cls._backend = BACKENDS_TYPES[backend_type](**kwargs)
        cls._init = True

    @classmethod
    def get_raw(cls, data_id, data_group=None):
        return cls._backend.get(data_id, data_group)

    @classmethod
    def get_json(cls, data_id, data_group=None):
        data = cls._backend.get(data_id, data_group)
        return get_dependency("json").loads(data)

    @classmethod
    def get_toml(cls, data_id, data_group=None):
        data = cls._backend.get(data_id, data_group)
        return get_dependency("toml").loads(data)

    @classmethod
    def get(cls, data_id, data_group=None, format="json"):
        if format == "json":
            return cls.get_json(data_id, data_group)
        if format == "toml":
            return cls.get_toml(data_id, data_group)
        raise Exception("{} format is not support".format(format))
