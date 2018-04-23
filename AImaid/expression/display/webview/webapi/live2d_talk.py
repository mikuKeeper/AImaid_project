from .....core.model.main.model_message_queue import MessageQueueM
import json


M = MessageQueueM()
talkq = 'talkmsg'


def getTextUrl():
    data = {'status':0, 'message':''}
    msg = getMsg()
    if msg == None:
        data['status'] = 1
        data['message'] = ''
    else:
        data['status'] = 0
        data['message'] = msg
    return json.dumps(data)


def getMsg():
    return M.popFIFO(talkq)