import re
import time
import json
import json
import logging
import socket
import threading
from threading import Thread, Lock
from ipc.client import IpcClient
from rp.camera import Camera

class IpcMedia(Thread):
    OUTGOING_MESSAGES = []
    INCOMING_MESSAGES = []
    MOTION_DETECTION_VIDEO_LENGTH_SEC = 15
    
    def __init__(self):
        self.cam = Camera(self.motion_detected)
        self.logger = logging.getLogger('IpcCamera')
        self.outgoing_messages_lock = Lock()
        self.incoming_messages_lock = Lock()
    
    def add_message(self, ipc_event, payload):
        self.OUTGOING_MESSAGES.append({ 'type': ipc_event, 'data': { 'payload': payload }})

    def capture(self, cmd):
        self.logger.info('RECIEVED RPCAM_CAPTURE', cmd)
        time.sleep(5)
        result = self.cam.capture(cmd['num'])
        self.add_message(self.ipc_events['RPCAM_CAPTURE_READY'], result)

    def record(self, cmd):
        self.logger.info('RECIEVED RPCAM_VIDEO_RECORD', cmd)
        result = self.cam.video(cmd['sec'])
        self.add_message(self.ipc_events['RPCAM_VIDEO_RECORD_READY'], result)

    def motion_detected(self):
        self.logger.info('RPCAM_MOTION_DETECTED')
        result = self.cam.video(self.MOTION_DETECTION_VIDEO_LENGTH_SEC)
        self.add_message(self.ipc_events['RPCAM_MOTION_DETECTED'], result)

    
    def parce_cmd(self, cmd):
        self.logger.info(cmd)
        payload = cmd['data']['payload']
        if cmd['type'] == self.ipc_events['RPCAM_CAPTURE']:
            self.capture(payload)
        elif cmd['type'] == self.ipc_events['RPCAM_VIDEO_RECORD']:
            self.record(payload)      

    def accept_event(self, cmd):
        with self.incoming_messages_lock:
            self.INCOMING_MESSAGES.append(cmd)
            self.logger.info('appending message to collection')

    def dispatch_outstanding(self, client):
        with self.outgoing_messages_lock:
            while len(self.OUTGOING_MESSAGES) != 0:
                self.logger.info('dispatching outstanding messages')
                message = self.OUTGOING_MESSAGES.pop()
                client.send(message)
                
    def process_incomming(self):
        with self.incoming_messages_lock:
            while len(self.INCOMING_MESSAGES) != 0:
                self.logger.info('handling incomming messages')
                cmd = self.INCOMING_MESSAGES.pop()
                self.parce_cmd(cmd)
                      
    def run(self, ipc_socket, ipc_events):
        self.ipc_socket = ipc_socket
        self.ipc_events = ipc_events
        self.running = True
        with IpcClient(self.ipc_socket) as client:
            client.incomeObservable.subscribe(self.accept_event)
            client.run();

            while self.running:
                try:
                    self.dispatch_outstanding(client)    
                    self.process_incomming();
                finally:
                    time.sleep(1)
            
