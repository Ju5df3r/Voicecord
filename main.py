import os
import sys
import json
import time
import requests
import threading
from websocket._core import create_connection
from keep_alive import keep_alive

status = "online"  #online/dnd/idle

GUILD_ID = 1318835149928136777
CHANNEL_ID = 1353606994715742338
SELF_MUTE = True
SELF_DEAF = True

usertoken = os.getenv("TOKEN")
if not usertoken:
    print("[ERROR] Please add a token inside Secrets.")
    sys.exit()

headers = {"Authorization": usertoken, "Content-Type": "application/json"}

validate = requests.get('https://canary.discordapp.com/api/v9/users/@me',
                        headers=headers)
if validate.status_code != 200:
    print("[ERROR] Your token might be invalid. Please check it again.")
    sys.exit()

userinfo = requests.get('https://canary.discordapp.com/api/v9/users/@me',
                        headers=headers).json()
username = userinfo["username"]
discriminator = userinfo["discriminator"]
userid = userinfo["id"]


def send_heartbeat(ws, interval, stop_event):
    while not stop_event.is_set():
        time.sleep(interval / 1000)
        try:
            ws.send(json.dumps({"op": 1, "d": None}))
            print("♥ Heartbeat sent")
        except Exception as e:
            print(f"Heartbeat failed: {e}")
            break


def joiner(token, status):
    ws = create_connection('wss://gateway.discord.gg/?v=9&encoding=json')
    print("✓ Connected to Discord Gateway")

    start = json.loads(ws.recv())
    heartbeat_interval = start['d']['heartbeat_interval']
    print(f"✓ Heartbeat interval: {heartbeat_interval}ms")

    auth = {
        "op": 2,
        "d": {
            "token": token,
            "properties": {
                "$os": "Windows 10",
                "$browser": "Google Chrome",
                "$device": "Windows"
            },
            "presence": {
                "status": status,
                "afk": False
            }
        },
        "s": None,
        "t": None
    }

    vc = {
        "op": 4,
        "d": {
            "guild_id": GUILD_ID,
            "channel_id": CHANNEL_ID,
            "self_mute": SELF_MUTE,
            "self_deaf": SELF_DEAF
        }
    }

    ws.send(json.dumps(auth))
    print("✓ Authentication sent")

    # Wait for READY event
    while True:
        msg = json.loads(ws.recv())
        if msg.get('t') == 'READY':
            print("✓ Ready event received")
            break

    # Join voice channel
    ws.send(json.dumps(vc))
    print("✓ Joined voice channel")

    # Start heartbeat thread
    stop_event = threading.Event()
    heartbeat_thread = threading.Thread(target=send_heartbeat,
                                        args=(ws, heartbeat_interval,
                                              stop_event))
    heartbeat_thread.daemon = True
    heartbeat_thread.start()

    # Keep reading messages to maintain connection
    print("✓ Maintaining connection... (press Ctrl+C to stop)")
    while True:
        try:
            msg = ws.recv()
            if msg:
                data = json.loads(msg)
                # Handle important opcodes
                if data['op'] == 9:  # Invalid session
                    print("! Invalid session, reconnecting...")
                    stop_event.set()
                    ws.close()
                    break
                elif data['op'] == 7:  # Reconnect
                    print("! Discord requested reconnect...")
                    stop_event.set()
                    ws.close()
                    break
        except KeyboardInterrupt:
            print("\n! Stopping...")
            stop_event.set()
            ws.close()
            break
        except Exception as e:
            print(f"! Error reading message: {e}")
            stop_event.set()
            ws.close()
            break


def run_joiner():
    os.system("clear")
    print(f"Logged in as {username}#{discriminator} ({userid}).")
    print("Connecting to voice channel...")
    while True:
        try:
            joiner(usertoken, status)
        except Exception as e:
            print(f"Connection lost: {e}. Reconnecting in 5 seconds...")
            time.sleep(5)


keep_alive()
run_joiner()
