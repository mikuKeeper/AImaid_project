import random, json

class IdleEmotion():
    def __init__(self):
        self.emotion_score = 0
        self.emotion_threshold = 1000
        self.idle_things = ['讲笑话','讲故事','歇后语','脑筋急转弯','绕口令','顺口溜','喵喵喵','谁是你主人', '你是谁']
        self.inc_ranges = [(0,10)]
        self.dec_ranges = [(0,500),(300,700),(200,600)] 

    def increase(self, type=0):
        range = self.inc_ranges[type]
        self.emotion_score = self.emotion_score + random.randint(range[0], range[1])

    def decrease(self, type=0):
        range = self.dec_ranges[type]
        self.emotion_score = self.emotion_score - random.randint(range[0], range[1])

    def isIdle(self):
        if self.emotion_score > self.emotion_threshold:
            return True
        else:
            return False

    def popIdea(self):
        if self.isIdle():
            data = json.dumps({'type':'0','text':self.idle_things[random.randint(0,self.idle_things.__len__()-1)],'commentuser':'system'})
            return data
        else:
            return None








