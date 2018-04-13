import requests
import pygame
import subprocess, os
from ...core.model.main.model_maid import MaidM

class BaiduYuyin(): 
    def __init__(self):
        workpath = os.path.dirname(os.path.abspath(__file__))
        self.voicepath = os.path.join(workpath,'tmp')
        self.apikey = 'Hc0nybVln8WrL96O6cZkXggn'
        self.secretkey = 'd1a0fd4ad85d7c69752636330fda71a5'
        self.authurl = 'https://openapi.baidu.com/oauth/2.0/token?'
        self.tsnurl = 'http://tsn.baidu.com/text2audio'
        self.M = MaidM()
        self.token = self.fetchToken()
        self.chunk = 1024
        pygame.mixer.init(frequency=16000)

    def fetchToken(self):
        res = requests.get(self.authurl + 'grant_type=client_credentials' + '&client_id=' + self.apikey + '&client_secret=' + self.secretkey)
        j = res.json()
        return j['access_token']

    def postText(self, msg):
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
        while True:
            try:
                res = requests.post(self.tsnurl,data=data)
            except Exception as e:
                print('x1')
                print(e)
                continue
            else:
                break
        fb = open(os.path.join(self.voicepath, 'voice.mp3'),'wb')
        fb.write(res.content)
        fb.close()

    def playMp3(self):
        try:
            fb = open('/dev/null','r')
            child = subprocess.Popen(['ffmpeg','-y', '-i', os.path.join(self.voicepath, 'voice.mp3'), os.path.join(self.voicepath, 'voice.wav')],stdout=fb, stderr=fb)
            fb.close()
            child.wait()
        except Exception as e:
            print(e)
        else:
            psound = pygame.mixer.Sound(os.path.join(self.voicepath,'voice.wav'))
            try:
                psound.play()
                psound.set_volume(1)
            except Exception as e:
                print('play error')
                print(e)
            self.M.setBusy(True)
            while pygame.mixer.get_busy():
                pygame.time.delay(5)
            self.M.setBusy(False)


if __name__ == '__main__':
    bdyy = BaiduYuyin()
    bdyy.postText('我爱你')
    #bdyy.playWave()
    bdyy.playMp3()
    
        
        
        
        

