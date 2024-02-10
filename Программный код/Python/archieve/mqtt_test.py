from paho.mqtt import client as mqtt_client


MQTT_HOST = 'mqtt.by'
MQTT_PORT = 1883
MQTT_CLIENT_ID = f'Auto_OrderPicker_1517_{random.randint(0, 1000)}'
MQTT_USER = 'Auto_OrderPicker_1517'
MQTT_PSWD = 'r0316cce'

MQTT_PREFIX = 'user/Auto_OrderPicker_1517/'

MQTT_TEST_TOPIC = MQTT_PREFIX + 'test'


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(MQTT_TEST_TOPIC)
    client.on_message = on_message
    
    

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            subscribe(client)
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return python code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(MQTT_CLIENT_ID)
    client.username_pw_set(MQTT_USER, MQTT_PSWD)
    client.on_connect = on_connect
    client.connect(MQTT_HOST, MQTT_PORT)
    return client
    
    
FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

def on_disconnect(client, userdata, rc):
    logging.info("Disconnected with result python code: %s", rc)
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        logging.info("Reconnecting in %d seconds...", reconnect_delay)
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            subscribe(client)######################################################
            logging.info("Reconnected successfully!")
            return
        except Exception as err:
            logging.error("%s. Reconnect failed. Retrying...", err)

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    logging.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)