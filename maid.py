import random, json, time
from operator import methodcaller

from AImaid import expression
from AImaid import strategy
from AImaid.ability.skill import *
from AImaid.core.model.main.model_maid import MaidM

class Maid():
    def __init__(self):
        #model
        self.M = MaidM()
        
        #strategy
        self.logic = strategy.logic
        self.idle_emotion = strategy.emotion.idle.IdleEmotion()

        #base expression
        self.talk = expression.actions.talk

        #ability skill
        self.mp3skill = mp3play.mp3controller.MP3Controller()

    def fetchMessage(self):
        #0=chat, 1=music
        while True:
            data = self.chatModule()
            if data != None:
                return 0,data
            data = self.musicModule()
            if data != None:
                return 1,data

    def chatModule(self):
        data = self.M.popNormalChat()
        idea = self.idle_emotion.popIdea()
        if idea != None:
            data = idea
            self.idle_emotion.decrease(0)
        if data == None:
            time.sleep(0.3)
            self.idle_emotion.increase(0)
            return None
        else:
            self.idle_emotion.decrease(1)
            try:
                data = json.loads(data)
            except Exception as e:
                return None
            else:
                return data

    def musicModule(self):
        data = self.M.popMusicCMD()
        if data == None:
            return None
        else:
            self.idle_emotion.decrease(2)
            try:
                data = json.loads(data)
            except Exception as e:
                return None
            else:
                return data 


       
    def abilityAction(self, skill, data):
        opt, retmsg = skill.action(data)
        if opt != None:
            methodcaller(opt, retmsg)(self)
        else:
            pass

    def work(self):
        while True:
            module, data = self.fetchMessage()
            if module == 0:
                #chat
                retmsg = self.logic.chatReact(data)
                self.talk(retmsg)
            elif module == 1:
                #musicAction
                self.abilityAction(self.mp3skill, data)


if __name__ == "__main__":
    maid = Maid()
    maid.work()


        
        
 
