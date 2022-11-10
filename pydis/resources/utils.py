
from typing import Optional
import json
import zlib
import aiohttp

class Utility:

    @staticmethod
    def json_loader(filename : str, load : Optional[bool] = False) -> str:
        with open(filename) as f:
            m = f.read()
            if load:
                return json.loads(m)
            return m

    @staticmethod
    def _compress(response : aiohttp.WSMessage) -> str:
        return json.loads(zlib.decompress(response.data))["t"]