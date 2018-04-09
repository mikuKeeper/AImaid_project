import threading
import os
import subprocess
import time
import sqlite3
from AImaid.core.model.main.model_maid import MaidM
#from common_unit.my_redis import *
#r = MyRedis()
#rcon = r.connect()
#maidbusykey = 'bilibili:danmumaid:isbusy'
#rcon.set(maidbusykey,False)
M = MaidM()
if M.setBusy(False):
    print('initial status successfully')
else:
    print('initial status failed')
    print('maid stop')
    exit()

fb = open('/dev/null')

def maidthread():
    child = subprocess.Popen(['python3','maid.py'])
    time.sleep(1800)
    while True:
        if rcon.get(maidbusykey).decode('utf8') == 'False':
            child.kill()
            sys.exit()
        time.sleep(1)
    

while True:
    thread_a = threading.Thread(target=maidthread)
    thread_a.setDaemon(True)
    thread_a.start()
    thread_a.join()
    print('reset maid')



