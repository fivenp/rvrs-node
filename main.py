import os
import requests
import json
import time
import uuid

from mqtt import *

API_URL = "http://localhost:53805"
if "API_URL" in os.environ:
    API_URL = os.environ['API_URL']

TOKEN = uuid.UUID(int=uuid.getnode())
if "TOKEN" in os.environ:
    TOKEN = os.environ['TOKEN']

MQTT_URL = "rvrs-dev.cloud.shiftr.io"
if "MQTT_URL" in os.environ:
    MQTT_URL = os.environ['MQTT_URL']

MQTT_USER = "rvrs-dev"
if "MQTT_USER" in os.environ:
    MQTT_USER = os.environ['MQTT_USER']

MQTT_PWD = "Ldbfq2kDqR1CiAk4"
if "MQTT_PWD" in os.environ:
    MQTT_PWD = os.environ['MQTT_PWD']

MQTT = 0
MACHINE_ID = 0
MACHINE_SLUG = ""

HANDSHAKE_URL = f"{API_URL}/handshake/{TOKEN}"
REQUESTS_URL = f"{API_URL}/requests"
RESPONSES_URL = f"{API_URL}/responses"

def do_handshake(url):
    print("🤝 Starting Handshake")
    try:
        response = requests.get(url)
        response.raise_for_status()
        ret = response.json()
        MACHINE_SLUG = ret.get("listener")
        MACHINE_ID = ret.get("id")
        return response.json()  # Assuming api returns a json array of commands
    except requests.RequestException as e:
        print(f"🧨 Error during handshake: {e}")
        return


def main():
    print("🚀 Initialising")
    handshake = do_handshake(HANDSHAKE_URL)
    while not handshake:
        print("🔄 Sleep for 60 and Loop that handshake again....")
        time.sleep(60)
        handshake = do_handshake(HANDSHAKE_URL)
    print("✅ Handshake initialised")
    print(handshake)
    while MQTT != 1:
        connect_mqtt(MQTT_URL, MQTT_USER, MQTT_PWD, TOKEN)

if __name__ == "__main__":
    main()
