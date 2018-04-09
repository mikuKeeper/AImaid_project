import sqlite3
from ..main.model_message_queue import MessageQueueM

class NormalChatM():
    def __init__(self,conn=None):
        if conn == None:
            self.conn = sqlite3.connect('AImaid/core/model/maid.db')
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


