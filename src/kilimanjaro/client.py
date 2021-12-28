import asyncio

import json

import config
from .socket import *

async def connect():
    await socket_c.connect()

    print("Connected to Kilimanjaro!")

    print("Sending a simple ping request.")
    await socket_c.send_data("{\"type\": \"ping\", \"data\": {}}")

async def start():
    first_time = True

    while True:
        # Attempt keep alive if socket is seen as connected.
        if socket_c.is_connected() == True:
            try:
                await socket_c.is_alive()
            except Exception:
                print("Keep alive failed...")
                socket_c.set_connected(False)

        # If socket isn't connected, try to connect.
        if socket_c.is_connected() == False:
            # See if this is our first time connecting.
            if first_time == False:
                print("Kilimanjaro connection found offline. Reconnecting...")
            else:
                first_time = False

            try:
                await connect()
            except Exception as e:
                print("Failed to connect to Kilimanjaro.");
                print(e)

        # Sleep for 30 seconds.
        await asyncio.sleep(30)

def init():
    asyncio.run(start())