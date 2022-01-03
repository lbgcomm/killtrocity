import asyncio

import json
import ssl

import config

import asyncio

class km_socket():
    def __init__(self):
        self.socket = None
        self.connected = False
        self.reader = None
        self.writer = None
        
    async def connect(self):
        self.reader, self.writer = await asyncio.open_unix_connection(path=config.cfg.get("km_socket_path"))

        self.connected = True

    async def send_data(self, data):
        if self.writer is None or self.writer.is_closing():
            return

        tosend = bytes(data, encoding='utf8')
        
        self.writer.write(tosend)
        await self.writer.drain()

    async def send_data_json(self, data):
        if self.writer is None or self.writer.is_closing() == True:
            return

        data_json = json.dumps(data)

        tosend = bytes(data_json, encoding='utf8')

        self.writer.write(tosend)
        await self.writer.drain()

    async def recv_data(self):
        data = await self.reader.read(2048)

        return data.decode()

    async def close(self):
        self.writer.close()
        await self.writer.wait_closed()

    def is_connected(self):
        if self.writer is None or self.writer.is_closing() == True:
            return False

        return True 

client = km_socket()