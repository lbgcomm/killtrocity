import asyncio

import json
import ssl

import config

import socket
import select

class raw_socket():
    def __init__(self):
        self.socket = None
        self.connected = False
        
    async def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((config.cfg.get("km_addr"), config.cfg.get("km_port")))
        self.socket.setblocking(False)

        self.connected = True

    async def send_data(self, data):
        if self.socket is None:
            return

        tosend = bytes(json.dumps(data), encoding='utf8')

        self.socket.sendall(tosend)

    async def send_data_json(self, data):
        if self.socket is None:
            return

        data_json = json.dumps(data)

        tosend = bytes(data_json, encoding='utf8')

        self.socket.sendall(tosend)

    async def recv_data(self):
        if self.socket is None:
            return

        return self.socket.recv(2048)

    async def is_alive(self):
        data = {}
        data["type"] = "ping"
        data["data"] = [1, 3]
        
        await self.send_data(data)

    async def close(self):
        self.socket.close()

    def is_connected(self):
        return self.connected

    def set_connected(self, val: bool):
        self.connected = val

socket_c = raw_socket()