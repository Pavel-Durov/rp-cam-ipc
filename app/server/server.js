const ipc = require('node-ipc');
const events = require('../core/events.json');
const ipcConst = require('../core/ipc-const.json')

ipc.config.id = ipcConst.RPCAM_SERRVER_ID;
ipc.config.retry = ipcConst.RPCAM_SERRVER_RETRY;

ipc.serve(ipcConst.RP_CAM_CAPTURE_SOCKET, () => {
    ipc.server.on(events.RPCAM_CAPTURE, (data) => {
        ipc.log(events.RPCAM_CAPTURE);
        ipc.server.broadcast(events.RPCAM_CAPTURE, data);
    });
    ipc.server.on(events.RPCAM_CAPTURE_READY, (data) => {
        ipc.log(events.RPCAM_CAPTURE_READY);
        ipc.server.broadcast(events.RPCAM_CAPTURE_READY, data);
    });
    ipc.server.on(events.RPCAM_VIDEO_RECORD, (data) => {
        ipc.log(events.RPCAM_VIDEO_RECORD)
        ipc.server.broadcast(events.RPCAM_VIDEO_RECORD, data);
    });
    ipc.server.on(events.RPCAM_VIDEO_RECORD_READY, (data) => {
        ipc.log(events.RPCAM_VIDEO_RECORD_READY, data)
        ipc.server.broadcast(events.RPCAM_VIDEO_RECORD_READY, data);
    });
    ipc.server.on(events.RPCAM_MOTION_DETECTED, (data) => {
        ipc.log(events.RPCAM_MOTION_DETECTED, data)
        ipc.server.broadcast(events.RPCAM_MOTION_DETECTED, data);
    });
});

ipc.server.start();
