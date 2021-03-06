
const { stop } = require('../server/ipc-server');
const ipc = require('node-ipc');

const {
  RPCAM_SERRVER_ID,
  RPCAM_CAPTURE_SOCKET
} = require('../core/ipc-const.json');

const {
  CONNECT,
  RPCAM_CAPTURE_READY,
  RPCAM_CAPTURE,
  RPCAM_VIDEO_RECORD,
  RPCAM_VIDEO_RECORD_READY,
  RPCAM_MOTION_DETECTED
} = require('../core/events.json');

var expect = require('chai').expect;

describe(`ipc server, ${RPCAM_SERRVER_ID}, ${RPCAM_CAPTURE_SOCKET}`, () => {
  let server;
  after((done) => {
    server.on('disconnect', () => {
      done();
    });
    ipc.disconnect(RPCAM_SERRVER_ID);
    stop();
  });

  before(`connect to ${RPCAM_SERRVER_ID}, ${RPCAM_CAPTURE_SOCKET}`, (done) => {
    ipc.connectTo(RPCAM_SERRVER_ID, RPCAM_CAPTURE_SOCKET, () => {
      server = ipc.of[RPCAM_SERRVER_ID];
      server.on(CONNECT, () => done());
    });
  });

  it('events should be strings', () => {
    const nonStrings = [
      RPCAM_CAPTURE_READY,
      RPCAM_CAPTURE,
      RPCAM_CAPTURE_READY,
      RPCAM_VIDEO_RECORD,
      RPCAM_VIDEO_RECORD_READY
    ].filter(s => typeof s !== 'string');
    expect(nonStrings).to.be.empty;
  });

  it('RPCAM_CAPTURE_READ event test', async () => {
    const response = await testIpcEvent(RPCAM_CAPTURE_READY, 1);
    expect(1).to.be.eql(response);
  });

  it('RPCAM_CAPTURE event test', async () => {
    const response = await testIpcEvent(RPCAM_CAPTURE, 2);
    expect(2).to.be.eql(response);
  });

  it('RPCAM_CAPTURE_READY event test', async () => {
    const response = await testIpcEvent(RPCAM_CAPTURE_READY, 3);
    expect(3).to.be.eql(response);
  });

  it('RPCAM_VIDEO_RECORD event test', async () => {
    const response = await testIpcEvent(RPCAM_VIDEO_RECORD, 4);
    expect(4).to.be.eql(response);
  });

  it('RPCAM_VIDEO_RECORD_READY event test', async () => {
    const response = await testIpcEvent(RPCAM_VIDEO_RECORD_READY, 5);
    expect(5).to.be.eql(response);
  });

  it('RPCAM_MOTION_DETECTED event test', async () => {
    const response = await testIpcEvent(RPCAM_MOTION_DETECTED, 5);
    expect(5).to.be.eql(response);
  });
});

async function testIpcEvent(eventName, dispatchMsg) {
  return new Promise((resolve) => {
    ipc.of[RPCAM_SERRVER_ID].on(eventName, function (msg) {
      resolve(msg);
    });
    ipc.of[RPCAM_SERRVER_ID].emit(eventName, dispatchMsg);
  });
}

