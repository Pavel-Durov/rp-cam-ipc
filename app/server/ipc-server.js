const ipc = require('node-ipc');
const log = require('debug')('ipc:server');
const events = require('../core/events.json');
const {
  RPCAM_SERRVER_ID,
  RPCAM_SERRVER_RETRY,
  RPCAM_CAPTURE_SOCKET
} = require('../core/ipc-const.json');

ipc.config.id = RPCAM_SERRVER_ID;
ipc.config.retry = RPCAM_SERRVER_RETRY;
ipc.config.logger = (a) => log(a);

ipc.serve(RPCAM_CAPTURE_SOCKET, () => {
  // ipc.server.on(events.RPCAM_CAPTURE, (data) => {
  //   ipc.server.broadcast(events.RPCAM_CAPTURE, data);
  // });
  // ipc.server.on(events.RPCAM_CAPTURE_READY, (data) => {
  //   ipc.server.broadcast(events.RPCAM_CAPTURE_READY, data);
  // });
  // ipc.server.on(events.RPCAM_VIDEO_RECORD, (data) => {
  //   ipc.server.broadcast(events.RPCAM_VIDEO_RECORD, data);
  // });
  // ipc.server.on(events.RPCAM_VIDEO_RECORD_READY, (data) => {
  //   ipc.server.broadcast(events.RPCAM_VIDEO_RECORD_READY, data);
  // });
  // ipc.server.on(events.RPCAM_MOTION_DETECTED, (data) => {
  //   ipc.server.broadcast(events.RPCAM_MOTION_DETECTED, data);
  // });
});

ipc.server.start();

module.exports = {
  stop: () => {
    ipc.server.stop();
  }
};
