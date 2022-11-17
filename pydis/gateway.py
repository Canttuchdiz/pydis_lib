import asyncio
import aiohttp
from .resources import Utility, UTILS_DIR, InvalidSessionError, IncorrectPayloadError
from aiohttp import ClientWebSocketResponse
import json
from typing import Optional, Coroutine, Callable


class DiscordWebSocket():

    def __init__(self):
        self.token = ''
        self.interval = 0
        self.data = Utility.json_loader(UTILS_DIR / 'jsons/identifier.json', True)
        self._events = []
        self.loop = None


    async def _hello_handler(self, websocket : ClientWebSocketResponse) -> int:

        response = await websocket.receive()

        return response.json()["d"]["heartbeat_interval"]

    async def _dispatch(self, event: str) -> None:
        method = "on_" + event.lower()

        try:
            coro : Callable = getattr(self, method)
            # wrapper = self._run_event(coro)
            self._loop.create_task(coro())


            # print(type(coro))
            # print(coro.__name__)

        except AttributeError as e:
            pass

    async def _run_event(self, coro : Callable):
        try:
            await coro()
        except Exception as e:
            print(e)

    async def _websocket(self) -> None:
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
        while not ws.closed:
            response = await self.poll_event(ws)
            if response.type == aiohttp.WSMsgType.TEXT:
                if json.loads(response.data)["op"] == 9:
                    raise InvalidSessionError()
                msg = json.loads(response.data)["t"]
                await self._dispatch(str(msg))


            elif response.type == aiohttp.WSMsgType.BINARY:
                msg = Utility._compress(response)
                await self._dispatch(msg)
                print(msg)
            else:
                print(response)


    async def poll_event(self, ws):
        return await ws.receive()



    async def _identification(self, ws):

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

        await ws.send_json({"op": 1, "d": None})
        # if response.type == aiohttp.WSMsgType.TEXT:
        #     print(json.loads(response.data))
        await asyncio.sleep(interval * 0.001)


    def run(self, token : str):

        self.token = token

        loop = asyncio.get_event_loop()
        self._loop = loop
        self._loop.run_until_complete(self._websocket())
        self._loop.run_forever()


