import logging
from fs.util import get_ipc_const, get_ipc_events, create_dirs
from ipc.media import IpcMedia

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

def start(ipc_socket, ipc_event):
    create_dirs()
    media = IpcMedia()
    media.run(ipc_socket, ipc_event)
    
if __name__ == '__main__':
    ipcConst = get_ipc_const()
    events = get_ipc_events()
    start(ipcConst['RP_CAM_CAPTURE_SOCKET'], events)
