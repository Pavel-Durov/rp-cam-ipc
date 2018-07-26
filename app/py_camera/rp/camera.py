import os
import sys
import time
import logging
from fs.util import generate_H264_absolute_file_name, generate_JPEG_absolute_file_name
import picamera
import datetime

class Camera(object):
    RECORDING_TIME_MIN_SEC = 1
    CAM_RESOLUTION = (1024, 768)
    CAM_FRAMERATE = 30

    def __init__(self, motionDetection):
        self.logger = logging.getLogger('Camera')
        self.motionDetection = motionDetection
        self.cam = picamera.PiCamera()
        self.set_config()
        self.action = NONE
    
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
                self.logger.info('captire in progress')
                file_path = generate_img_path(fs_util.IMG_GENERAL)
                self.cam.capture(file_path, use_video_port=True)
                result.append(file_path)
            except:
                self.logger.error(sys.exc_info())

        self.logger.info(result)
        return result
    
    def __normalize_rec_time(self, sec):
        result = sec
        if sec < RECORDING_TIME_MIN_SEC:
            result = RECORDING_TIME_MIN_SEC
        return result
     
    def video(self, sec):
        path = None
        try:
            path = generate_video_path(fs_util.VIDEO_GENERAL)
            sec = self.__normalize_rec_time(sec)
            self.logger.info('recording started, {}, {} sec'.format(path, sec))
            self.cam.start_recording(path)
            self.cam.wait_recording(sec)
            self.cam.stop_recording()
        except:
            self.logger.error(sys.exc_info())

        return path

    def start_motion_detection(self):
        try:
            with MotionDetector(self.cam) as detector:
                self.cam.start_recording('/dev/null', format='h264', motion_output=detector)
                while True:
                    while not detector.is_detected:
                        self.logger.info('waiting for motion...')
                        self.cam.wait_recording(1)

                self.cam.stop_recording()
        except:
            self.logger.error(sys.exc_info())
       

class MotionDetector(picamera.array.PiMotionAnalysis):
    STILL_INTEVAL_MIN = 5
    __motion_detected = False
    
    def __init__(self):
        self.logger = logging.getLogger('MotionDetector')
        last_still_capture_time = datetime.datetime.now()
    
    def is_detected(self):
        return self.__motion_detected
    
    def time_diff(self):
        delta = datetime.timedelta(seconds=self.STILL_INTEVAL_MIN)
        return datetime.datetime.now() > self.last_still_capture_time + delta

    def analyse(self, a):
        self.__motion_detected = False
        if self.time_diff():
            self.last_still_capture_time = datetime.datetime.now()
            x = np.square(a['x'].astype(np.float)) 
            y = np.square(a['y'].astype(np.float))
            
            a = np.sqrt(x + y).clip(0, 255).astype(np.uint8)

            if (a > 60).sum() > 10:
                self.logger.info('motion detected')
                self.__motion_detected = True