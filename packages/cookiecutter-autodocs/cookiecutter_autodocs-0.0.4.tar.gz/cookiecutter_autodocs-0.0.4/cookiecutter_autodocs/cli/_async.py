from asyncio import run
from functools import wraps

from typer import Typer


class AsyncTyper(Typer):
    """A Typer subclass that allows async commands."""

    def async_command(self, *args, **kwargs):
        """Wraps a coroutine so it works with typer"""

        def decorator(async_func):
            @wraps(async_func)
            def sync_func(*_args, **_kwargs):
                return run(async_func(*_args, **_kwargs))

            self.command(*args, **kwargs)(sync_func)
            return async_func

        return decorator
