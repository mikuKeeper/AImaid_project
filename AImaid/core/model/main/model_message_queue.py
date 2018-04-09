import sqlite3

class MessageQueueM():
    def __init__(self,conn=None):
        if conn is None:
            self.conn = sqlite3.connect('AImaid/core/model/maid.db')
        else:
            self.conn = conn
        self.c = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def createNewQueue(self, name):
        queue_name = 'queue_' + name
        try:
            self.c.execute('''CREATE TABLE %s
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    MESSAGE TEXT NOT NULL
                    );'''%(queue_name,))
            self.conn.commit()
        except Exception as e:
            print('create new queue failed :', e)
            self.conn.rollback()
        else:
            print('create new queue %s successfully'%(queue_name,))

    def push(self, name, message):
        queue_name = 'queue_' + name
        try:
            self.c.execute("INSERT INTO %s(MESSAGE) VALUES(?)"%(queue_name,),(message,))
            self.conn.commit()
        except Exception as e:
            print('push message!! failed : ',e)
            self.conn.rollback()
            return False
        else:
            return True
    
    def popFILO(self, name):
        queue_name = 'queue_' + name
        try:
            cursor = self.c.execute('SELECT MESSAGE,ID FROM %s ORDER BY ID DESC LIMIT 1')
            result = cursor.fetchall()[0]
            self.c.execute('DELETE FROM %s WHERE ID=?'%(queue_name,),(result[1],))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            return None
        else:
            return result

    def popFIFO(self, name):
        queue_name = 'queue_' + name
        try:
            cursor = self.c.execute('SELECT MESSAGE,ID FROM %s ORDER BY ID  LIMIT 1'%(queue_name,))
            result = cursor.fetchall()[0]
            self.c.execute('DELETE FROM %s WHERE ID=?'%(queue_name,),(result[1],))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            return None
        else:
            return result

    def lenQueue(self, name):
        queue_name = 'queue_' + name
        try:
            cursor = self.c.execute('SELECT COUNT(*) FROM %s'%(queue_name,))
            result = cursor.fetchall()[0][0]
        except Exception as e:
            print('is empty queue run wrong : ', e)
            return 0
        else:
            return result

    def clearQueue(self, name):
        queue_name = 'queue_' + name
        try:
            self.c.execute('DELETE FROM %s'%(queue_name,))
            self.conn.commit()
        except Exception as e:
            print('clear Queue failed : ', e)
            self.conn.rollback()
            return False
        else:
            return True
            
            



        

