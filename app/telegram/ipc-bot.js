const ipc = require('node-ipc');
const ipcEvents = require('../core/events.json');
const telegram_bot = require('./bot');
const log = require('debug')('ipc:bot');
const ipcConst = require('../core/ipc-const.json');

ipc.config.id = 'telegram_bot';
ipc.config.retry = 1000;


const botIpcBridge = {
  emit: function (cmd, payload) {
    ipc.of[ipcConst.RPCAM_SERRVER_ID].emit(cmd, {
      id: ipc.config.id,
      payload: payload
    });
  },
  capture: function (num) {
    botIpcBridge.broadcast(ipcEvents.RPCAM_CAPTURE, { num: num });
  },
  recordVideo: function (sec) {
    botIpcBridge.broadcast(ipcEvents.RPCAM_VIDEO_RECORD, { sec: sec });
  },
  startMotionDetection: function () {
    botIpcBridge.broadcast(ipcEvents.RPCAM_START_MOTION_DETECTION);
  },
  stopMotionDetection: function () {
    botIpcBridge.broadcast(ipcEvents.RPCAM_STOP_MOTION_DETECTION);
  },
};

ipc.connectTo(ipcConst.RPCAM_SERRVER_ID, ipcConst.RPCAM_CAPTURE_SOCKET, () => {
  const server = ipc.of[ipcConst.RPCAM_SERRVER_ID];
  server.on(ipcEvents.CONNECT, () => {
    telegram_bot.start(botIpcBridge)
      .then(() => log('telegram_bot STARTED'))
      .catch(err => log(err));
  });

  server.on(ipcEvents.RPCAM_CAPTURE_READY, data => {
    log(ipcEvents.RPCAM_CAPTURE_READY, data);
    telegram_bot.sendImage(data.payload);
  });

  server.on(ipcEvents.RPCAM_VIDEO_RECORD_READY, data => {
    log(ipcEvents.RPCAM_VIDEO_RECORD_READY, data);
    telegram_bot.sendVideo(data.payload);
  });
  server.on(ipcEvents.RPCAM_MOTION_DETECTED, (data) => {
    log(ipcEvents.RPCAM_MOTION_DETECTED, data);
    telegram_bot.onMotionDetected(data.payload);
  });
  server.on(ipcEvents.DISCONNECT, () => {
    log(`disconnected from ${ipcConst.RPCAM_SERRVER_ID}`);
  });

  log(ipc.of.rpcam.destroy);
});