import asyncio
import functools
from typing import Callable


def run_in_executor(_func) -> Callable:
    """Run blocking code async."""

    @functools.wraps(_func)
    def wrapped(*args, **kwargs):
        loop = asyncio.get_running_loop()
        func = functools.partial(_func, *args, **kwargs)
        return loop.run_in_executor(executor=None, func=func)

    return wrapped
