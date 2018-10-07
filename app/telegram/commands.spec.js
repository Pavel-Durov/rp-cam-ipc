const expect = require('chai').expect;
const commands = require('./commands');

describe('telegram bot commands', () => {
  it('/h command parse', () => {
    const cmd = commands.parse('/h');
    expect(cmd.cmd).to.be.eq('/h');
    expect(cmd.action).to.be.not.eq(undefined);
  });

  it('/img command parse', () => {
    const cmd = commands.parse('/img');
    expect(cmd.cmd).to.be.eq('/img');
    expect(cmd.action).to.be.not.eq(undefined);
  });

  it('/vid command parse', () => {
    const cmd = commands.parse('/vid');
    expect(cmd.cmd).to.be.eq('/vid');
    expect(cmd.action).to.be.not.eq(undefined);
  });

  it('/sub command parse', () => {
    const cmd = commands.parse('/sub');
    expect(cmd.cmd).to.be.eq('/sub');
    expect(cmd.action).to.be.not.eq(undefined);
  });

  it('/unsub command parse', () => {
    const cmd = commands.parse('/unsub');
    expect(cmd.cmd).to.be.eq('/unsub');
    expect(cmd.action).to.be.not.eq(undefined);
  });

  it('/i command parse', () => {
    const cmd = commands.parse('/i');
    expect(cmd.cmd).to.be.eq('/i');
    expect(cmd.action).to.be.not.eq(undefined);
  });

  it('undefined command parse', () => {
    const cmd = commands.parse('/somethig-else');
    expect(cmd).to.be.eq(undefined);
  });
});