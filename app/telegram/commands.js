const R = require('ramda');
const log = require('debug')('bot:commands');
const LOG_TAG = 'CMD';

function generateCmdList() {
  return cmdModule.list.map(c => `${c.cmd}:    ${c.description}`).join('\n');
}

const HELP_CMD = {
  cmd: '/h',
  description: 'command list',
  action: (_, bot) => {
    log(generateCmdList());
    bot.sendMessage(generateCmdList());
    log(LOG_TAG, 'HELP_CMD');
  }
};

const IMG_CMD = {
  cmd: '/img',
  description: 'take a snapshot',
  action: (_, bot) => {
    bot.takeImage(1);
    log(LOG_TAG, 'IMG_CMD');
  }
};

const VID_CMD = {
  cmd: '/vid',
  description: 'record video',
  action: (_, bot) => {
    bot.recordVideo(5);
    log('VID_CMD:action');
  }
};

const SUB_CMD = {
  cmd: '/sub',
  description: 'subscribe to notifications',
  action: (message, bot) => {
    bot.subscribe(message.chat.id);
    log('SUB_CMD:action');
  }
};

const UNSUB_CMD = {
  cmd: '/unsub',
  description: 'unsubscribe to notifications',
  action: (message, bot) => {
    bot.unsubscribe(message.chat.id);
    log('UNSUB_CMD:action');
  }
};

const INFO_CMD = {
  cmd: '/i',
  description: 'general info',
  action: (_, bot) => {
    bot.sendMessage(JSON.stringify(bot.SUBSCRIBERS));
    log('INFO_CMD:action');
  }
};

const filterCmd = str => R.filter(R.propEq('cmd', str), cmdModule.list);
const locateCmd = R.compose(R.head, filterCmd);

const cmdModule = {
  list: [HELP_CMD, IMG_CMD, VID_CMD, SUB_CMD, UNSUB_CMD, INFO_CMD],
  parse: str => locateCmd(str)
};

module.exports = cmdModule;
