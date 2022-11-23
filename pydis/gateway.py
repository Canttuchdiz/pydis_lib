import asyncio
import aiohttp
from .resources import Utility, UTILS_DIR, InvalidSessionError, IncorrectPayloadError
from aiohttp import ClientWebSocketResponse
import json
from typing import Optional, Coroutine, Callable
from .message import Message


class DiscordWebSocket:

    """
    Handles all gateway connections and coroutines
    """

    def __init__(self):
        self.token = ''
        self.interval = 0
        self.data = Utility.json_loader(UTILS_DIR / 'jsons/identifier.json', True)
        self._events = []
        self.loop = None


    async def _hello_handler(self, websocket : ClientWebSocketResponse) -> int:

        """
        Receives hello event and returns the interval
        :param websocket:
        :return:
        """

        response = await websocket.receive()

        return response.json()["d"]["heartbeat_interval"]

    async def _dispatch(self, event: str, payload = None) -> None:

        """
        Dispatches methods corresponding events received
        :param event:
        :param payload:
        :return:
        """

        method = "on_" + event.lower()

        try:
            coro : Callable = getattr(self, method)
            self._loop.create_task(self._run_event(event=event, coro=coro, payload=payload))

        except AttributeError as e:
            pass

    async def _call_method(self, coro, **kwargs):

        """
        Calls method
        :param coro:
        :param kwargs:
        :return:
        """

        try:
            await coro(**kwargs)
        except Exception as e:
            print(e)

    async def _run_event(self, event : str, coro : Callable, payload):

        """
        Calls the call method lol
        :param event:
        :param coro:
        :param payload:
        :return:
        """

        if event == "MESSAGE_CREATE":
            await self._call_method(coro=coro, message=Message(payload=payload, event=event))
        else:
            await self._call_method(coro=coro)


    async def _websocket(self) -> None:

        """
        Connects to websocket and does identification + heartbeat
        :return:
        """

        session = aiohttp.ClientSession()
        async with session.ws_connect('wss://gateway.discord.gg') as ws:
            self.interval = await self._hello_handler(ws)

            await self._identification(ws)

    # @property
    # def message_content(self, response : str, load : Optional[bool] = False):
    #     data = response
    #     if load:
    #         data = json.loads(response)
    #
    #     try:
    #         return data["d"]["content"]
    #     except Exception as e:
    #         return None




    async def _event_handler(self, ws : bytes):

        """
        Handles receiving events and dispatching the corresponding methods
        :param ws:
        :return:
        """

        while not ws.closed:
            response = await self.poll_event(ws)
            if response.type == aiohttp.WSMsgType.TEXT:
                if json.loads(response.data)["op"] == 9:
                    raise InvalidSessionError()
                msg = json.loads(response.data)
                try:
                    await self._dispatch(event=msg["t"], payload=msg)
                except AttributeError:
                    pass


            elif response.type == aiohttp.WSMsgType.BINARY:
                msg = Utility._compress(response)
                await self._dispatch(event=msg["t"], payload=msg)
            else:
                print(response)


    async def poll_event(self, ws):

        """
        Polls the event
        :param ws:
        :return:
        """

        return await ws.receive()



    async def _identification(self, ws):

        """
        Identifies application to discord
        :param ws:
        :return:
        """

        self.data["d"]["token"] = self.token

        try:
            await ws.send_json(self.data)
        except Exception as e:
            raise IncorrectPayloadError()
        asyncio.create_task(self._event_handler(ws))
        while not ws.closed:
            await self._heartbeat(interval=self.interval, ws=ws)

    # async def push(self, )

    async def _heartbeat(self, interval: int, ws, d: str = "null") -> None:

        """
        Keeps gateway connection live
        :param interval:
        :param ws:
        :param d:
        :return:
        """

        await ws.send_json({"op": 1, "d": None})
        # if response.type == aiohttp.WSMsgType.TEXT:
        #     print(json.loads(response.data))
        await asyncio.sleep(interval * 0.001)


    def run(self, token : str):

        """
        Starts the event loops and connects to the gateway
        :param token:
        :return:
        """

        self.token = token

        loop = asyncio.get_event_loop()
        self._loop = loop
        self._loop.run_until_complete(self._websocket())
        self._loop.run_forever()


