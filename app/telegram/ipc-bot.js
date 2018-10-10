const ipc = require('node-ipc');
const ipcEvents = require('../core/events.json');
const telegram_bot = require('./bot');
const logger = require('../core/logger');
const ipcConst = require('../core/ipc-const.json')

const LOG_TAG = 'ipc:telegram-bot-client';
ipc.config.id = 'telegram_bot';
ipc.config.retry = 1000;


const botIpcBridge = {
  emit: (cmd, payload) => {
    ipc.of[ipcConst.RPCAM_SERRVER_ID].emit(cmd, {
      id: ipc.config.id,
      payload: payload
    });
  },
  capture: num => {
    botIpcBridge.emit(ipcEvents.RPCAM_CAPTURE, { num: num });
  },
  recordVideo: sec => {
    botIpcBridge.emit(ipcEvents.RPCAM_VIDEO_RECORD, { sec: sec });
  }
};

ipc.connectTo(ipcConst.RPCAM_SERRVER_ID, ipcConst.RPCAM_CAPTURE_SOCKET, () => {
  const server = ipc.of[ipcConst.RPCAM_SERRVER_ID];
  server.on(ipcEvents.CONNECT, () => {
    telegram_bot.start(botIpcBridge)
      .then(tbot => logger.info(LOG_TAG, 'telegram_bot STARTED'))
      .catch(err => logger.error(LOG_TAG, err));
  });

  server.on(ipcEvents.RPCAM_CAPTURE_READY, data => {
    logger.info(LOG_TAG, ipcEvents.RPCAM_CAPTURE_READY, data)
    telegram_bot.sendImage(data.payload);
  });

  server.on(ipcEvents.RPCAM_VIDEO_RECORD_READY, data => {
    logger.info(LOG_TAG, ipcEvents.RPCAM_VIDEO_RECORD_READY, data)
    telegram_bot.sendVideo(data.payload);
  });

  server.on(ipcEvents.DISCONNECT, () => {
    logger.info(LOG_TAG, `disconnected from ${ipcConst.RPCAM_SERRVER_ID}`);
  });

  logger.info(LOG_TAG, ipc.of.rpcam.destroy);
});