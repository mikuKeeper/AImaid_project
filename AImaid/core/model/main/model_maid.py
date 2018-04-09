import sqlite3
from .model_message_queue import MessageQueueM


class MaidM():
    def __init__(self, conn=None):
        if conn == None:
            self.conn = sqlite3.connect('AImaid/core/model/maid.db')
        else:
            self.conn = conn
        self.c = self.conn.cursor()
        self.normalmessagekey = 'chatmessage'
        self.cmdmessage_music = 'musiccmd'
        self.mqM = MessageQueueM(self.conn)

    def __del__(self):
        self.conn.close()

    
    def setBusy(self, isbusy):
        try:
            self.c.execute("UPDATE maid_status SET STATUS_VALUE=? WHERE STATUS_NAME='isbusy'",(str(isbusy),))
            self.conn.commit()
        except Exception as e:
            print('set busy failed : ',e)
            return False
        else:
            return True

    def getBusy(self):
        try:
            cursor = self.c.execute("SELECT STATUS_VALUE from maid_status WHERE STATUS_NAME='isbusy'")
        except Exception as e:
            print('get busy failed :', e)
            return True
        else:
            result = cursor.fetchall()[0][0]
            if result == "False":
                return False
            else:
                return True
            
    def pushNormalChat(self, message):
        print('maid push nolmalchat: ',message)
        return self.mqM.push(self.normalmessagekey, message)

    def popNormalChat(self):
        result = self.mqM.popFIFO(self.normalmessagekey)
        if result != None:
            return result[0]
        else:
            return None

    def pushMusicCMD(self, message):
        return self.mqM.push(self.cmdmessage_music, message)

    def popMusicCMD(self):
        result = self.mqM.popFIFO(self.cmdmessage_music)
        if result != None:
            return result[0]
        else:
            return None


            
        
