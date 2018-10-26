import os
import sys
import time
import logging
import fs.util as fs
import datetime
import numpy as np
from threading import Thread

RP_CONTEXT = True
try:
  import picamera
  import picamera.array
except ImportError:
  RP_CONTEXT = False


class Camera(object):
  RECORDING_LENGTH_MIN_SEC = 1
  CAM_RESOLUTION_SD = (640, 480)
  CAM_RESOLUTION_HD = (1280, 720)
  CAM_FRAMERATE = 24
  _on_motion_detected = None

  def __init__(self, on_motion_detected):
    self.logger = logging.getLogger('Camera')
    self._on_motion_detected = on_motion_detected
    self._set_cam()
    self._set_default_config()
    self.action = None

  def _set_cam(self):
    if RP_CONTEXT:
      self.cam = picamera.PiCamera()
    else:
      self.cam = MockedCamera()

  def dispose(self):
    self.cam.close()

  def _set_default_config(self):
    self.set_config(self.CAM_RESOLUTION_HD)

  def set_config(self, resolution):
    self.cam.resolution = resolution
    self.cam.framerate = self.CAM_FRAMERATE

  def capture(self, num):
    result = []
    for _ in range(0, num):
      try:
        path = fs.generate_JPEG_absolute_file_name(fs.IMG_GENERAL)
        self.logger.info('capture in progress {}'.format(path))
        self.cam.capture(path, use_video_port=True)
        result.append(path)
      except:
        self.logger.error(sys.exc_info())

    self.logger.info('capture result {}'.format(result))
    return result

  def _normalize_rec_time(self, sec):
    result = sec
    if sec < self.RECORDING_LENGTH_MIN_SEC:
      result = self.RECORDING_LENGTH_MIN_SEC
    return result

  def convert(self, path):
    self.logger.info('RUNNING H263 to MP4 convetion')
    return fs.convert_h264_to_mp4(path)

  def video(self, sec):
    path = None
    try:
      path = fs.generate_H264_absolute_file_name(fs.VIDEO)
      sec = self._normalize_rec_time(sec)
      self.logger.info('recording started, {}, {} sec'.format(path, sec))
      self.cam.start_recording(path)
      self.cam.wait_recording(sec)
      self.cam.stop_recording()
      path = self.convert(path)
      if not RP_CONTEXT:
        path = '/home/ubuntu/workspace/app/media/test/big_buck_bunny.mp4'
    except:
      self.logger.error(sys.exc_info())
    return path

  def detect_motion(self, sec):
    try:
      with MotionDetector(self.cam) as output:
        path = fs.generate_H264_absolute_file_name(fs.MOTION_DETECTION)
        self.logger.info(
            'motion_detection: path: {}, length: {}'.format(path, sec))
        self.set_config(self.CAM_RESOLUTION_SD)
        self.cam.start_recording(path, motion_output=output)
        self.cam.wait_recording(sec)
        self.cam.stop_recording()
        if(output.motion_detected):
          convened_path = self.convert(path)
          self._on_motion_detected(convened_path)
        self.logger.info('deleting file: {}'.format(path)
        fs.delete_file(path)
    except:
      self.logger.error(sys.exc_info())
    finally:
      self._set_default_config()


if RP_CONTEXT:
  # Source: https://picamera.readthedocs.io/en/release-1.10/api_array.html
  class MotionDetector(picamera.array.PiMotionAnalysis):
    motion_detected=False

    def analyse(self, a):
      a=np.sqrt(
          np.square(a['x'].astype(np.float)) +
          np.square(a['y'].astype(np.float))
      ).clip(0, 255).astype(np.uint8)
      # If there're more than 10 vectors with a magnitude greater
      # than 60, then say we've detected motion
      if (a > 60).sum() > 10:
        self.motion_detected=True

else:
  logger=logging.getLogger('MockedCamera')

  class MockedCamera(object):
    resolution=0
    framerate=0

    def __init__(self):
      self.logger=logging.getLogger('MockedCamera')

    def capture(self, file_path, use_video_port):
      self.logger.info('capture')

    @staticmethod
    def start_recording(sepath, format, motion_output=None):
      logger.info('start_recording')

    @staticmethod
    def wait_recording(sec):
      logger.info('wait_recording:s‰tart')
      time.sleep(sec)
      logger.info('wait_recording:stop')

    @staticmethod
    def stop_recording():
      logger.info('stop_recording')

    @staticmethod
    def close(self):
      logger.info('CLOSE')

  class MotionDetector():
    analyse_started=False

    def __init__(self, cam):
      self.cam=cam

    def analyse(self, a):
      self.analyse_started=True
