import re
import unittest
from ipc.client import IpcClient


class TestingFsUtils(unittest.TestCase):

  def test_json_stringify(self):
    json_str = IpcClient(
        'invalid-socke').stringify_json({"message": "test-message"})
    self.assertEqual(json_str, b'{"message": "test-message"} \x0c')


if __name__ == '__main__':
  unittest.main()
