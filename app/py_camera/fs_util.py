import os
import json

IPC_CONST_JSON_FILE = 'app/core/ipc-const.json'
IPC_EVENTS_JSON_FILE = 'app/core/events.json'

def get_ipc_const():
    with open(os.path.join(os.getcwd(), IPC_CONST_JSON_FILE)) as f:
        jsonConst = json.load(f)
        return jsonConst

def get_ipc_events():
    with open(os.path.join(os.getcwd(), IPC_EVENTS_JSON_FILE)) as f:
        jEvent = json.load(f)
        return jEvent
