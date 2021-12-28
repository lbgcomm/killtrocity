import asyncio
import websockets

import json
import ssl

import config

class socket():
    def __init__(self):
        self.socket = None

    async def connect(self):
        self.socket = await websockets.connect("wss://" + config.cfg.get("kf_addr") + ":" + str(config.cfg.get("kf_port")), ssl=ssl.create_default_context())

    async def send_data(self, data):
        if self.socket is None:
            raise Exception("Socket invalid")

        await self.socket.send(data)

    async def send_data_json(self, data):
        if self.socket is None:
            raise Exception("Socket invalid")

        data_json = json.dumps(data)

        await self.socket.send(data_json)

    async def recv_data(self):
        if self.socket is None:
            raise Exception("Socket invalid")

        ret = await self.socket.recv()

        return ret

    def is_connected(self):
        if self.socket is None:
            return False

        return self.socket.open

socket_c = socket()