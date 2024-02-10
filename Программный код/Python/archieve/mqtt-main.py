from cam_capture import capture
from qr_scanner import scan_qrcode

from mqtt_msg_center import subscribe_and_handler,
                            mqtt_publish_log,
                            mqtt_start,
                            mqtt_stop


MQTT_ORDER_TOPIC = 'order'
MQTT_CMD_TOPIC = 'cmd'


CAPTURE_CMD = 'capture'
QR_SCAN_CMD = 'scan_qrcode'

image_name = "test-1.jpg"


def mqtt_on_cmdMsg(client, userdata, msg):
    cmd = msg.payload.decode('utf-8')
    print(f"Command '{cmd}' from '{msg.topic}'")
    if (cmd == CAPTURE_CMD):
        capture(image_name)
        print('image was captured!')
    elif (cmd == QR_SCAN_CMD):
        print('Scanning for QR python code...')
        data = scan_qrcode(image_name)
        if (data):
            print(f"Data = '{data}'")
        else:
            print("QR Code not detected")
    else:
        print("Error! Unknown command")
            

def mqtt_on_orderMsg(client, userdata, msg):
    print(f"Order '{msg.payload.decode('utf-8')}' from '{msg.topic}'")




client = mqtt_connect()
subscribe_and_handler(client, MQTT_ORDER_TOPIC, mqtt_on_orderMsg)
subscribe_and_handler(client, MQTT_CMD_TOPIC, mqtt_on_cmdMsg)
mqtt_start(client)
#time.sleep(600)
#mqtt_stop(client)



