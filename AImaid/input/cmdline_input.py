import json
import sqlite3
from ..core.model.input.model_normal_chat import NormalChatM
class CmdlineInput():
    def __init__(self):
        self.conn = sqlite3.connect('AImaid/core/model/maid.db')
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
