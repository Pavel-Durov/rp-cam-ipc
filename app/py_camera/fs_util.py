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
IMG_GENERAL = 'global'
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

def __generate_img_name():
    return __get_timestamp_str() + JPEG_EXTENTION

def __generate_video_name():
    return __get_timestamp_str() + H264_EXTENTION

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

def __create_img_dir(name):
    full_path = os.path.join(MEDIA_DIR, name)
    pathlib.Path(full_path).mkdir(parents=True, exist_ok=True)

def create_dirs():
    pathlib.Path(MEDIA_DIR).mkdir(parents=True, exist_ok=True)
    for dir_name in __get_dir_names():
        __create_img_dir(dir_name)

def append_full_path(media_file):
    directory = os.path.join(os.getcwd(), MEDIA_DIR, dir_type)
    return os.path.join(directory, name)


def generate_img_full_path(dir_type):
    name = __generate_img_name()
    directory = os.path.join(os.getcwd(), MEDIA_DIR, dir_type)
    return os.path.join(directory, name)

def generate_video_full_path(dur_type):
    name = __generate_video_name()
    directory = os.path.join(os.getcwd(), MEDIA_DIR, dir_type)
    return os.path.join(directory, name)

