import os
import time

class Camera(object):
    def __init__(self, motionDetection):
        self.motionDetection = motionDetection

    def capture(self, num):
        time.sleep(num)
        return [os.path.join(os.getcwd(), 'app/media/test/test.png')]

    def video(self, sec):
        time.sleep(sec)
        return os.path.join(os.getcwd(), 'app/media/test/test.mp4')