'use strict';

const {
  filter,
  propEq,
  compose,
  head
} = require('ramda');

const {
  RPCAM_SNAPSHOTS_PER_IMG_CMD,
  RPCAM_VIDEO_CMD_DURATION
} = require('../core/ipc-const');

const log = require('debug')('bot:commands');

function generateCmdList() {
  return CMD_LIST.map(({ cmd, description }) => `${cmd}:    ${description}`).join('\n');
}

const HELP_CMD = {
  cmd: '/h',
  description: 'command list',
  action: (chatId, bot) => {
    bot.sendMessage(generateCmdList());
    log('HELP_CMD:action');
  }
};

const IMG_CMD = {
  cmd: '/img',
  description: 'take a snapshot',
  action: (chatId, bot) => {
    bot.takeImage(RPCAM_SNAPSHOTS_PER_IMG_CMD);
    log('IMG_CMD:action');
  }
};

const VID_CMD = {
  cmd: '/vid',
  description: 'record video',
  action: (chatId, bot) => {
    bot.recordVideo(RPCAM_VIDEO_CMD_DURATION);
    log('VID_CMD:action');
  }
};

const SUB_CMD = {
  cmd: '/sub',
  description: 'subscribe to notifications',
  action: (chatId, bot) => {
    bot.subscribe(chatId);
    log('SUB_CMD:action');
  }
};

const UNSUB_CMD = {
  cmd: '/unsub',
  description: 'unsubscribe to notifications',
  action: (chatId, bot) => {
    bot.unsubscribe(chatId);
    log('UNSUB_CMD:action');
  }
};

const INFO_CMD = {
  cmd: '/i',
  description: 'general info',
  action: (chatId, bot) => {
    bot.sendMessage(JSON.stringify(bot.SUBSCRIBERS));
    log('INFO_CMD:action');
  }
};

const CMD_LIST = [HELP_CMD, IMG_CMD, VID_CMD, SUB_CMD, UNSUB_CMD, INFO_CMD];
const filterCmd = str => filter(propEq('cmd', str), CMD_LIST);
const locateCmd = compose(head, filterCmd);

module.exports = {
  parse: str => locateCmd(str),
  test: {
    filterCmd
  }
};
