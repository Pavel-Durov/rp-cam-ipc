const ipc = require('node-ipc');
const log = require('debug')('ipc:server');
const {
  RPCAM_CAPTURE,
  RPCAM_CAPTURE_READY
} = require('../core/events.json');
const {
  RPCAM_SERRVER_ID,
  RPCAM_SERVER_RETRY,
  RPCAM_CAPTURE_SOCKET,
  RPCAM_VIDEO_RECORD,
  RPCAM_VIDEO_RECORD_READY,
  RPCAM_MOTION_DETECTED,
  RPCAM_START_MOTION_DETECTION,
  RPCAM_STOP_MOTION_DETECTION
} = require('../core/ipc-const.json');

ipc.config.id = RPCAM_SERRVER_ID;
ipc.config.retry = RPCAM_SERVER_RETRY;
ipc.config.logger = (a) => log(a);

ipc.serve(RPCAM_CAPTURE_SOCKET, () => {
  ipc.server.on(RPCAM_CAPTURE, (data) => {
    ipc.server.broadcast(RPCAM_CAPTURE, data);
  });
  ipc.server.on(RPCAM_CAPTURE_READY, (data) => {
    ipc.server.broadcast(RPCAM_CAPTURE_READY, data);
  });
  ipc.server.on(RPCAM_VIDEO_RECORD, (data) => {
    ipc.server.broadcast(RPCAM_VIDEO_RECORD, data);
  });
  ipc.server.on(RPCAM_VIDEO_RECORD_READY, (data) => {
    ipc.server.broadcast(RPCAM_VIDEO_RECORD_READY, data);
  });
  ipc.server.on(RPCAM_MOTION_DETECTED, (data) => {
    ipc.server.broadcast(RPCAM_MOTION_DETECTED, data);
  });
  ipc.server.on(RPCAM_START_MOTION_DETECTION, (data) => {
    ipc.server.broadcast(RPCAM_START_MOTION_DETECTION, data);
  });
  ipc.server.on(RPCAM_STOP_MOTION_DETECTION, (data) => {
    ipc.server.broadcast(RPCAM_STOP_MOTION_DETECTION, data);
  });
});

ipc.server.start();

module.exports = {
  stop: () => {
    ipc.server.stop();
  }
};
