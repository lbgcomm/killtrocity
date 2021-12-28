import asyncio

import json

import config
import kilimanjaro
from .socket import *

async def validate():
    data = {}

    data["type"] = "connect"
    data["auth"] = 10041

    print("Sending data!")
    await kilimanjaro.socket_c.send_data_json(data)
    await socket_c.send_data_json(data)

    print("Data sent")

    await socket_c.recv_data()

def handle_data(data):
    if data["type"] is None:
        return
    
    if data["data"] is None:
        return

    # Handle a full config update.
    if data["type"] == "full_update":
        print("[KF] Received full update. Updating file...")

        # Output JSON pretty print.
        json_data = json.dumps(data["data"], indent=4)

        # Write to Kilimanjaro config file.
        with open("/etc/kilimanjaro/kilimanjaro.json", "w") as file:
            file.write(json_data["data"])
    # Handle a singular update.
    elif data["type"] == "update":
        if data["name"] is not None:
            if data["name"] == "conn_add":
                print("[KF] Received connection add. Sending to KM socket.")
            elif data["name"] == "conn_del":
                print("[KF] Received connection delete. Sending to KM socket.")
            elif data["name"] == "pp_add":
                print("[KF] Received port punch add. Sending to KM socket.")
            elif data["name"] == "pp_del":
                print("[KF] Received port punch delete. Sending to KM socket.")

        # Send to KM socket (in JSON format).
        kilimanjaro.socket_c.send_data_json(data)
    
    return

async def recv_messages():
    while True:
        data = await socket_c.recv_data()

        handle_data(data)

async def request_full_update():
    while True:
        data = {}
        data["type"] = "full_update"

        await socket_c.send_data_json(data)

        await asyncio.sleep(30.0)

async def connect():
    await socket_c.connect()

    print("Connected to Kill Frenzy!")

async def start():
    first_time = True

    # Create tasks.
    validate_task = asyncio.create_task(validate(), name="validate")
    recv_task = asyncio.create_task(recv_messages(), name="recv_messages")
    request_full_update_task = asyncio.create_task(request_full_update(), name="request_full_update")

    # Create an infinite loop that checks if the socket is connected and reconnects if need to be.
    while True:
        # Check if we're connected.
        if socket_c.is_connected() == False:
            if first_time == False:
                print("Kill Frenzy found offline. Reconnecting...")
            else:
                first_time = False

                # Cancel all tasks if they aren't already.
                validate_task.cancel()
                recv_task.cancel()
                request_full_update_task.cancel()

            try:
                # Connect to Kill Frenzy's web socket.
                await connect()

                # Now that we're connected, validate.
                done, pending = await asyncio.wait({validate_task})
                
                # Check if the validate task completed successfully.
                if validate_task in done:
                    # Now run the rest of the tasks.
                    L = await asyncio.gather(recv_task, request_full_update_task)

            except Exception as e:
                print("Failed to connect to Kill Frenzy.");
                print(e)

        await asyncio.sleep(30)

def init():
    asyncio.run(start())