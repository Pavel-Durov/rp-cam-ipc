import re
import unittest
from rp.camera import Camera


class TestingCamera(unittest.TestCase):

  def test_json_stringify(self):
    camera = Camera(lambda: 'on motion detected')
    self.assertEqual(camera._on_motion_detected(), 'on motion detected')


if __name__ == '__main__':
  unittest.main()
