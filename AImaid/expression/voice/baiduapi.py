from ...core.model.main.model_maid import MaidM
from ...core.model.main.model_message_queue import MessageQueueM

import platform
import requests

class BaiduYuyinAPI(): 
    def __init__(self):
        self.apikey = 'Hc0nybVln8WrL96O6cZkXggn'
        self.secretkey = 'd1a0fd4ad85d7c69752636330fda71a5'
        self.authurl = 'https://openapi.baidu.com/oauth/2.0/token?'
        self.tsnurl = 'http://tsn.baidu.com/text2audio'
        self.M = MaidM()
        self.token = self.fetchToken()
        self.Mq = MessageQueueM()
        self.talkq = 'talkmsg'
       

    def fetchToken(self):
        res = requests.get(self.authurl + 'grant_type=client_credentials' + '&client_id=' + self.apikey + '&client_secret=' + self.secretkey)
        j = res.json()
        self.token = j['access_token']
        return j['access_token']

    def postText(self,msg):
        tsnurl = 'http://tsn.baidu.com/text2audio' + '?'
        data = {
            'tex':msg,
            'lan':'zh',
            'tok':self.token,
            'ctp':'1',
            'cuid':'xiaobingppap',
            'spd':'4',
            'pit':'8',
            'vol':'7',
            'per':'0',
            }
        for k, v  in data.items():
            tsnurl = tsnurl + '&' + k + '=' + v
        self.Mq.push(self.talkq, tsnurl)
     


  