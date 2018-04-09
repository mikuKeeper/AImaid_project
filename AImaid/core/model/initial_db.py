import sqlite3
from main.model_message_queue import MessageQueueM


try:
    conn = sqlite3.connect('maid.db')
except Exception as e:
    print('error:',e)
else:
    print('opened database successfully')

c = conn.cursor()
#try to drop table if it is exist
try:
    c.execute('DROP table maid_status;')
    c.execute('DROP table action_status;')

    conn.commit()
except Exception as e:
    print(e)
else:
    print('drop maid successfully')
print('###########################')

#create table
try:
    c.execute('''CREATE TABLE maid_status
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        STATUS_NAME TEXT NOT NULL,
        STATUS_VALUE TEXT NOT NULL);''')

    c.execute('''CREATE TABLE action_status
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        STATUS_NAME TEXT NOT NULL,
        STATUS_VALUE TEXT NOT NULL);''')
 
    conn.commit()
except Exception as e:
    print('create table failed :',e)
    exit()
else:
    print('create table successfully')

print('###########################')
#insert default values
try:
    #initial maid status value
    c.execute("INSERT INTO maid_status(STATUS_NAME,STATUS_VALUE)\
            VALUES('isbusy',?)",(str(False),))
    #initial mp3 status value
    c.execute("INSERT INTO action_status(STATUS_NAME,STATUS_VALUE)\
            VALUES('mp3player_dianbo_isbusy',?)",(str(False),))
    
    c.execute("INSERT INTO action_status(STATUS_NAME,STATUS_VALUE)\
            VALUES('mp3player_defaultBGM_switch',?)",(str(False),))

    #add more if you need

    

    conn.commit()
except Exception as e:
    print('initial the default value failed: ', e)
    exit()
else:
    print('initial the default value successfully')

print('###########################')

#create base queue
mqM = MessageQueueM(conn)
base_queue_list = ['originalmessage', 'chatmessage','musiccmd','dianbo']
for n in base_queue_list:
    mqM.createNewQueue(n)
print('create queues finished')
print('###########################')
