from cam_capture import capture
from qr_scanner import scan_qrcode

import time



def DPRINT(msg):
    print(msg)

######################################################################
########################### Serial UART ##############################
######################################################################

import serial

ser = ""

PORT = "COM1"
UART_SPEED = 115200


def uart_init():
    DPRINT("uart init..")
    ser = serial.Serial(PORT, UART_SPEED)
    return ser
    
def uart_print(msg):
    #msg += '\n'
    DPRINT(f'UART << {msg}')
    ser.write(msg.encode('utf-8'))


######################################################################
############# COMMANDS and get CMD AND ORDER from MQTT ###############
######################################################################

from mqtt_msg_center import (mqtt_connect,
                            subscribe_and_handler,
                            mqtt_publish_log,
                            mqtt_start,
                            mqtt_stop)

import mqtt_settings


client = ''

NO_CMD = 0
START_CMD = 1
BREAK_CMD = 2
PAUSE_CMD = 3
CH_ORDER_CMD = 4
SAVE_ORDER_CMD = 5

cmd = None

def reset_cmd():
    global cmd
    cmd = NO_CMD

reset_cmd()


commands = [
    {"cmd": NO_CMD,         "text": "no_cmd"},
    {"cmd": START_CMD,      "text": "start_cmd"},
    {"cmd": BREAK_CMD,      "text": "break_cmd"},
    {"cmd": PAUSE_CMD,      "text": "pause_cmd"},
    {"cmd": CH_ORDER_CMD,   "text": "ch_order_cmd"},
    {"cmd": SAVE_ORDER_CMD, "text": "save_order_cmd"}
]

NO_ORDER_MSG = ""
order_msg = NO_ORDER_MSG


MQTT_ORDER_TOPIC = mqtt_settings.MQTT_PREFIX + 'order'
MQTT_CMD_TOPIC = mqtt_settings.MQTT_PREFIX + 'cmd'


def mqtt_print(msg):
    mqtt_publish_log(client, msg)

def mqtt_on_cmdMsg(client, userdata, msg):
    global cmd
    cmd_text = msg.payload.decode('utf-8')
    print(f"Command '{cmd_text}' from '{msg.topic}'")
    cmd = NO_CMD
    
    for command in commands:
        if cmd_text == command["text"]:
            cmd = command["cmd"]
            break
    
     
def mqtt_on_orderMsg(client, userdata, msg):
    global order_msg
    order_msg = msg.payload.decode('utf-8')
    print(f"Order '{order_msg}' from '{msg.topic}'")


def mqtt_init():   
    print("mqtt init..")
    client = mqtt_connect()
    subscribe_and_handler(client, MQTT_ORDER_TOPIC, mqtt_on_orderMsg)
    subscribe_and_handler(client, MQTT_CMD_TOPIC, mqtt_on_cmdMsg)
    mqtt_start(client)
    return client
    
    
######################################################################
######################################################################


def log(msg):
    print(msg)
    mqtt_print(msg)




storage_cells_num = 9

storage_first_cell_pos_cm = 5
storage_cell_size_cm = 10

grip_opened_u_pos = 0
grip_closed_u_pos = 180
grip_opened_v_pos = 0
grip_closed_v_pos = 180


current_cell = 0


def device_home():
    global current_cell
    log("go home...")
    msg = f'G1 U{grip_opened_u_pos} V{grip_opened_v_pos}'
    uart_print(msg)
    uart_print('G28')
    time.sleep(2)  #### Change to receive 'done' cmd from Serial ESP32
    current_cell = 0
    

def device_pause():
    log("Pause order collecting!")
    uart_print('M18') #Motors off



def convert_cell_to_pos(num):
    if num == 0:
        pos = 0
    elif num >= 1:
        pos = (storage_first_cell_pos_cm +
            (num - 1) * storage_cell_size_cm)
    return pos


def device_next_cell():
    global current_cell
    log("Go to next cell")
    current_cell += 1
    pos = convert_cell_to_pos(current_cell)
    uart_print(f'G1 X{pos}')
    time.sleep(2)  #### Change to receive 'done' cmd from Serial ESP32

