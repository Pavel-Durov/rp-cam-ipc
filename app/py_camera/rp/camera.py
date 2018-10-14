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
  RECORDING_TIME_MIN_SEC = 1
  CAM_RESOLUTION = (1024, 768)
  CAM_FRAMERATE = 30

  def __init__(self, on_motion_detected):
    self.logger = logging.getLogger('Camera')
    self.on_motion_detected = on_motion_detected
    if RP_CONTEXT:
      self.cam = picamera.PiCamera()
    else:
      self.cam = MockedCamera()
    self.set_config()
    self.action = None

  def dispose(self):
    self.cam.close()

  def set_config(self):
    self.cam.resolution = self.CAM_RESOLUTION
    self.cam.framerate = self.CAM_FRAMERATE

  def capture(self, num):
    result = []
    for i in range(0, num):
      file_path = None
      try:
        self.logger.info('capture in progress')
        file_path = fs.generate_JPEG_absolute_file_name(fs.IMG_GENERAL)
        self.cam.capture(file_path, use_video_port=True)
        if not RP_CONTEXT:
          file_path = 'https://chocolatey.org/content/packageimages/nodejs.10.7.0.png'
        result.append(file_path)
      except:
        self.logger.error(sys.exc_info())

    self.logger.info('capture result {}'.format(result))
    return result

  def __normalize_rec_time(self, sec):
    result = sec
    if sec < self.RECORDING_TIME_MIN_SEC:
      result = self.RECORDING_TIME_MIN_SEC
    return result

  def convert(self, path):
    try:
      convertedPath = path.replace("h264", "mp4")
      cmd = "MP4Box -fps 20 -add {} {} ".format(path, convertedPath)
      self.logger.info('RUNNING H263 to MP4 convetion')
      self.logger.info(cmd)
      os.system(cmd)
      return convertedPath
    except:
      self.logger.error(
          'Error on h264-mp4 convertion {}'.format(sys.exc_info()))

  def video(self, sec):
    path = None
    try:
      path = fs.generate_H264_absolute_file_name(fs.VIDEO)
      sec = self.__normalize_rec_time(sec)
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
      self.logger.info('motion_detection: started')
      with MotionDetector(self.cam) as output:
        self.logger.info('motion_detection: start_recording')
        self.cam.start_recording('/dev/null', format='h264', motion_output=output)
        self.cam.wait_recording(sec)
        self.cam.stop_recording()
        if(output.motion_detected):
          self.on_motion_detected()
    except:
      self.logger.error(sys.exc_info())

if RP_CONTEXT:
  # Source: https://picamera.readthedocs.io/en/release-1.10/api_array.html
  class MotionDetector(picamera.array.PiMotionAnalysis):
    motion_detected = False
    def analyse(self, a):
      a = np.sqrt(
          np.square(a['x'].astype(np.float)) +
          np.square(a['y'].astype(np.float))
          ).clip(0, 255).astype(np.uint8)
      # If there're more than 10 vectors with a magnitude greater
      # than 60, then say we've detected motion
      if (a > 60).sum() > 10:
        self.motion_detected = True

else:
  class MockedCamera(object):
    resolution = 0
    framerate = 0

    def __init__(self):
      self.logger = logging.getLogger('MockedCamera')

    def capture(self, file_path, use_video_port):
      self.logger.info('capture')

    def start_recording(path, format, motion_output=None):
      self.logger.info('start_recording')

    def wait_recording(sec):
      self.logger.info('wait_recording:s‰tart')
      time.sleep(sec)
      self.logger.info('wait_recording:stop')

    def stop_recording():
      self.logger.info('stop_recording')

    def close(self):
      self.logger.info('CLOSE')
