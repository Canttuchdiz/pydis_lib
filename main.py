import json
import asyncio
import aiofiles
import aiohttp
from aiohttp import ClientWebSocketResponse
import logging
import zlib
from time import sleep
from typing import Optional


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

    async def _hello_handler(self, websocket : ClientWebSocketResponse) -> int:
        async for message in websocket:
            print(message[1])

            message = message.json()
            return message["d"]["heartbeat_interval"]

    async def _websocket(self) -> None:
        session = aiohttp.ClientSession()
        async with session.ws_connect('{discord smth idk}') as ws:

            self.interval = await self._hello_handler(ws)

            await self._identification(ws)




    async def _identification(self, ws):

        data = Utility.json_loader('identifier.json', True)
        data["d"]["token"] = self.token
        await ws.send_json(data)
        response = await ws.receive()
        response = zlib.decompress(response[1])
        print(response)
        asyncio.ensure_future(await self._heartbeat(self.interval, ws))



    async def _heartbeat(self, interval: int, ws, d: str = "null") -> None:

        while not ws.closed:
            await ws.send_json({"op": 1, "d": None})
            response = await ws.receive()
            print(response.data)
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

