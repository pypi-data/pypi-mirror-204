from ._version import version as __version__
from ._native import (
    JSONStore,
    zmq_version,
    simdjson_active_runtime,
    simdjson_threaded,
    simdjson_version,
    Bitmap, DynamicScan, try_me
)
from ._config import Settings
from .app import create_application
from . import domain


class MyDynamicScan(DynamicScan):
    def __init__(self) -> None:
        DynamicScan.__init__(self)
    
    def check(self, payload: str) -> bool:
        print("in check...", payload)
        return True 
    
    def touch(self, payload: str):
        print("in touch...",payload)


a = MyDynamicScan()
try_me(a)


def app_factory():
    """
    Application factory compatible with uvicorn; use setting --factory
    to invoke it as shown in `run-recorder.sh` at the root folder 
    of this repo.

    """
    return create_application(Settings())
