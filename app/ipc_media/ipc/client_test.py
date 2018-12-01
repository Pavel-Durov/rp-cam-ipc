import os
import sys
import time
import unittest
from ipc.media import Media
from ipc.client import IpcClient
from fs.util import get_ipc_const, get_ipc_events


class TestingIpcClient(unittest.TestCase):

  def test_json_stringify(self):
    json_str = IpcClient(
        'invalid-socket').stringify_json({"message": "test-message"})
    self.assertEqual(json_str, b'{"message": "test-message"} \x0c')

  @staticmethod
  def start_server():
    cmd = "pm2 start ./app/server/ipc-server.js > /dev/null"
    os.system(cmd)
    # TODO: find a reliable way to indicate that server is up
    #       (instead of using magic numbers)
    time.sleep(1)

  @staticmethod
  def stop_server():
    cmd = "pm2 stop all > /dev/null"
    os.system(cmd)

  def test_ipc_connection(self):
    TestingIpcClient.start_server()
    events = get_ipc_events()
    ipcConst = get_ipc_const()
    try:
      with IpcClient(ipcConst['RPCAM_CAPTURE_SOCKET']) as client:
        out_msg = Media.format_msg(events["RPCAM_MOTION_DETECTED"], 'test')
        client.income_observable.subscribe(lambda msg: client.stop())
        client.send(out_msg)
        client.close()
    finally:
      TestingIpcClient.stop_server()

  def test_income_observable(self):
    ipcConst = get_ipc_const()
    client = IpcClient(ipcConst['RPCAM_CAPTURE_SOCKET'])
    client.income_observable.subscribe(lambda msg: self.assertEqual(msg, 123))
    client._income_observer.on_next(123)


if __name__ == '__main__':
  unittest.main()
