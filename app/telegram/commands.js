const R = require('ramda');
const logger = require("../core/logger.js");
const LOG_TAG = 'CMD';

function generateCmdList() {
  return cmdModule.list.map(c => `${c.cmd}:    ${c.description}`).join('\n')
}

const HELP_CMD = {
  cmd: '/h',
  description: 'command list',
  action: (_, bot) => {
    logger.info(generateCmdList());
    bot.sendMessage(generateCmdList())
    logger.log(LOG_TAG, 'HELP_CMD')
  }
}

const IMG_CMD = {
  cmd: '/img',
  description: 'take a snapshot',
  action: (_, bot) => {
    bot.takeImage(1);
    logger.log(LOG_TAG, 'IMG_CMD');
  }
}

const VID_CMD = {
  cmd: '/vid',
  description: 'record video',
  action: (_, bot) => {
    bot.recordVideo(5);
    logger.log(LOG_TAG, 'VID_CMD')
  }
}

const SUB_CMD = {
  cmd: '/sub',
  description: 'subscribe to notifications',
  action: (message, bot) => {
    bot.subscribe(message.chat.id);
    logger.log(LOG_TAG, 'SUB_CMD')
  }
}

const UNSUB_CMD = {
  cmd: '/unsub',
  description: 'unsubscribe to notifications',
  action: (message, bot) => {
    bot.unsubscribe(message.chat.id);
    logger.log(LOG_TAG, 'UNSUB_CMD')
  }
}

const INFO_CMD = {
  cmd: '/i',
  description: 'general info',
  action: (_, bot) => {
    bot.sendMessage(JSON.stringify(bot.SUBSCRIBERS))
    logger.log(LOG_TAG, 'INFO_CMD')
  }
}

const filterCmd = str => R.filter(R.propEq('cmd', str), cmdModule.list);
const locateCmd = R.compose(R.head, filterCmd);

var cmdModule = {
  list: [HELP_CMD, IMG_CMD, VID_CMD, SUB_CMD, UNSUB_CMD, INFO_CMD],
  parse: str => locateCmd(str)
}
module.exports = cmdModule;