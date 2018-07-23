import json
import os
import time
import pathlib
import calendar

IPC_CONST_JSON_FILE = 'app/core/ipc-const.json'
IPC_EVENTS_JSON_FILE = 'app/core/events.json'

H264_EXTENTION = '.h264'
JPEG_EXTENTION = '.jpg'
MEDIA_DIR = 'app/media/'
CAT_FACIAL = 'cat_facial'
HUMAN_FACIAL = 'human_facial'
HUMAN_FULL_BODY = 'human_full_body'
HUMAN_UPPER_BODY = 'human_upper_body'
IMG_GENERAL = 'general'
VIDEO_GENERAL = 'general'
MOTION_DETECTION = 'motion_detection'
VIDEO = 'video'

def get_ipc_const():
    with open(os.path.join(os.getcwd(), IPC_CONST_JSON_FILE)) as f:
        jsonConst = json.load(f)
        return jsonConst

def get_ipc_events():
    with open(os.path.join(os.getcwd(), IPC_EVENTS_JSON_FILE)) as f:
        jEvent = json.load(f)
        return jEvent

def __generate_file_name(ext):
    return __get_timestamp_str() + ext

def __get_timestamp_str():
    return str(calendar.timegm(time.gmtime()))

def __get_dir_names():
    return [CAT_FACIAL,
            HUMAN_FACIAL,
            HUMAN_FULL_BODY,
            HUMAN_UPPER_BODY,
            IMG_GENERAL,
            MOTION_DETECTION,
            VIDEO]

def __create_dir(name):
    full_path = os.path.join(MEDIA_DIR, name)
    pathlib.Path(full_path).mkdir(parents=True, exist_ok=True)

def __create_meda_dir():
    pathlib.Path(MEDIA_DIR).mkdir(parents=True, exist_ok=True)

def create_dirs():
    for dir_name in __get_dir_names():
        __create_dir(dir_name)

def __append_full_path(media_file):
    directory = os.path.join(os.getcwd(), MEDIA_DIR, dir_type)
    return os.path.join(directory, name)

def generate_img_path(dir_type):
    name = __generate_file_name(JPEG_EXTENTION)
    return __append_full_path(name)

def generate_video_path(dur_type):
    name = __generate_file_name(H264_EXTENTION)
    return __append_full_path(name)