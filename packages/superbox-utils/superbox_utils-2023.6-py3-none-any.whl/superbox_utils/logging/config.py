import dataclasses
import logging
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import List
from typing import Optional

from superbox_utils.config.exception import ConfigException
from superbox_utils.config.loader import ConfigLoaderMixin
from superbox_utils.logging import FILE_LOG_FORMAT
from superbox_utils.logging import LOG_LEVEL
from superbox_utils.logging import STDOUT_LOG_FORMAT
from superbox_utils.logging import SYSTEMD_LOG_FORMAT
from superbox_utils.logging import handler


@dataclass
class LoggingConfig(ConfigLoaderMixin):
    level: str = field(default="error")

    @property
    def verbose(self) -> int:
        """Get logging verbose level as integer."""
        return list(LOG_LEVEL).index(self.level)

    def init(
        self, log: Optional[str], log_path: Optional[Path] = None, name: Optional[str] = None, verbose: int = 0
    ) -> None:
        """Initialize logger handler and formatter.

        Parameters
        ----------
        log: str
            set log handler to systemd, stdout or file.
        log_path: Path, optional
            custom log path.
        name: str, optional
            The logger name.
        verbose: int
            Logging verbose level as integer.
        """
        logger: logging.Logger = logging.getLogger(name)
        logger.setLevel(LOG_LEVEL["info"])

        if log == "systemd":
            systemd_handler = handler.SystemdHandler()
            systemd_handler.setFormatter(logging.Formatter(SYSTEMD_LOG_FORMAT))
            logger.addHandler(systemd_handler)
        elif log == "stdout":
            stdout_handler: logging.Handler = logging.StreamHandler()
            stdout_handler.setFormatter(logging.Formatter(STDOUT_LOG_FORMAT))
            logger.addHandler(stdout_handler)
        elif log == "file" and log_path:
            log_path.mkdir(exist_ok=True, parents=True)

            file_handler = logging.FileHandler(log_path / f"{name}.log")
            file_handler.setFormatter(logging.Formatter(FILE_LOG_FORMAT, datefmt="%Y-%m-%d %H:%M:%S"))
            logger.addHandler(file_handler)
        else:
            default_handler: logging.Handler = logging.StreamHandler()
            default_handler.setFormatter(logging.Formatter(FILE_LOG_FORMAT, datefmt="%Y-%m-%d %H:%M:%S"))
            logger.addHandler(default_handler)

        self.update_level(name, verbose)

    def update_level(self, name: Optional[str], verbose: int) -> None:
        """Update the logging level in config data class.

        Parameters
        ----------
        name: str, optional
            The logger name.
        verbose: int
            Logging verbose level as integer.
        """
        logger: logging.Logger = logging.getLogger(name)

        levels: List[int] = list(LOG_LEVEL.values())
        level: int = levels[min(max(verbose, self.verbose), len(levels) - 1)]

        logger.setLevel(level)

    def _validate_level(self, value: str, _field: dataclasses.Field) -> str:
        if (value := value.lower()) not in LOG_LEVEL.keys():
            raise ConfigException(
                f"[{self.__class__.__name__.replace('Config', '').upper()}] Invalid log level '{self.level}'. The following log levels are allowed: {' '.join(LOG_LEVEL.keys())}."
            )

        return value
