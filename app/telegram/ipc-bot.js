const ipc = require('node-ipc');
const ipcEvents = require('../core/events.json');
const telegram_bot = require('./bot');
const logger = require('../core/logger');
const ipcConst = require('../core/ipc-const.json')

const LOG_TAG = 'ipc:telegram-bot-client';
ipc.config.id = 'telegram_bot';
ipc.config.retry = 1000;

ipc.connectTo(ipcConst.RPCAM_SERRVER_ID, ipcConst.RP_CAM_CAPTURE_SOCKET, () => {
    const botIpcBridge = {
        emit: (cmd, payload) => {
            ipc.of.rpcam.emit(cmd, {
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

    ipc.of.rpcam.on(ipcEvents.CONNECT, () => {
        telegram_bot.start(botIpcBridge)
            .then(tbot => logger.info(LOG_TAG, 'telegram_bot STARTED'))
            .catch(err => logger.error(LOG_TAG, err));
    });

    ipc.of.rpcam.on(ipcEvents.RPCAM_CAPTURE_READY, data => {
        logger.info(LOG_TAG, ipcEvents.RPCAM_CAPTURE_READY, data)
        telegram_bot.sendImage(data.payload);
    });

    ipc.of.rpcam.on(ipcEvents.RPCAM_VIDEO_RECORD_READY, data => {
        logger.info(LOG_TAG, ipcEvents.RPCAM_VIDEO_RECORD_READY, data)
        telegram_bot.sendVideo(data.payload);
    });

    ipc.of.rpcam.on(ipcEvents.DISCONNECT, () => {
        ipc.log('disconnected from world');
    });

    console.log(ipc.of.rpcam.destroy);
});
