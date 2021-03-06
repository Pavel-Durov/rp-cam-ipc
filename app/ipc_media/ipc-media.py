import logging
from fs.util import get_ipc_const, get_ipc_events, create_dirs
from ipc.media import Media

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(ipc_socket, motion_detection_length_sec, ipc_event):
  create_dirs()
  media = Media(motion_detection_length_sec)
  media.run(ipc_socket, ipc_event)


if __name__ == '__main__':
  ipcConst = get_ipc_const()
  events = get_ipc_events()
  start(ipcConst['RPCAM_CAPTURE_SOCKET'], ipcConst['RPCAM_MOTION_DETECTION_LENGTH_SEC'], events)
