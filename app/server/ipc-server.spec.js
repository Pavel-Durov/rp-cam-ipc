
const server = require('./ipc-server');
const ipc = require('node-ipc');
const ipcConst = require('../core/ipc-const.json')
const ipcEvents = require('../core/events.json');

var expect = require('chai').expect;

describe(`ipc server, ${ipcConst.RPCAM_SERRVER_ID}, ${ipcConst.RP_CAM_CAPTURE_SOCKET}`, () => {

  var connected = false;

  before(() => {
    return new Promise((resolve) => {
      ipc.log = () => { };
      ipc.connectTo(ipcConst.RPCAM_SERRVER_ID, ipcConst.RP_CAM_CAPTURE_SOCKET, () => {
        ipc.of[ipcConst.RPCAM_SERRVER_ID].on(ipcEvents.CONNECT, () => {
          connected = true;
          resolve();
        });
      });
    });
  })

  after(() => {
    connected = false;
    return ipc.disconnect(ipcConst.RPCAM_SERRVER_ID);
  });

  it(`connect to ${ipcConst.RPCAM_SERRVER_ID}, ${ipcConst.RP_CAM_CAPTURE_SOCKET}`, () => {
    expect(connected).to.be.eq(true);
  });

  it(`RPCAM_CAPTURE emit & recive`, done => {
    const msg = 'capture-event-message';
    testIpcEvent(ipcEvents.RPCAM_CAPTURE, msg).then((msg) => {
      expect(msg).to.be.eq(msg);
      done();
    })
  });

  it(`RPCAM_CAPTURE_READY emit & recive`, done => {
    const msg = 'capture-ready-event-message'
    testIpcEvent(ipcEvents.RPCAM_CAPTURE_READY).then((msg) => {
      expect(msg).to.be.eq(msg);
      done();
    })
  });

  it(`RPCAM_VIDEO_RECORD emit & recive`, done => {
    const msg = 'vide-record-event-message'
    testIpcEvent(ipcEvents.RPCAM_VIDEO_RECORD).then((msg) => {
      expect(msg).to.be.eq(msg);
      done();
    })
  });

  it(`RPCAM_VIDEO_RECORD_READY emit & recive`, done => {
    const msg = 'video-record-ready-message'
    testIpcEvent(ipcEvents.RPCAM_VIDEO_RECORD_READY, msg).then((msg) => {
      expect(msg).to.be.eq(msg);
      done();
    })
  });

  it(`RPCAM_MOTION_DETECTED emit & recive`, done => {
    const msg = 'omg-motion-detected-messag';
    testIpcEvent(ipcEvents.RPCAM_MOTION_DETECTED).then((msg) => {
      expect(msg).to.be.eq(msg);
      done();
    })
  });
});

function testIpcEvent(eventName, msg) {
  return new Promise((resolve, reject) => {
    ipc.of[ipcConst.RPCAM_SERRVER_ID].on(eventName, resolve);
    ipc.of[ipcConst.RPCAM_SERRVER_ID].emit(eventName, msg);
  });
}

