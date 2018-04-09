from AImaid.present.yuyin import *
import random
from AImaid.present.display import *
from AImaid.chatbot.xiaobingchat import *
from AImaid.chatbot.tulingbot import *
from AImaid.action.mp3play.mp3controller import *
from AImaid.core.model.main.model_maid import MaidM

class Maid():
    def __init__(self):
        self.M = MaidM()
        self.songlist = []
        self.mp3ctl = MP3Controller()
        self.yuyin = BaiduYuyin()
        self.dsp = Display(position='right_bottom')
        self.dsp.runPlay()
        #self.chatbot = XiaoBing()
        self.chatbot = Tuling()
        #idel things
        self.idle_emotion = 0
        self.idle_things = ['讲笑话','讲故事','歇后语','脑筋急转弯','绕口令','顺口溜','喵喵喵','谁是你主人', '你是谁']
        #filter message
        self.help_msg = ['这是什么','你是谁', '这是什么玩意', '你叫什么','什么鬼','这是在干嘛?','?','???']
        self.info_msg = "我叫娜娜眯(NANAMI)，是主人开发的全自动智能机器女仆，你可以通过弹幕和我交流，我特别擅长讲冷笑话^_^" 
    def fetchMessage(self):
        #0=chat, 1=music
        while True:
            data = self.chatModel()
            if data != None:
                return 0,data
            data = self.musicModel()
            if data != None:
                return 1,data

    def chatModel(self):
        data = self.M.popNormalChat()
        if self.idle_emotion > 1000:
            data = json.dumps({'type':'0','text':self.idle_things[random.randint(0,self.idle_things.__len__()-1)],'commentuser':'system'})
            self.idle_emotion = self.idle_emotion - random.randint(0,500)
        if data == None:
            time.sleep(0.3)
            self.idle_emotion = self.idle_emotion + random.randint(0,10)
            return None
        else:
            self.idle_emotion = self.idle_emotion - random.randint(300,700)
            try:
                data = json.loads(data)
            except Exception as e:
                return None
            else:
                return data

    def musicModel(self):
        data = self.M.popMusicCMD()
        if data == None:
            return None
        else:
            self.idle_emotion = self.idle_emotion - random.randint(200,600)
            try:
                data = json.loads(data)
            except Exception as e:
                return None
            else:
                return data 

    def messageFilter(self, msg):
        if msg in self.help_msg:
            return True,self.info_msg
        elif 'http://' in msg:
            return False, "禁止事项,喵喵"
        else:
            return False,msg

    def responseFilter(self, msg):
        if 'http://' in msg or 'https://' in msg:
            return '禁止事项,喵喵'
        elif '小冰' in msg:
            msg = msg.replace('小冰', '娜娜咪')
            return msg
        else:
            return msg

    def talk(self, msg):
        print('女仆NANAMI: '+msg)
        try:
            self.yuyin.postText(msg)
            self.dsp.nextAction('talk')
            self.yuyin.playMp3()
        except Exception as e:
            print(e)
        self.dsp.nextAction('normal')
 
    def response(self, data):
        if data['type'] == '0':
            print(data['commentuser']+': '+data['text'])
            flag, msg = self.messageFilter(data['text']) 
            if flag == False:
                retmsg = self.chatbot.chat(msg)
                retmsg = self.responseFilter(retmsg)
            else:
                retmsg = msg
            if data['commentuser'] != 'system':
                self.talk(retmsg)
            else:
                self.talk(retmsg)

        elif data['type'] == '1':
            print(data['giftuser']+'送了'+data['giftname']+'给你')
            msg = '我送了'+data['giftname']+'给你'
            retmsg = self.chatbot.chat(msg)
            self.talk(data['giftuser']+','+retmsg)
        elif data['type'] == '2':
            print('欢迎'+data['commentuser']+','+'我是弹幕女仆^_^')
            self.talk('欢迎'+data['commentuser']+','+'我是弹幕女仆^_^')


    def musicAction(self, data):
        print(data['user']+': '+data['text'])
        cmd = data['cmd']
        if cmd == 'switch':
            self.mp3ctl.switch()
        elif cmd == 'search':
            self.songlist = self.mp3ctl.search(data['songname'])
            if self.songlist == None:
                retmsg = '抱歉喵，未找到你点播的歌曲'
                self.talk(retmsg)
            else:
                retmsg = '已完成搜索，请从列表中选择: '
                strlist = ''
                for i, song in enumerate(self.songlist):
                    strlist = strlist + str(i) + '.' + song['singer'] + '_' + song['name'][0:10] + ';'
                retmsg = retmsg + strlist
                self.talk(retmsg)
        elif cmd == 'select' and self.songlist != [] and self.songlist != None:
            selectnum = int(data['selectnum'])
            if selectnum < 0 or selectnum >= self.songlist.__len__():
                selectnum = 0
            song = self.songlist[selectnum]
            flag = self.mp3ctl.dianboPlay(song)
            if flag == True:
                retmsg = data['user'] + ',' + '点播' + song['singer'] + '的' + song['name'][0:10] + ' 成功'
                self.talk(retmsg)
            else:
                retmsg = '对不起，' + data['user'] + ',' + '点播' + song['singer'] + '的' + song['name'][0:10] + ' 失败'
                self.talk(retmsg)
        

    def work(self):
        while True:
            model, data = self.fetchMessage()
            if model == 0:
                self.response(data)
            elif model == 1:
                self.musicAction(data)

if __name__ == "__main__":
    #xb = XiaoBing()
    #retmsg = xb.chat('做我女朋友好不好')
    maid = Maid()
    maid.work()


        
        
 
