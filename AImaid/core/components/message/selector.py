from ...model.main.model_message_queue import MessageQueueM
import re
import json
import time

class MessageSelector():
    def __init__(self):
        self.messagesrckey = 'originalmessage'
        self.normalmessagekey = 'chatmessage'
        self.cmdmessage_music = 'musiccmd'
        self.mqM = MessageQueueM()

    def messageHub(self):
        while True:
            data = self.mqM.popFIFO(self.messagesrckey)
            if data != None:
                try:
                    data = json.loads(data[0])
                except Exception as e:
                    print(e)
                    continue
            else:
                time.sleep(0.5)
                continue
            print(data)
            type = data['type']
            if type == '0':
                msg = data['text']
                if self.musicSelector(msg,data):
                    continue
                else:
                    j = json.dumps(data)
                    self.mqM.push(self.normalmessagekey, j)
            else:
                j = json.dumps(data)
                self.mqM.push(self.normalmessagekey, j)


    def musicSelector(self, msg, data):
        cmd = {}
        if msg != '' and msg[0] == '#':
            m = re.match('^#点歌 (.*)', msg)
            if m != None:
                cmd['songname'] = m.group(1)
                cmd['step'] = '1'
                cmd['cmd'] = 'search'
                cmd['text'] = msg
                cmd['user'] = data['commentuser']
                cmd = json.dumps(cmd)
                self.mqM.push(self.cmdmessage_music, cmd)
                return True
            m = re.match('^#(\d)',msg)
            if m != None:
                cmd['step'] = '2'
                cmd['user'] = data['commentuser']
                cmd['cmd'] = 'select'
                cmd['text'] = msg
                cmd['selectnum'] = m.group(1)
                cmd = json.dumps(cmd)
                self.mqM.push(self.cmdmessage_music, cmd)
                return True
            m = re.match('^#切歌', msg)
            if m != None:
                cmd['cmd'] = 'switch'
                cmd['user'] = data['commentuser']
                cmd['text'] = msg
                cmd = json.dumps(cmd)
                self.mqM.push(self.cmdmessage_music, cmd)

                return True
        else:
            return False

if __name__ == "__main__":
    messelector = MessageSelector()
    messelector.messageHub()

        
        

        
        
