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
  _outgoing_messages_lock = Lock()
  _incoming_messages_lock = Lock()
  _detect_motion = False

  def __init__(self, motion_detection_length_sec):
    self.OUTGOING_MESSAGES = []
    self.INCOMING_MESSAGES = []
    self._outgoing_messages_lock = Lock()
    self._incoming_messages_lock = Lock()
    self.MOTION_DETECTION_LENGTH_SEC = motion_detection_length_sec
    self.cam = Camera(self.motion_detected)
    self.logger = logging.getLogger('ipc-media')

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

  def motion_detected(self, path, score):
    self.logger.info('RPCAM_MOTION_DETECTED')
    param = {'path': path, score: 'score'}
    self.add_message(self.ipc_events['RPCAM_MOTION_DETECTED'], param)

  def parse_cmd(self, cmd):
    self.logger.info(cmd)
    payload = cmd['data']['payload']
    cmd_type = cmd['type']
    if cmd_type == self.ipc_events['RPCAM_CAPTURE']:
      self.capture(payload)
    elif cmd_type == self.ipc_events['RPCAM_VIDEO_RECORD']:
      self.record(payload)
    elif cmd_type == self.ipc_events['RPCAM_START_MOTION_DETECTION']:
      self._detect_motion = True
    elif cmd_type == self.ipc_events['RPCAM_STOP_MOTION_DETECTION']:
      self._detect_motion = False

  def accept_event(self, cmd):
    with self._incoming_messages_lock:
      self.INCOMING_MESSAGES.append(cmd)
      self.logger.info('Event Accepted: {}'.format(cmd))

  def dispatch_outstanding(self, client):
    with self._outgoing_messages_lock:
      while len(self.OUTGOING_MESSAGES) != 0:
        self.logger.info('dispatching outstanding messages')
        message = self.OUTGOING_MESSAGES.pop()
        client.send(message)

  def process_incoming(self):
    with self._incoming_messages_lock:
      while len(self.INCOMING_MESSAGES) != 0:
        self.logger.info('handling incomming messages')
        cmd = self.INCOMING_MESSAGES.pop()
        self.parse_cmd(cmd)

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
          self.process_incoming()
        finally:
          if self._detect_motion:
            self.cam.detect_motion(self.MOTION_DETECTION_LENGTH_SEC)
          time.sleep(1)
