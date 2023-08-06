import logging
from logging import StreamHandler
from typing import Dict
from typing import Final


class SystemdHandler(StreamHandler):
    """Systemd handler with logging prefix for submit log level to journalcl."""

    # https://www.freedesktop.org/software/systemd/man/sd-daemon.html
    PREFIX: Final[Dict[int, str]] = {
        logging.CRITICAL: "<2>",
        logging.ERROR: "<3>",
        logging.WARNING: "<4>",
        logging.INFO: "<6>",
        logging.DEBUG: "<7>",
    }

    def emit(self, record) -> None:
        """Modify a record and add logging prefix."""
        try:
            msg: str = self.format(record)
            prefix: str = self.PREFIX.get(record.levelno, "<6>")
            self.stream.write(f"{prefix}{msg}{self.terminator}")
            self.flush()
        except RecursionError:
            raise
        except Exception:  # pylint: disable=broad-exception-caught
            self.handleError(record)
