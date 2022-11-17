from pydis import DiscordWebSocket
from typing import TypeVar, Callable, Optional, Coroutine, Any
import asyncio

Coro = TypeVar('Coro', bound=Callable[..., Coroutine[Any, Any, Any]])

class Client(DiscordWebSocket):


    def event(self, coro: Coro, /) -> Coro:
        """A decorator that registers an event to listen to.
        You can find more info about the events on the :ref:`documentation below <discord-api-events>`.
        The events must be a :ref:`coroutine <coroutine>`, if not, :exc:`TypeError` is raised.
        Example
        ---------
        .. code-block:: python3
            @client.event
            async def on_ready():
                print('Ready!')
        .. versionchanged:: 2.0
            ``coro`` parameter is now positional-only.
        Raises
        --------
        TypeError
            The coroutine passed is not actually a coroutine.
        """

        if not asyncio.iscoroutinefunction(coro):
            raise TypeError('event registered must be a coroutine function')

        setattr(self, coro.__name__, coro)
        return coro

