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


class Media():
  OUTGOING_MESSAGES = []
  INCOMING_MESSAGES = []
  MOTION_DETECTION_LENGTH_SEC = 15

  def __init__(self, motion_detection_length_sec):
    self.MOTION_DETECTION_LENGTH_SEC = motion_detection_length_sec
    self.cam = Camera(self.motion_detected)
    self.logger = logging.getLogger('ipc-media')
    self.outgoing_messages_lock = Lock()
    self.incoming_messages_lock = Lock()

  @staticmethod
  def format_msg(ipc_event, payload):
    return {'type': ipc_event, 'data': {'payload': payload}}

  def add_message(self, ipc_event, payload):
    self.OUTGOING_MESSAGES.append(self.format_msg(ipc_event, payload))

  def capture(self, cmd):
    self.logger.info('RECIEVED RPCAM_CAPTURE {}'.format(cmd))
    time.sleep(5)
    payload = self.cam.capture(cmd['num'])
    self.add_message(self.ipc_events['RPCAM_CAPTURE_READY'], payload)

  def record(self, cmd):
    self.logger.info('RECIEVED RPCAM_VIDEO_RECORD {}'.format(cmd))
    payload = self.cam.video(cmd['sec'])
    self.add_message(self.ipc_events['RPCAM_VIDEO_RECORD_READY'], payload)

  def motion_detected(self, path):
    self.logger.info('RPCAM_MOTION_DETECTED')
    self.add_message(self.ipc_events['RPCAM_MOTION_DETECTED'], path)

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
      client.income_observable.subscribe(self.accept_event)
      client.run()

      while self.running:
        try:
          self.dispatch_outstanding(client)
          self.process_incomming()
        finally:
          self.cam.detect_motion(self.MOTION_DETECTION_LENGTH_SEC)
          time.sleep(1)
