import re
import sys
import time
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
    format_payload = json.dumps(payload)
    return {'type': ipc_event, 'data': {'payload': format_payload}}

  def add_message(self, ipc_event, payload):
    with self._outgoing_messages_lock:
      self.OUTGOING_MESSAGES.append(self.format_msg(ipc_event, payload))

  @staticmethod
  def extract_cmd_payload(cmd):
    payload = None
    data = cmd['data']
    if isinstance(data, dict) and 'payload' in data:
      payload = data['payload']
    return payload

  def capture(self, cmd):
    self.logger.info('Capturing {}'.format(cmd))
    payload = self.cam.capture(cmd['num'])

    self.add_message(self.ipc_events['RPCAM_CAPTURE_READY'], payload)

  def record(self, cmd):
    self.logger.info('Recording {}'.format(cmd))
    payload = self.cam.video(cmd['sec'])
    self.add_message(self.ipc_events['RPCAM_VIDEO_RECORD_READY'], payload)

  def motion_detected(self, path, score):
    motion_data = {'path': path, 'score': score}
    self.logger.info('RPCAM_MOTION_DETECTED {}'.format(motion_data))
    self.add_message(self.ipc_events['RPCAM_MOTION_DETECTED'], motion_data)

  def parse_cmd(self, cmd):
    self.logger.info('parse_cmd {}'.format(cmd))
    payload = Media.extract_cmd_payload(cmd)
    if payload:
      if cmd['type'] == self.ipc_events['RPCAM_CAPTURE']:
        self.capture(payload)
      elif cmd['type'] == self.ipc_events['RPCAM_VIDEO_RECORD']:
        self.record(payload)

  def accept_event(self, cmd):
    with self._incoming_messages_lock:
      self.INCOMING_MESSAGES.append(cmd)

  def dispatch_outstanding(self, client):
    self.logger.info('process out msg {}'.format(len(self.OUTGOING_MESSAGES)))
    with self._outgoing_messages_lock:
      while len(self.OUTGOING_MESSAGES) != 0:
        message = self.OUTGOING_MESSAGES.pop()
        client.send(message)

  def process_incoming(self):
    self.logger.info('process in msg {}'.format(len(self.INCOMING_MESSAGES)))
    with self._incoming_messages_lock:
      while len(self.INCOMING_MESSAGES) != 0:
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
          self.cam.detect_motion(self.MOTION_DETECTION_LENGTH_SEC)
          time.sleep(1)
