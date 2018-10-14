const telegram = require('telegram-bot-api');
const commands = require('./commands');
const log = require('debug')('bot');

const STR = {
  SUB_SUCCESS: 'Thanks for subscribing👍',
  UNSUB_ERROR: '',
  UNSUB_SUCCESS: 'Sad to see you leaving...',
  SUB_FAIL_EXIST: 'Ooops, already subscribed 😞',
  UNKNOWN_CMD: 'UNKNOWN COMMAND 😠'
};

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
    (imgPaths || []).forEach(path => {
      bot.notify(id => bot.api.sendPhoto({
        chat_id: id,
        caption: 'This is a test caption', photo: path
      }));
    });
  },
  sendVideo: (path, caption) => {
    bot.notify(id => bot.api.sendVideo({ chat_id: id, caption: caption, video: path }));
  },
  onMotionDetected: (path) => {
    bot.sendVideo(path, '🕵️ Motion Detected');
  },
  notify: func => {
    log('notify,', bot.SUBSCRIBERS);
    (bot.SUBSCRIBERS || []).forEach(async (id) => {
      try {
        const data = await func(id);
        log(data);
      } catch (e) {
        log(e);
      }
    });
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