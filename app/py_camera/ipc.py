import re
import time
import json
import json
import logging
import socket
from cam import Camera

class IpcCamera(object):
    MESSAGES = []

    def __init__(self, socket, ipc_events):
        self.ipc_socket = socket
        self.cam = Camera(self.motion_detected)
        self.logger = logging.getLogger('IpcCamera')
        self.ipc_events = ipc_events

    def parse_json(self, response):
        strJson = re.sub(r'[\x0c]', '', str(response, 'UTF-8'))
        return json.loads(strJson)

    def capture(self, cmd):
        self.logger.info('RECIEVED RPCAM_CAPTURE', cmd)
        result = self.cam.capture(cmd['num'])
        self.MESSAGES.append({ 'type': self.ipc_events['RPCAM_CAPTURE_READY'], 'data': { 'payload': result }})

    def record(self, cmd):
        self.logger.info('RECIEVED RPCAM_VIDEO_RECORD', cmd)
        result = self.cam.video(cmd['sec'])
        self.MESSAGES.append({ 'type': self.ipc_events['RPCAM_VIDEO_RECORD_READY'], 'data': { 'payload': result }})

    def motion_detected(self):
        self.logger.info('RPCAM_MOTION_DETECTED')
        result = self.cam.video(15)
        self.MESSAGES.append({ 'type': self.ipc_events['RPCAM_MOTION_DETECTED'], 'data': { 'payload': result }})

    def parse_cmd(self, cmd):
        payload = cmd['data']['payload']
        if cmd['type'] == self.ipc_events['RPCAM_CAPTURE']:
            self.capture(payload)
        elif cmd['type'] == self.ipc_events['RPCAM_VIDEO_RECORD']:
            self.record(payload)

    def dispatch_outstanding(self, client):
        while len(self.MESSAGES) != 0:
            message = self.MESSAGES.pop()
            client.send(message)

    def ipc(self):
        with Client(self.ipc_socket) as client:
            self.dispatch_outstanding(client)
            cmd = self.parse_json(client.recieve())
            self.parse_cmd(cmd)

    def stop_co(self):
        self.running = false

    def start_co(self):
        self.running = True
        while self.running:
            try:
                self.ipc()
            finally:
                time.sleep(2)

class Client(object):
    def __init__(self, server_address):
        self.logger = logging.getLogger('IpcClient')
        self.addr = server_address
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    def connect(self):
        self.logger.info('Connect')
        self.sock.connect(self.addr)

    def close(self):
        self.logger.info('Closing Connection')
        self.sock.close()

    def __enter__(self):
        self.logger.info('Starting Connection')
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def recieve(self):
        self.logger.info('Recieving Message')
        return self.sock.recv(256)

    def send(self, jsonMsg):
        msg = (json.dumps(jsonMsg) + ' \f').encode('UTF-8')
        self.logger.info('Sending Message', jsonMsg)
        self.sock.send(msg)