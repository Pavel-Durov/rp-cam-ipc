import os
import sys
import time
import logging
import fs_util
from picamera import PiCamera

class Camera(object):
    def __init__(self, motionDetection):
        self.logger = logging.getLogger('Camera')
        self.motionDetection = motionDetection
        self.cam = PiCamera()

    def capture(self, num):
        result = []
        for i in range(0, num):
            file_path = None
            try:
                self.logger.info('CAPTURING IN PROCESS')
                file_path = fs_util.generate_img_full_path(fs_util.IMG_GENERAL)
                self.cam.capture(file_path, use_video_port=True)
                result.append(file_path)
            except:
                self.logger.error(sys.exc_info()[0])

        self.logger.info(result)
        return result

    def video(self, sec):
        time.sleep(sec)
        return os.path.join(os.getcwd(), 'app/media/test/test.mp4')
