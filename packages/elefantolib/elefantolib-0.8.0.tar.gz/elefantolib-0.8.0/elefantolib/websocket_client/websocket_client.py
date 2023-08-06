from typing import Callable

import websockets

from elefantolib.websocket_client import BaseWebsocketClient


class WebsocketClient(BaseWebsocketClient):

    async def ws(self, path: str, callback: Callable, *args, **kwargs):
        url = f'{self.ws_url}/{path}'
        async with websockets.connect(url) as ws_connect:
            await callback(ws_connect, *args, **kwargs)
