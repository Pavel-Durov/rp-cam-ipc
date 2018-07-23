const expect = require('chai').expect;
const bot = require('./bot');

describe('telegram bot', () =>{
     const botIpcMock = {
         emit: (cmd, payload) => {
             
         },
         capture: num => {
             
         },
         recordVideo: sec => {
             
         }
     };

    it('enviroment TELEGRAM_BOT_TOKEN variable set', () => {
        expect(process.env.TELEGRAM_BOT_TOKEN).to.match(/\d*:\w*/)
    })

    it('sendMessage', done =>{
        bot.SUBSCRIBERS = ['test'];
        bot.api = { 
            sendMessage: (msg) => {
                expect(msg.chat_id).to.be.eq('test');
                expect(msg.text).to.be.eq('hi');
                done()
            }
        };
        bot.sendMessage('hi');
    })

    it('suscribtion',() =>{
        bot.SUBSCRIBERS = [];
         bot.api = { 
            sendMessage: (msg) => Promise.resolve()
        };
        bot.subscribe(1);
        expect(bot.SUBSCRIBERS).to.include.members([1])
    })

    it('double suscribtion',() =>{
        bot.SUBSCRIBERS = [];
        bot.api = { 
            sendMessage: (msg) => Promise.resolve()
        };
        
        bot.subscribe(1);
        bot.subscribe(1);
        
        expect(bot.SUBSCRIBERS).to.eql([1])
    })

    it('suscribtion/unsuscribtion correct id',() =>{
        bot.SUBSCRIBERS = [];
        bot.api = { 
            sendMessage: (msg) => Promise.resolve()
        };
        
        bot.subscribe(1);
        bot.unsubscribe(1);
        
        expect(bot.SUBSCRIBERS).to.eql([])
    })

    it('suscribtion/unsuscribtion wrong id',() =>{
        bot.SUBSCRIBERS = [];
        bot.api = { 
            sendMessage: (msg) => Promise.resolve()
        };
        bot.subscribe(1);
        bot.unsubscribe(2);
        
        expect(bot.SUBSCRIBERS).to.eql([1])
    })

    it('sendImage', done =>{
        bot.SUBSCRIBERS = [];
        bot.api = { 
            sendPhoto: (msg) => {
                expect(msg.photo).to.be.eq('test/test.jpg');
                done()
            },
            sendMessage: (msg) => Promise.resolve()
        };
        bot.subscribe(1);
        bot.sendImage(['test/test.jpg'])
    })

    it('sendVideo', done =>{
        bot.SUBSCRIBERS = [];
        bot.api = { 
            sendPhoto: (msg) => {
                expect(msg.photo).to.be.eq('test/test.mp4');
                expect(msg.chat_id).to.be.eq(1);
                done()
            },
            sendMessage: (msg) => Promise.resolve()
        };
        bot.subscribe(1);
        bot.sendImage(['test/test.mp4'])
    })
    
})