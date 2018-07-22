import fs_util
import logging
from ipc import IpcCamera

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

if __name__ == '__main__':
    ipcConst = fs_util.get_ipc_const()
    events = fs_util.get_ipc_events()
    camIpc = IpcCamera(ipcConst['RP_CAM_CAPTURE_SOCKET'], events)
    fs_util.create_dirs()
    camIpc.start_co()
