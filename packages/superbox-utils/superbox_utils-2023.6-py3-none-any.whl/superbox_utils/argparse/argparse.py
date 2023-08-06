import argparse

from superbox_utils.logging import LOG_LEVEL


def init_argparse(description: str) -> argparse.ArgumentParser:
    """Initialize argument parser with default arguments.

    Parameters
    ----------
    description: str
        Argument parser description.

    Returns
    -------
    ArgumentParser
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "-l",
        "--log",
        choices=["systemd", "stdout", "file"],
        default="stdout",
        help="set log handler to file or systemd",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help=f"verbose mode: multiple -v options increase the verbosity (maximum: {len(LOG_LEVEL)})",
    )

    return parser
