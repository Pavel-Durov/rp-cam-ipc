const { expect } = require('chai');
const {
  parse
} = require('./commands');

const {
  RPCAM_SNAPSHOTS_PER_IMG_CMD,
  RPCAM_VIDEO_CMD_DURATION
} = require('../core/ipc-const');

describe('telegram bot commands', () => {
  function extractCmdAction(strCmd) {
    const { cmd, action } = parse(strCmd);
    expect(cmd).to.be.eq(strCmd);
    expect(action).to.be.a('function');
    return action;
  }

  describe('parse', () => {
    it('/h command', () => {
      const action = extractCmdAction('/h');
      action(undefined, {
        sendMessage: (cmdList) => {
          expect(cmdList).to.be.a('string');
          expect(cmdList).to.not.be.empty;
        }
      });
    });
    it('/img command', () => {
      const action = extractCmdAction('/img');
      action(undefined, {
        takeImage: (count) => {
          expect(count).to.be.equal(RPCAM_SNAPSHOTS_PER_IMG_CMD);
        }
      });
    });
    it('/vid command', () => {
      const action = extractCmdAction('/vid');
      action(undefined, {
        recordVideo: (duration) => {
          expect(duration).to.be.equal(RPCAM_VIDEO_CMD_DURATION);
        }
      });
    });

    it('/sub command', () => {
      const chatId = 1234;
      const action = extractCmdAction('/sub');
      action(chatId, {
        subscribe: (id) => {
          expect(id).to.be.a('number');
          expect(id).to.be.equal(chatId);
        }
      });
    });
    it('/unsub command', () => {
      const chatId = 4321;
      const action = extractCmdAction('/unsub');
      action(chatId, {
        unsubscribe: (id) => {
          expect(id).to.be.a('number');
          expect(id).to.be.equal(chatId);
        }
      });
    });
    it('/i command', () => {
      const action = extractCmdAction('/i');
      action(undefined, {
        SUBSCRIBERS: [12345],
        sendMessage: (msg) => {
          expect(msg).to.be.a('string');
          expect(msg).to.be.eq(JSON.stringify([12345]));
        }
      });
    });
    it('undefined command', () => {
      const cmd = parse('/somethig-else');
      expect(cmd).to.be.eq(undefined);
    });
  });
});