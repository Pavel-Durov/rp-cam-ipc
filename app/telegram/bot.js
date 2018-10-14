const telegram = require('telegram-bot-api');
const commands = require('./commands');
const log = require('debug')('bot');
const fs = require('fs');

const STR = {
  SUB_SUCCESS: 'Thanks for subscribing👍',
  UNSUB_ERROR: '',
  UNSUB_SUCCESS: 'Sad to see you leaving...',
  SUB_FAIL_EXIST: 'Ooops, already subscribed 😞',
  UNKNOWN_CMD: 'UNKNOWN COMMAND 😠'
};

function deleteFile(path) {
  log(`Deleting file, ${path}`);
  fs.unlink(path, (err) => {
    if (err) throw err;
    log(`${path} was deleted`);
  });
}

const bot = {
  SUBSCRIBERS: [],
  ipc: {},
  api: {},
  takeImage: num => bot.ips.capture(num),
  recordVideo: sec => bot.ips.recordVideo(sec),
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
    bot.sendMessage(msg);
  },
  unsubscribe: id => {
    const index = bot.SUBSCRIBERS.indexOf(id);
    if (index != -1) {
      bot.sendMessage(STR.UNSUB_SUCCESS);
      bot.SUBSCRIBERS.pop(index);
    }
  },
  sendImage: imgPaths => {
    (imgPaths || []).forEach(async path => {
      await bot.notify(async function (id) {
        return bot.api.sendPhoto({
          chat_id: id,
          caption: (new Date()).toLocaleString(),
          photo: path
        });
      });
    });
  },
  sendVideo: async (path, caption) => {
    await bot.notify(async function (id) {
      return bot.api.sendVideo({ chat_id: id, caption: caption, video: path });
    });
    deleteFile(path);
  },
  onMotionDetected: (path) => {
    bot.sendVideo(path, '🕵️ Motion Detected');
  },
  notify: func => {
    log('notify,', bot.SUBSCRIBERS);
    const promises = (bot.SUBSCRIBERS || []).map(async (id) => {
      try {
        const data = await func(id);
        log(data);
      } catch (e) {
        log(e);
      }
    });
    return Promise.all(promises);
  },
  start: botIpc => {
    bot.ips = botIpc;
    return new Promise((resolve, reject) => {
      bot.api = new telegram({
        token: process.env.TELEGRAM_BOT_TOKEN,
        updates: {
          enabled: true,
          get_interval: 1000
        }
      });
      bot.api.getMe().then(resolve).catch(reject);
      bot.start_listening();
    });
  },
  start_listening: () => {
    bot.api.on('message', message => {
      const cmd = commands.parse(message.text);
      bot.sendMessage('PROCESSING 🤓');
      if (cmd) {
        cmd.action(message, bot);
      } else {
        bot.sendMessage(STR.UNKNOWN_CMD);
      }
    });
  }
};

module.exports = bot;