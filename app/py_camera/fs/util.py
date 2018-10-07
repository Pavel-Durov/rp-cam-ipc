import os
import time
import json
import calendar

IPC_CONST_JSON_FILE = 'app/core/ipc-const.json'
IPC_EVENTS_JSON_FILE = 'app/core/events.json'

MP4_EXTENTION = '.mp4'
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


def __create_dir(dir_path):
  os.makedirs(dir_path, exist_ok=True)


def create_dirs():
  __create_dir(MEDIA_DIR)
  for dir_name in __get_dir_names():
    path = os.path.join(MEDIA_DIR, name)
    __create_dir(path)


def generate_JPEG_absolute_file_name(dir_type):
  name = __generate_file_name(JPEG_EXTENTION)
  return __append_full_path(name, dir_type)


def generate_H264_absolute_file_name(dir_type):
  name = __generate_file_name(H264_EXTENTION)
  return __append_full_path(name, dir_type)


def generate_MP4_absolute_file_name(dir_type):
  name = __generate_file_name(MP4_EXTENTION)
  return __append_full_path(name, dir_type)


def __append_full_path(media_file, dir_type):
  directory = os.path.join(os.getcwd(), MEDIA_DIR, dir_type)
  return os.path.join(directory, media_file)


def __generate_file_name(ext):
  return __get_timestamp_str() + ext
