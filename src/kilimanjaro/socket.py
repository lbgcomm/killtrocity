import asyncio
import websockets

import json
import ssl

import config

import socket
import select

class raw_socket():
    def __init__(self):
        self.socket = None
        self.connected = False
        self.fails = 0

    async def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((config.cfg.get("km_addr"), config.cfg.get("km_port")))
        self.socket.setblocking(0)

        self.connected = True

    async def send_data(self, data):
        if self.socket is None:
            raise Exception("Socket invalid")

        self.socket.sendall(bytes(data, encoding='utf8'))

    async def send_data_json(self, data):
        if self.socket is None:
            raise Exception("Socket invalid")

        data_json = json.dumps(data)

        self.socket.sendall(bytes(data_json, encoding='utf8'))

    async def recv_data(self):
        if self.socket is None:
            raise Exception("Socket invalid")

        ready = select.select([self.socket], [], [], config.cfg.get("alive_timeout"))

        if ready[0]:
            return self.socket.recv(1024)
        else:
            return None

    async def is_alive(self):
        data = {}
        data["type"] = "ping"
        
        self.socket.sendall(bytes(json.dumps(data), encoding='utf8'))

    def is_connected(self):
        return self.connected

    def set_connected(self, val: bool):
        self.connected = val

socket_c = raw_socket()