def device_grab_object():
    log("Grab the object")
    uart_print(f'G1 U{grip_closed_u_pos}')
    time.sleep(1)  #### Change to receive 'done' cmd from Serial ESP32
    uart_print(f'G1 V{grip_closed_v_pos}')
    time.sleep(1)  #### Change to receive 'done' cmd from Serial ESP32

def device_pull_object():
    log("Pull the object")
    uart_print(f'G1 U{grip_opened_u_pos}')
    time.sleep(1)  #### Change to receive 'done' cmd from Serial ESP32

def device_release_object():
    log("Release the object")
    uart_print(f'G1 V{grip_opened_v_pos}')
    time.sleep(1)  #### Change to receive 'done' cmd from Serial ESP32

def device_break():
    pass




warehouse = ["гайки", 
             "винты",
             "шайбы",
             "шпильки",
             "подшипники",
             "линейные направляющие",
             "валы",
             "двигатели",
             "датчики"
]

order = []
collected = []

def reset_order():
    global order
    order = []

def reset_collected_order():
    global collected
    collected = []

def orderlist_to_string(items):
    msg = ', '.join(str(item) for item in items)
    return msg
    

def decode_order():
    global order_msg
    if order_msg != NO_ORDER_MSG:
        log("New order was received!")
        reset_order()
        msg = list(set(order_msg.split()))
        correct_fl = True
        for word in msg:
            if word in collected:
                log(f"Warning! Item '{word}' is already picked up!")
            elif word in warehouse:
                order.append(word)
                log(f"Item '{word}' was added to order list")
            else:
                log(f"Error! Incorrect item '{word}'")
                correct_fl = False
        
        if (not correct_fl):
            log("Warning! One or more order positions were incorrect!")
        
        msg = 'Текущий заказ: ' + orderlist_to_string(order)
        log(msg)
        order_msg = NO_ORDER_MSG
        
        



        

def initializing_handler():
    DPRINT(">> Initializing handler")
    global client
    global ser
    global state
    client = mqtt_init()
    ser = uart_init()
    device_home()
    log("Waiting for commands")
    state = WAITING_ST


def waiting_handler():
    DPRINT(">> Waiting handler")
    DPRINT(f">> Command is '{cmd}'")
    global state
    if cmd == CH_ORDER_CMD: 
        log("Changing order..")
        state = SETTING_ORDER_ST
    elif cmd == START_CMD:
        state = STARTING_ST
    elif cmd == NO_CMD:
        pass
    else:
        log(f'Error! Wrong command - {cmd}')
    reset_cmd()

    
def setting_order_handler():
    DPRINT(">> Setting order handler")
    global state
    decode_order()
    DPRINT(">> decoded order: ")
    DPRINT(order)
    DPRINT(f">> Command is '{cmd}'")
    if cmd == SAVE_ORDER_CMD:
        log("Saving the order")
        state = WAITING_ST
    reset_cmd()
        

def starting_handler():
    DPRINT(">> Starting handler")
    global state
    if (len(order) == 0):
        if (len(collected) > 0):
            log("Order is already picked up!")
            state = FINISH_ST
        else:
            log("Warning! Order is empty!")
            state = WAITING_ST
    else:
        log("Starting order collecting..")
        state = SCANNING_ST



MOVE = 0
SCAN = 1
GRAB = 2
THROW = 3
scanning_stage = MOVE

item = ""

def reset_scanningStage():
    global item
    global current_cell
    global scanning_stage
    item = None
    current_cell = 0
    scanning_stage = MOVE



