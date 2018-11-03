const telegram = require('telegram-bot-api');
const { parse } = require('./commands');
const log = require('debug')('bot');
const fs = require('fs');
const { promisify } = require('util');
const { isEmpty } = require('ramda');

const STR = {
  SUB_SUCCESS: 'Thanks for subscribing👍',
  UNSUB_ERROR: '',
  UNSUB_SUCCESS: 'Sad to see you leaving...',
  SUB_FAIL_EXIST: 'Ooops, already subscribed 😞',
  UNKNOWN_CMD: 'UNKNOWN COMMAND 😠'
};


async function deleteFile(path) {
  log(`Deleting file, ${path}`, typeof (path));
  await promisify(fs.unlink)(path);
  log(`${path} was deleted`);
}

const bot = {
  SUBSCRIBERS: [],
  ipc: {},
  api: {},
  takeImage: num => bot.ipc.capture(num),
  recordVideo: sec => bot.ipc.recordVideo(sec),
  sendMessage: msg => {
    bot.notify(id => bot.api.sendMessage({ chat_id: id, text: msg }));
  },
  subscribe: id => {
    let msg = STR.SUB_SUCCESS;
    if (bot.SUBSCRIBERS.indexOf(id) > -1) {
      msg = STR.SUB_FAIL_EXIST;
    } else {
      bot.SUBSCRIBERS.push(id);
    }
    if (isEmpty(bot.SUBSCRIBERS)) {
      bot.ipc.startMotionDetection();
    } else {
      bot.ipc.stopMotionDetection();
    }
    bot.sendMessage(msg);
  },
  unsubscribe: id => {
    const index = bot.SUBSCRIBERS.indexOf(id);
    if (index != -1) {
      bot.sendMessage(STR.UNSUB_SUCCESS);
      bot.SUBSCRIBERS.pop(index);
    }
  },
  sendImage: async (imgPaths) => {
    const promises = (imgPaths || []).map(async path => {
      await bot.notify(async function (id) {
        await bot.api.sendPhoto({
          chat_id: id,
          caption: (new Date()).toLocaleString(),
          photo: path
        });
      });
      await deleteFile(path);
    });
    return Promise.all(promises);
  },
  sendVideo: async (path, caption) => {
    log(`sending video ${path}`);
    await bot.notify(async function (id) {
      await bot.api.sendVideo({ chat_id: id, caption: caption, video: path });
    });

    await deleteFile(path);
  },
  onMotionDetected: (videoPath) => {
    bot.sendVideo(videoPath, `🕵️ Motion Detected, ${(new Date()).toLocaleString()}`);
  },
  notify: asyncFunc => {
    log('notify,', bot.SUBSCRIBERS);
    const promises = (bot.SUBSCRIBERS || []).map(async (id) => {
      try {
        const data = await asyncFunc(id);
        log(data);
      } catch (e) {
        log(e);
      }
    });
    return Promise.all(promises);
  },
  setApi: (api) => {
    bot.api = api;
  },
  start: async (botIpc) => {
    bot.ipc = botIpc;
    const api = new telegram({
      token: process.env.TELEGRAM_BOT_TOKEN,
      updates: {
        enabled: true,
        get_interval: 1000
      }
    });
    await api.getMe();
    bot.setApi(api);
    bot.start_listening();
  },
  start_listening: () => {
    bot.api.on('message', message => {
      const { chat: { id }, text } = message;
      const cmd = parse(text);
      if (cmd) {
        bot.sendMessage('PROCESSING 🤓');
        cmd.action(id, bot);
      } else {
        bot.sendMessage(STR.UNKNOWN_CMD);
      }
    });
  }
};

module.exports = bot;