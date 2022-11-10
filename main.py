import json
import asyncio
import aiofiles
import aiohttp
from aiohttp import ClientWebSocketResponse
import logging
import zlib
from time import sleep
from typing import Optional
from errors import *


class Utility:

    @staticmethod
    def json_loader(filename : str, load : Optional[bool] = False) -> str:
        with open(filename) as f:
            m = f.read()
            if load:
                return json.loads(m)
            return m





class ClientHandling():

    def __init__(self):
        self.token = ''
        self.interval = 0
        self.data = Utility.json_loader('identifier.json', True)


    async def _hello_handler(self, websocket : ClientWebSocketResponse) -> int:

        response = await websocket.receive()

        return response.json()["d"]["heartbeat_interval"]

    async def _websocket(self) -> None:
        session = aiohttp.ClientSession()
        async with session.ws_connect('wss://gateway.discord.gg') as ws:
            self.interval = await self._hello_handler(ws)

            await self._identification(ws)

    def _compress(self, response):
        return json.loads(zlib.decompress(response.data))["t"]

    async def _event_handler(self, ws : bytes):
        while not ws.closed:
            response = await self.poll_event(ws)
            if response.type == aiohttp.WSMsgType.TEXT:
                print(response.data)

            elif response.type == aiohttp.WSMsgType.BINARY:
                msg = self._compress(response)
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



    async def _heartbeat(self, interval: int, ws, d: str = "null") -> None:

        await ws.send_json({"op": 1, "d": None})
        # if response.type == aiohttp.WSMsgType.TEXT:
        #     print(json.loads(response.data))
        await asyncio.sleep(interval * 0.001)


    def run(self, token : str):

        setattr(self, 'token', token)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._websocket())
        loop.run_forever()


class Client(ClientHandling):

    pass

