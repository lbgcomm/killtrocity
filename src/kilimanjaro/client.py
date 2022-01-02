import asyncio
import killfrenzy

import json
import threading

import config
from .socket import *

async def handle_data(data):
    if data is None:
        return

    info = None

    try:
        info = json.loads(data)
    except Exception as e:
        print("[KM] handle_data() :: Error parsing JSON data.")
        print(data)
        print(e)

        return
    if "type" not in info:
        print("[KM] handle_data() :: Data has no type.")

        return
    
    if "data" not in info:
        print("[KM] handle_data() :: Data has no data field.")
        
        return

    # Send to KF socket (in JSON format).
    if killfrenzy.socket_c.is_connected():
        try:
            print("Sending " + json.dumps(info))
            await killfrenzy.socket_c.send_data_json(info)
        except Exception as e:
            print("[KM] handle_data() :: Failed sending data to KF.")
            print(e)

            return

async def recv_updates():
    while True:
        if socket_c.is_connected() is not True:
            break

        try:
            data = await socket_c.recv_data()
        except Exception as e:
            print("[KM] recv_updates() :: Failed to receive data.")
            print(e)

            await sleep(5)

            continue

        if data is not None:
            print("[KM] recv_updates() :: Received data off of KM socket!")
            await handle_data(data)

            await sleep(5)

def recv_updates_thread():
    asyncio.run(recv_updates())

async def sleep(time):
    await asyncio.sleep(time)

async def start():
    first_time = True

    # Create tasks.
    p1 = None

    while True:
        # Attempt keep alive if socket is seen as connected.
        if socket_c.is_connected() == True:
            try:
                await socket_c.is_alive()
            except Exception as e:
                print("[KM] start() :: Keep alive failed...")
                print(e)
                
                socket_c.set_connected(False)

        # If socket isn't connected, try to connect.
        if socket_c.is_connected() == False:
            # See if this is our first time connecting.
            if first_time == False:
                print("[KM] start() :: Connection offline. Reconnecting...")
                
                try:
                    if p1 is not None:
                        p1.kill()
                except Exception as e:
                    pass
                
            else:
                first_time = False

            try:
                await socket_c.connect()
            except Exception as e:
                print("[KM] start() :: Failed to connect to Kilimanjaro.");
                print(e)

                await sleep(30)

                continue

            print("[KM] Connected!")

            # Send ping request.
            print("[KM] Sending ping request.")

            try:
                await socket_c.send_data("{\"type\": \"ping\", \"data\": {}}")
            except Exception as e:
                print("[KM] start() :: Failed to send ping request.")
                print(e)

                await sleep(10)

                continue

            # Start receive thread.
            p1 = threading.Thread(target=recv_updates_thread)
            p1.start()

        # Sleep for 30 seconds.
        await sleep(30)

def init():
    asyncio.run(start())