def scanning_handler():
    global state
    global item
    global current_cell
    global scanning_stage
    DPRINT(">> Scanning handler")
    
    DPRINT(f">> Command is '{cmd}'")
    if cmd == PAUSE_CMD:
        if scanning_stage = GRAB:
            scanning_stage = SCAN
        device_pause()
        state = PAUSE_ST
        return
    elif cmd == BREAK_CMD:
        state = BREAK_ST
        return
    reset_cmd()
    
    if scanning_stage == MOVE:
        if (current_cell == storage_cells_num):
            log("The last cell was reached! Scan again from the first cell!")
            current_cell = 0
        DPRINT('Going to the next cell..')
        device_next_cell()
        DPRINT(f'Current cell is #{current_cell}')
        scanning_stage = SCAN
    
    elif scanning_stage == SCAN:   
        DPRINT('Capture img and scan for QR')
        filename = f'cell-{current_cell}.png'
        DPRINT(filename)
        
        capture(filename)
        data = scan_qrcode(filename)
        if (not data):
            log(f'Cant found QR python code. Try again..')
        else:
            DPRINT("Successfully found and read QR python code!")
            log(f"Found '{data}' item")
            if (data in order):
                log(f"'{data}' is in order! Collecting..")
                item = data
                scanning_stage = GRAB
            else:
                log(f"'{data}' is not in order! Continue scanning!")
                scanning_stage = MOVE
                
    elif scanning_stage == GRAB:
        device_grab_object()
        device_pull_object()
        device_release_object()
        log(f'{item} was collected!')
        
        index = order.index(item)
        collected.append(order.pop(index))
        
        DPRINT("order:") 
        DPRINT(order)
        DPRINT("collected:") 
        DPRINT(collected)
        
        item = None
        scanning_stage = MOVE
        if (len(order) == 0):
            log("Order is picked up!")
            state = FINISH_ST
    else:
        DPRINT("Error! Wrong scanning stage!")
    
    
    
    
        
def reset_scanning_data():
    reset_scanningStage()
    reset_order()
    reset_collected_order()


def end_scanning():
    if (len(collected) > 0):
        log('Collected: ' + orderlist_to_string(collected))
    if (len(order) > 0):
        log('Not collected: ' +orderlist_to_string(order))
    
    reset_scanning_data()
    device_home()
    log("Waiting for commands")

    
def finish_handler():
    DPRINT(">> Finish handler")
    global state
    log("Order completed!")
    ### Display finish screen
    end_scanning()
    state = WAITING_ST
    
def break_handler():
    DPRINT(">> Break handler")
    global state
    log("Break order collecting!")
    device_break()
    ### Display break screen
    end_scanning()
    state = WAITING_ST

def pause_handler():
    DPRINT(">> Pause handler")
    global state
    if cmd == CH_ORDER_CMD: 
        state = CH_ORDER_ST
    elif cmd == START_CMD:
        state = STARTING_ST
    elif cmd == BREAK_CMD:
        state = BREAK_ST
    reset_cmd()
    
def ch_order_handler():
    DPRINT(">> Changing order handler")
    global state
    decode_order()
    DPRINT(">> decoded order: ")
    DPRINT(order)
    DPRINT(f">> Command is '{cmd}'")
    if cmd == SAVE_ORDER_CMD:
        state = PAUSE_ST    
    reset_cmd()
    

INITIALIZING_ST     = 0
WAITING_ST          = 1
SETTING_ORDER_ST    = 2
STARTING_ST         = 3
SCANNING_ST         = 4
FINISH_ST           = 5
PAUSE_ST            = 6
CH_ORDER_ST         = 7
BREAK_ST            = 8

state = INITIALIZING_ST

state_handlers = [
        {"state": INITIALIZING_ST,  "func": initializing_handler},
        {"state": WAITING_ST,       "func": waiting_handler},
        {"state": SETTING_ORDER_ST, "func": setting_order_handler},
        {"state": STARTING_ST,      "func": starting_handler},
        {"state": SCANNING_ST,      "func": scanning_handler},
        {"state": FINISH_ST,        "func": finish_handler},
        {"state": PAUSE_ST,         "func": pause_handler},
        {"state": CH_ORDER_ST,      "func": ch_order_handler},
        {"state": BREAK_ST,         "func": break_handler}
]

while True:
    for handler in state_handlers:
        if handler["state"] == state:
            handler["func"]()
            break
    #time.sleep(1)