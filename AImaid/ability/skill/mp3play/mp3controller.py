from .source.sougou.sougouyinyue import *
from ....core.model.ability.model_mp3player import Mp3PlayerM


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

    def action(self, data):
        print(data['user']+': '+data['text'])
        cmd = data['cmd']
        operation = None
        retmsg = None
        if cmd == 'switch':
            self.switch()
            operation = None
            retmsg = None
        elif cmd == 'search':
            self.songlist = self.search(data['songname'])
            if self.songlist == None:
                retmsg = '抱歉喵，未找到你点播的歌曲'
                operation = 'talk'
            else:
                retmsg = '已完成搜索，请从列表中选择: '
                strlist = ''
                for i, song in enumerate(self.songlist):
                    strlist = strlist + str(i) + '.' + song['singer'] + '_' + song['name'][0:10] + ';'
                retmsg = retmsg + strlist
                operation = None
        elif cmd == 'select' and self.songlist != [] and self.songlist != None:
            selectnum = int(data['selectnum'])
            if selectnum < 0 or selectnum >= self.songlist.__len__():
                selectnum = 0
            song = self.songlist[selectnum]
            flag = self.dianboPlay(song)
            if flag == True:
                retmsg = data['user'] + ',' + '点播' + song['singer'] + '的' + song['name'][0:10] + ' 成功'
                operation = 'talk'
            else:
                retmsg = '对不起，' + data['user'] + ',' + '点播' + song['singer'] + '的' + song['name'][0:10] + ' 失败'
                operation = 'talk'

        return (operation, retmsg)



