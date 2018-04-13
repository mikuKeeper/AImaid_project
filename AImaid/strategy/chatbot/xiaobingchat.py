import requests
import time
import json
import random

class XiaoBing():
    def __init__(self):
        self.s = requests.session()
        self.accounts = []
        account1 = {'yktk':'1%7C1479910468%7C15%7CaWQ6MTA1NTE5OTk4NCxubjrkvJjphbfnlKjmiLc5MDc1Mjc5NjgzLHZpcDpmYWxzZSx5dGlkOjEwNTUxOTk5ODQsdGlkOjA%3D%7Cff1697e874cd99d3acbb5fc1e3c96fca%7C97e8bfe000118fdff75e0b3acdefd21d390b930b%7C1',
        'su':'1055199984',
        'sender_id':'1055199984'}
        #self.accounts.append(account1)
        account2 = {'yktk':'1%7C1480158162%7C15%7CaWQ6MTA1ODczMDkzMSxubjrkvJjphbfnlKjmiLc1MzE3NTY1NzI1LHZpcDpmYWxzZSx5dGlkOjEwNTg3MzA5MzEsdGlkOjA%3D%7Cfa7c44257be692ae799eea5efa5dbb47%7C94e2ab0e1f4c8197abff4242d3e84cb0c9544419%7C1',
        'su':'1058730931',
        'sender_id':'1058730931'}
        #self.accounts.append(account2)
        account3 = {'yktk':'1%7C1483288252%7C15%7CaWQ6MTA4MTU2ODczMyxubjrkvJjphbfnlKjmiLc1OTEzNTAwNjM4LHZpcDpmYWxzZSx5dGlkOjEwODE1Njg3MzMsdGlkOjA%3D%7Cc48fb51c7c4c934e69ba7a7d4074830c%7C3c7f95f812cc38cd2c3afb0ef956228cea01c09b%7C1',
        'su':'1081568733',
        'sender_id':'1081568733'}
        self.accounts.append(account3)
        #self.account = self.accounts[random.randint(0,2)]
        self.account = self.accounts[0]
        self.cookie={'yktk':self.account['yktk']}
        self.data1={'su': self.account['su'], 'msg': '舔舔', 'ru': '814677438', 'msg_limit': '500'}
        self.data2={'content_type': 'text', 'sender_id': self.account['sender_id'], 'mid': '226779520', 'msxiaoice_uid': '814677438', 'content': '么么哒'}
        self.reqhost1 = 'http://i.youku.com/u/audience/fun/postMsg'
        self.reqhost2 = 'http://i.youku.com/u/audience/fun/sendMsgToMSxiaoice'
        self.heartbeathost = 'http://i.youku.com/u/audience/fun/getNewMsg?su='+ self.account['su'] +'&ru=814677438'

    def chat(self, send_msg):
        while True:
            try:
                res1 = self.s.post(self.reqhost1, data=self.data1, cookies=self.cookie) 
                j = res1.json()
                self.data2['mid'] = j['mid']
                self.data2['content'] = send_msg
            except Exception as e:
                time.sleep(1)
                print(e)
            else:
                break
            
        while True:
            try:
                res2 = self.s.post(self.reqhost2, data=self.data2)
            except Exception as e:
                time.sleep(1)
                print(e)
            else:
                break
        i = 0
        while True:
            time.sleep(0.5)
            try:
                j = self.s.get(self.heartbeathost)
                i = i + 1
            except Exception as e:
                continue

            if j.content.decode('utf8') == '0':
                if i > 30:
                    return "unknown error(2)"
                continue
            else:
                try:
                    j = j.json()
                    msg = j[0]['content']
                except Exception as e:
                    print(e)
                    return "unknown error(1)"
                else:
                    break
        return msg

class DanMuClient():
    def __init__(self, roomId):
        self.roomid = roomId
        #shuang dao liu de jita
        #self.cookie={'sid':'4zn87a4u','LIVE_BUVID':'2314be94039c0d1620048081f4442015','LIVE_BUVID__ckMd5':'2a6bfd7979bf4c70','buvid3':'6DFDF6E8-B32F-4A56-BA36-5E574EC8D8C55838infoc','DedeUserID':'50325048','DedeUserID__ckMd5':'318f61fe64bd4aba','SESSDATA':'81f5a5d8%2C1482330272%2C73285f6c','LIVE_LOGIN_DATA':'a78ddfe2038ad022fd7855b1e4655971f8a18387','LIVE_LOGIN_DATA__ckMd5':'bb9ea6f47c84b804'}
        self.cookie={'sid':'9uvg7qr1',
            'LIVE_BUVID':'176135b1ed8415790aaa01e593ae9c5c',
            'LIVE_BUVID__ckMd5':'b597ad6f810ef3bf',
            'buvid3':'56AB549B-D9E7-46CA-AE6A-E58624E53F5A28574infoc',
            'DedeUserID':'61264019',
            'DedeUserID__ckMd5':'f5e692e9ddf5ffb4',
            'SESSDATA':'be9f5a10%2C1485883179%2C41f88fe9',
            'LIVE_LOGIN_DATA':'505caae16dfe0d6832b3e256c235b5e8f3868526',
            'LIVE_LOGIN_DATA__ckMd5':'883d869ca0f2da8e'}
        self.send_data = {'color':'16777215','fontsize':'25','mode':'1','msg':'test','rnd':str(time.time())[0:-7],'roomid':self.roomid}
        self.reqhost = "http://live.bilibili.com/msg/send"
        self.s = requests.session()
        self.headers = {'User-Agent':"Mozilla/5.0 (X11; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0 Iceweasel/43.0.4"}

    def sendDanmu(self, msg):
        msglen = msg.__len__()
        x = msglen // 20
        for i in range(0,x+1):
            time.sleep(0.5)
            submsg = msg[20*i:20*(i+1)]
            self.send_data['msg'] = submsg
            try:
                res = self.s.post(self.reqhost, data=self.send_data, cookies=self.cookie,headers=self.headers,timeout=5)
            except Exception as e:
                return False
            try:
                rescode = res.json()['code']
            except Exception as e:
                return False
            if rescode == 0:
                pass
            else:
                print('test')
                print(rescode)
                return False
        return True
       
