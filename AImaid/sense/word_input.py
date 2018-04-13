import json
import sqlite3
import os
from ..core.model.sense.model_normal_chat import NormalChatM
class CmdlineInput():
    def __init__(self):
        workpath = os.path.dirname(os.path.abspath(__file__))
        dbpath = os.path.join(workpath,'..','core','model','maid.db')
        self.conn = sqlite3.connect(dbpath)
        self.messagesrckey = 'originalmessage' 
        self.M = NormalChatM(self.conn)
    def cmdInput(self):
        text = input('Master:')
        try:
            data = json.dumps({'type':'0','text':text,'commentuser':'Master'})
            self.M.pushChat(data)
    
        except Exception as e:
            print(e)
        else:
            pass
        
            
if __name__ == "__main__":
    ci = CmdlineInput()
    while True:
        ci.cmdInput()
