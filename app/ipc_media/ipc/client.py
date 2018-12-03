import re
import sys
import time
import json
import socket
import logging
from threading import Thread, Lock
from rx import Observable, Observer


class IpcClient():
  income_observable = None
  _income_observer = None

  def __init__(self, server_address):
    self.logger = logging.getLogger('IpcClient')
    self.addr = server_address
    self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    self.receive_msg = False
    self.messages_lock = Lock()
    self.income_observable = Observable.create(self.init_income_observable)

  def init_income_observable(self, observer):
    self._income_observer = observer

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

  def stringify_json(self, jObj):
    self.logger.info('stringify_json: {}'.format(jObj))
    return (json.dumps(jObj) + ' \f').encode('UTF-8')

  def send(self, jsonMsg):
    msg = self.stringify_json(jsonMsg)
    self.logger.info('Sending Message {}'.format(msg))
    self.sock.send(msg)

  def parse_json(self, response):
    strJson = re.sub(r'[\x0c]', '', str(response, 'UTF-8'))
    return json.loads(strJson)

  def ipc_client_routine(self):
    self.receive_msg = True
    try:
      while self.receive_msg:
        msg = self.recieve()
        cmd = self.parse_json(msg)
        self.logger.info('Recieved Message: {}'.format(cmd))
        with self.messages_lock:
          self.logger.info(cmd)
          self._income_observer.on_next(cmd)
    except:
      self.logger.error(sys.exc_info())

  def stop(self):
    self.receive_msg = False

  def run(self, deamon=True):
    th = Thread(target=self.ipc_client_routine)
    th.daemon = deamon
    th.start()
