from ..core.components.message.filter import MessageFilter
from .chatbot import *

chatbot = tulingbot.Tuling()
msgfilter = MessageFilter()

def chatReact(data):
    if data['type'] == '0':
        print(data['commentuser']+': '+data['text'])
        flag, msg = msgfilter.inputFilter(data['text']) 
        if flag == False:
            retmsg = chatbot.chat(msg)
            retmsg = msgfilter.outputFilter(retmsg)
        else:
            retmsg = msg
        if data['commentuser'] != 'system':
            return retmsg
        else:
            return retmsg
