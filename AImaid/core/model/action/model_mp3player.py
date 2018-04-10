import sqlite3, os
from ..main.model_message_queue import MessageQueueM


class Mp3PlayerM():
    def __init__(self,conn=None):
        workpath = os.path.dirname(os.path.abspath(__file__))
        dbpath = os.path.join(workpath,'../maid.db')
        if conn == None:
            self.conn = sqlite3.connect(dbpath)
        else:
            self.conn = conn
        self.c = self.conn.cursor()
        self.mqM = MessageQueueM(self.conn)

        self.dianboqueue = 'dianbo'

    def __del__(self):
        self.conn.close()

#dianbo control    
    def setDianboBusy(self, isbusy):
        try:
            self.c.execute("UPDATE action_status SET STATUS_VALUE=? where STATUS_NAME='mp3player_dianbo_isbusy'",(str(isbusy),))
            self.conn.commit()
        except Exception as e:
            print('set mp3dianbobusy failed : ',e)
            return False
        else:
            return True

    def getDianboBusy(self):
        try:
            cursor = self.c.execute("SELECT STATUS_VALUE from action_status WHERE STATUS_NAME='mp3player_dianbo_isbusy'")
        except Exception as e:
            print('get mp3dianbobusy failed :', e)
            return True
        else:
            result = cursor.fetchall()[0][0]
            if result == "False":
                return False
            else:
                return True

    def pushDianbo(self, message):
        if self.mqM.push(self.dianboqueue, message):
            return True
        else:
            print('dianbo failed')
            return False

    def popDianbo(self):
        result = self.mqM.popFIFO(self.dianboqueue)
        if result != None:
            return result[0]
        else:
            return None

    def lenDianbo(self):
        result = self.mqM.lenQueue(self.dianboqueue)
        return result
    
    def clearDianbo(self):
        return self.mqM.clearQueue(self.dianboqueue)




#default BGM control
    def setDefaultBGMSwitchFlag(self, flag):
        try:
            self.c.execute("UPDATE action_status SET STATUS_VALUE=? where STATUS_NAME='mp3player_defaultBGM_switch'",(str(flag),))
            self.conn.commit()
        except Exception as e:
            print('set switch flag failed : ',e)
            return False
        else:
            return True

    def getDefaultBGMSwitchFlag(self):
        try:
            cursor = self.c.execute("SELECT STATUS_VALUE from action_status WHERE STATUS_NAME='mp3player_defaultBGM_switch'")
        except Exception as e:
            print('get switch BGM flag failed : ', e)
            return False
        else:
            result = cursor.fetchall()[0][0]
            if result == 'True':
                return True
            else:
                return False


