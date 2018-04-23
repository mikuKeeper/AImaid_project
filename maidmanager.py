import threading
import sys
import os
import subprocess
import time
import sqlite3
from AImaid.core.model.main.model_maid import MaidM
import platform

flask_env = os.environ.copy()
flask_env['FLASK_APP'] = 'startweb.py'
workpath = os.path.dirname(os.path.abspath(__file__))
if platform.architecture()[1] == 'WindowsPE':
    py = 'python.exe'
else:
    py = 'python3.6'
M = MaidM()
if M.setBusy(False):
    print('initial status successfully')
else:
    print('initial status failed')
    print('maid stop')
    exit()

def maidthread():
    M2 = MaidM()

    child = subprocess.Popen([py,os.path.join(workpath,'maid.py')])
    time.sleep(1800)
    while True:
        if M2.getBusy() == False:
            child.kill()
            sys.exit()
        time.sleep(1)

def othersthread():
    sense = subprocess.Popen([py,os.path.join(workpath,'maid_sense.py')],creationflags =subprocess.CREATE_NEW_CONSOLE)
    mainservice = subprocess.Popen([py,os.path.join(workpath,'maid_mainservice.py')],creationflags =subprocess.CREATE_NEW_CONSOLE)
    webservice = subprocess.Popen(['flask','run'],env=flask_env,creationflags =subprocess.CREATE_NEW_CONSOLE)



thread_b = threading.Thread(target=othersthread)
thread_b.setDaemon(True)
thread_b.start()
while True:
    thread_a = threading.Thread(target=maidthread)
    thread_a.setDaemon(True)
    thread_a.start()
    thread_a.join()
    
    print('reset maid')



