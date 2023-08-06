
from typing import Dict, Optional, Tuple
from zq_config.backends import Backend

from zq_config.backends.nacos import NacosBackend

BACKENDS_TYPES: Dict[str, Backend] = {
    "nacos": NacosBackend
}
