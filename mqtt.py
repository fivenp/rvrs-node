import paho.mqtt.client as paho
from paho import mqtt
import json

from execute import execute_request
from main import TOKEN, API_URL

def connect_mqtt(url, user, pwd, nodeToken):
    print("🤝 Connecting to MQTT")
    client = paho.Client(paho.CallbackAPIVersion.VERSION2, protocol=paho.MQTTv311)
    client.on_log = on_mqtt_log
    client.on_connect = on_mqtt_connect
    client.on_subscribe = on_mqtt_subscribe
    client.on_message = on_mqtt_message
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    client.username_pw_set(user, pwd)
    client.connect(url, 8883)
    client.subscribe(f"requests/{TOKEN}", qos=1)
    client.loop_forever()

def on_mqtt_log(mqttc, obj, level, string):
    print("-> " + string)

def on_mqtt_connect(client, userdata, flags, rc, properties=None):
    print(f"Connected with result code {rc}")
    MQTT = 1
    print("✅ MQTT Connected")

def on_mqtt_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("👂 Listening for new requests....")
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_mqtt_message(client, userdata, msg):
    print("📢 New request:")
    print(msg.topic+" "+str(msg.qos)+" -> "+str(msg.payload))
    print("------------------------------------------------")
    payload = json.loads(msg.payload)
    if "data" in payload:
        print("Payload good")
        if "requestTarget" in payload:
            print("Request Target set")
            if payload["requestTarget"] == TOKEN:
                print("Request Target good")
                if "requestId" in payload["data"]:
                    print("Request ID set")
                    execute_request(API_URL,payload["requestTargetId"],payload["data"]["requestId"],payload["data"]["type"],payload["data"]["options"],payload["data"]["dest"])
