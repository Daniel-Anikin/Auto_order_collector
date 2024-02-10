# python3.6

import random

from paho.mqtt import client as mqtt_client


MQTT_HOST = 'mqtt.by'
MQTT_PORT = 1883
MQTT_CLIENT_ID = f'Auto_OrderPicker_1517_{random.randint(0, 1000)}'
MQTT_USER = 'Auto_OrderPicker_1517'
MQTT_PSWD = 'r0316cce'

MQTT_PREFIX = 'user/Auto_OrderPicker_1517/'

MQTT_TEST_TOPIC = MQTT_PREFIX + 'test'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return python code %d\n", rc)

    client = mqtt_client.Client(MQTT_CLIENT_ID)
    client.username_pw_set(MQTT_USER, MQTT_PSWD)
    client.on_connect = on_connect
    client.connect(MQTT_HOST, MQTT_PORT)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(MQTT_TEST_TOPIC)
    print(f'Subcribed to `{MQTT_TEST_TOPIC}` topic')
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()