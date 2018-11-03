const expect = require('chai').expect;
const bot = require('../telegram/bot');
const {
  mkdir,
  rmdir,
  writeFile,
  exists
} = require('fs');
const { promisify } = require('util');
const path = require('path');

const writeFileAsync = promisify(writeFile);
const fileExistAsync = promisify(exists);

describe('telegram bot', () => {
  const FS_TEST_DIR = path.join(__dirname, 'fs-test');
  before('creating fs-test directory', async () => {
    await promisify(mkdir)(FS_TEST_DIR);
  });
  after('deleting fs-test directory', async () => {
    await promisify(rmdir)(FS_TEST_DIR);
  });

  it('env TELEGRAM_BOT_TOKEN variable set', () => {
    expect(process.env.TELEGRAM_BOT_TOKEN).to.match(/\d*:\w*/);
  });
  describe('actions', () => {
    it('sub/unsub same id', () => {
      const chatId = 2;
      bot.setApi({
        sendMessage: () => Promise.resolve()
      });
      bot.ipc = {
        stopMotionDetection: () => { },
        startMotionDetection: () => { }
      };
      bot.subscribe(chatId);
      bot.unsubscribe(chatId);
      expect(bot.SUBSCRIBERS).to.be.empty;
    });
    it('sub/unsub different id', () => {
      bot.setApi({
        sendMessage: () => Promise.resolve(),
      });
      bot.ipc = {
        stopMotionDetection: () => { },
        startMotionDetection: () => { }
      };
      bot.subscribe(1);
      bot.unsubscribe(2);

      expect(bot.SUBSCRIBERS).to.eql([1]);
    });
    it('sub', () => {
      bot.setApi({
        sendMessage: () => Promise.resolve()
      });
      const chatId = 1;
      bot.subscribe(chatId);
      expect(bot.SUBSCRIBERS).to.include(chatId);
      bot.unsubscribe(chatId);
    });
    it('sendMessage', done => {
      const chatId = 1223;
      bot.setApi({
        sendMessage: ({ chat_id, text }) => {
          expect(chat_id).to.be.eq(chatId);
          expect(text).to.be.eq('hi');
          done();
        }
      });
      bot.subscribe(chatId);
      bot.sendMessage('hi');
      bot.unsubscribe(chatId);
    });
    it('multiple sub', () => {
      const chatId = 1;
      bot.setApi({
        sendMessage: () => Promise.resolve()
      });
      bot.subscribe(chatId);
      bot.subscribe(chatId);
      bot.subscribe(chatId);
      expect(bot.SUBSCRIBERS).to.eql([chatId]);
      bot.unsubscribe(chatId);
    });
    it('sendVideo should delete video after send', async () => {
      const testFilePath = path.join(FS_TEST_DIR, 'test-0.mp4');
      await writeFileAsync(testFilePath, '0x00');
      await bot.sendVideo(testFilePath);
      expect(await fileExistAsync(testFilePath)).to.be.eq(false);
    });
    it('sendImage should delete image files after send', async () => {
      const testFilePath = path.join(FS_TEST_DIR, 'test-0.jpg');
      await writeFileAsync(testFilePath, '0x00');
      await bot.sendImage([testFilePath]);
      expect(await fileExistAsync(testFilePath)).to.be.eq(false);
    });
    it('sendImage should delete multiple files after send', async () => {
      const testFilePaths = [
        path.join(FS_TEST_DIR, 'test-0.jpg'),
        path.join(FS_TEST_DIR, 'test-1.jpg'),
        path.join(FS_TEST_DIR, 'test-2.jpg')
      ];

      const fileCreation = testFilePaths.map((path) => {
        return writeFileAsync(path, '0x00');
      });
      await Promise.all(fileCreation);
      await bot.sendImage(testFilePaths);

      const fileExistence = testFilePaths.map((path) => {
        return fileExistAsync(path);
      });
      const existing = await Promise.all(fileExistence);
      expect(existing).to.be.eql([false, false, false]);
    });
  });
});