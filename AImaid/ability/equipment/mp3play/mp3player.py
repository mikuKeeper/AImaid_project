import pygame
import random
import os
import subprocess
import wave
from ....core.model.ability.model_mp3player import Mp3PlayerM


class MP3Player():
    def __init__(self):
        #pygame.init(frequency=16000)
        self.M = Mp3PlayerM()
        self.defaultBGMpath = '/root/mp3/BGM/playlist/default/'
        self.defaultmp3list = self.fetchDefaultMP3List()
        #pygame.mixer.init(frequency=16000, size=-16, channels=2, buffer=4096)
        pygame.mixer.init(frequency=44100)

    def mp3ToWave(self, filepath):
        filename = os.path.splitext(filepath)[0]
        print(filename)
        wavefile = filename+'.wav'
        if not os.path.exists(wavefile):
            try:
                fb = open('/dev/null','r')
                child = subprocess.Popen(['ffmpeg', '-i', filepath,wavefile],stdout=fb, stderr=fb)
                fb.close()
                child.wait()
                print('transform')
            except Exception as e:
                print(e)
                return False
            else:
                return wavefile
        else:
            return wavefile
    

    def playMp3(self, filepath):
        print(filepath)
        res = self.mp3ToWave(filepath)
        if res != False:
            psound = pygame.mixer.Sound(res)
            psound.set_volume(0.4)
            try:
                psound.play()
            except Exception as e:
                print('playerror')
                print(e)
                return False
            else:
                return psound

    def dianbo(self, filepath):
        psound = self.playMp3(filepath)
        return psound

    def fetchDefaultMP3List(self):
        mp3list = []
        filelist = os.listdir(self.defaultBGMpath)
        for mp3 in filelist:
            filepath = self.defaultBGMpath+mp3
            mp3list.append(filepath)
        return mp3list


    def playDefaultBGM(self):
        mp3num = self.defaultmp3list.__len__()
        while True:
            dbflag = 0
            dblen = self.M.lenDianbo()
            if dblen == 0:
                mp3 = self.defaultmp3list[random.randint(0,mp3num-1)]
                psound = self.playMp3(mp3)
                dbsound = psound
            else:
                dianbomp3 = self.M.popDianbo()
                dblen = self.M.lenDianbo()
                if dianbomp3 != None:
                    dbflag = 1
                    dbsound = self.dianbo(dianbomp3)
            while pygame.mixer.get_busy():
                pygame.time.delay(5)
                if dblen > 0 and dbflag == 0:
                    dianbomp3 = self.M.popDianbo()
                    dblen = self.M.lenDianbo()
                    if dianbomp3 != None:
                        dbflag = 1
                        dbsound.stop()
                        dbsound = self.dianbo(dianbomp3)
                if self.M.getDefaultBGMSwitchFlag():
                    #psound.stop()
                    dbsound.stop()
                    self.M.setDefaultBGMSwitchFlag(False)
                    pygame.time.delay(1000)




if __name__ == '__main__':
    mp = MP3Player()
    mp.playDefaultBGM()



            



        



