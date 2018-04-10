import sqlite3, os
from ..main.model_message_queue import MessageQueueM

class NormalChatM():
    def __init__(self,conn=None):
        workpath = os.path.dirname(os.path.abspath(__file__))
        dbpath = os.path.join(workpath,'../maid.db')
        if conn == None:
            self.conn = sqlite3.connect(dbpath)
        else:
            self.conn = conn
        self.c = self.conn.cursor()
        self.mqM = MessageQueueM()
        self.messagesrckey = 'originalmessage'

    def __del__(self):
        self.conn.close()

    def pushChat(self, message):
        result = self.mqM.push(self.messagesrckey, message)
        return result
    
    def popChat(self):
        result = self.mqM.popFIFO(self.messagesrckey)
        if result != None:
            return result[0]
        else:
            return None

    def lenChat(self):
        result = self.mqM.lenQueue(self.messagesrckey)
        return result


