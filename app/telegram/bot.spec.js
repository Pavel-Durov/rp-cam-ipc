const expect = require('chai').expect;
const bot = require('./bot');

describe('telegram bot', () =>{
    it('enviroment TELEGRAM_BOT_TOKEN variable set', () => {
        expect(process.env.TELEGRAM_BOT_TOKEN).to.match(/\d*:\w*/)
    })
})