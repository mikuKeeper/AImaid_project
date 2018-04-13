import threading
import sys
import os
import subprocess
import time
import sqlite3
from AImaid.core.model.main.model_maid import MaidM

workpath = os.path.dirname(os.path.abspath(__file__))

M = MaidM()
if M.setBusy(False):
    print('initial status successfully')
else:
    print('initial status failed')
    print('maid stop')
    exit()

def maidthread():
    M2 = MaidM()
    child = subprocess.Popen(['python3',os.path.join(workpath,'maid.py')])
    time.sleep(1800)
    while True:
        if M2.getBusy() == False:
            child.kill()
            sys.exit()
        time.sleep(1)
    

while True:
    thread_a = threading.Thread(target=maidthread)
    thread_a.setDaemon(True)
    thread_a.start()
    thread_a.join()
    print('reset maid')



