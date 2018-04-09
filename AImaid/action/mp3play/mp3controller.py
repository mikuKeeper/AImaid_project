from .source.sougou.sougouyinyue import *
#from common_unit.my_redis import *
from ...core.model.action.model_mp3player import Mp3PlayerM


class MP3Controller():
    def __init__(self):
        self.src1 = SouGouMusicAPI()
        self.M = Mp3PlayerM()

    def search(self, name):
        songlist = self.src1.search(name)
        return songlist

    def dianboPlay(self, song):
        flag = self.src1.downloadMP3(song)
        if flag == 0 or flag == 1:
            file = self.src1.getMP3FilePath()
            self.M.pushDianbo(file)
            return True

        elif flag == 2:
            return False

    def switch(self):
        self.M.setDefaultBGMSwitchFlag(True)



