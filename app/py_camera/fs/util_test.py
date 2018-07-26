import re
import unittest
import fs.util as util

class TestingFsUtils(unittest.TestCase):

    def test_ipc_const(self):
        ipc_const = util.get_ipc_const()
        self.assertTrue("RPCAM_SERRVER_ID" in ipc_const)
        self.assertTrue("RP_CAM_CAPTURE_SOCKET" in ipc_const)
        
    def test_ipc_events(self):
        ipc_events = util.get_ipc_events()
        self.assertTrue("RPCAM_CAPTURE" in ipc_events)
        self.assertTrue("RPCAM_CAPTURE_READY" in ipc_events)
        self.assertTrue("RPCAM_VIDEO_RECORD" in ipc_events)
        self.assertTrue("RPCAM_VIDEO_RECORD_READY" in ipc_events)
        self.assertTrue("RPCAM_MOTION_DETECTED" in ipc_events)
    
    def test_generate_img_file_name(self):
        self.__file_path_test(util.IMG_GENERAL, 
                              util.JPEG_EXTENTION, 
                              util.generate_JPEG_absolute_file_name)

    def test_generate_H264_video_file_name(self):
        self.__file_path_test(util.VIDEO_GENERAL, 
                              util.H264_EXTENTION, 
                              util.generate_H264_absolute_file_name)

    def test_generate_MP4_video_file_name(self):
        self.__file_path_test(util.MOTION_DETECTION, 
                              util.MP4_EXTENTION, 
                              util.generate_MP4_absolute_file_name)
    
    def __file_path_test(self, directory, extention, func):
        file_name = func(directory)
        exp = "\/{}\/\w*\{}(?=\s|$)".format(directory, extention)
        regex_search = re.search(exp, file_name)
        self.assertTrue(regex_search)

if __name__ == '__main__':
    unittest.main()