
class MessageFilter():
    def __init__(self):
        self.help_msg = ['这是什么','你是谁', '这是什么玩意', '你叫什么','什么鬼','这是在干嘛?','?','???']
        self.info_msg = "我叫娜娜眯(NANAMI)，是主人开发的全自动智能机器女仆，你可以通过弹幕和我交流，我特别擅长讲冷笑话^_^" 

    def inputFilter(self, msg):
        if msg in self.help_msg:
            return True,self.info_msg
        elif 'http://' in msg:
            return False, "禁止事项,喵喵"
        else:
            return False,msg

    def outputFilter(self, msg):
        if 'http://' in msg or 'https://' in msg:
            return '禁止事项,喵喵'
        elif '小冰' in msg:
            msg = msg.replace('小冰', '娜娜咪')
            return msg
        else:
            return msg


