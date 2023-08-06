import abc
import sys
from types import ModuleType
from typing import Dict, Optional, Tuple



class Backend:
    @abc.abstractmethod
    def get(self, data_id, data_group) -> Optional[str]:
        raise NotImplementedError


def get_dependency(module_path: str) -> Optional[ModuleType]:
    if module_path not in sys.modules:
        __import__(module_path)

    return sys.modules[module_path]

