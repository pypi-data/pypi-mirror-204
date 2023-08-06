import logging
from collections import OrderedDict
from typing import Dict
from typing import Final

SYSTEMD_LOG_FORMAT: Final[str] = "%(message)s"
STDOUT_LOG_FORMAT: Final[str] = "%(message)s"
FILE_LOG_FORMAT: Final[str] = "%(asctime)s | %(levelname)s | %(message)s"

LOG_LEVEL: Final[Dict[str, int]] = OrderedDict(
    {
        "error": logging.ERROR,
        "warning": logging.WARNING,
        "info": logging.INFO,
        "debug": logging.DEBUG,
    }
)
