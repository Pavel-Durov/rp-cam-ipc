import os
import sys
import time
import logging
import fs.util as fs 
import datetime

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

    def __init__(self, motionDetection):
        self.logger = logging.getLogger('Camera')
        self.motionDetection = motionDetection
        if RP_CONTEXT:
            self.cam = picamera.PiCamera()
        else:
            self.cam = MockedCamera();
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
                    file_path = 'https://chocolatey.org/content/packageimages/nodejs.10.7.0.png';
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
     
    def video(self, sec):
        path = None
        try:
            path = fs.generate_MP4_absolute_file_name(fs.VIDEO_GENERAL)
            sec = self.__normalize_rec_time(sec)
            self.logger.info('recording started, {}, {} sec'.format(path, sec))
            self.cam.start_recording(path)
            self.cam.wait_recording(sec)
            self.cam.stop_recording()
            if not RP_CONTEXT:
                path = '/home/ubuntu/workspace/app/media/test/big_buck_bunny.mp4'
                
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
       
if RP_CONTEXT:
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
            self.logger.info('wait_recording:start')
            time.sleep(sec)
            self.logger.info('wait_recording:stop')

        def stop_recording():
            self.logger.info('stop_recording')

        def close(self):
            self.logger.info('CLOSE')
            
