import requests
import re
import bs4
import os

class SouGouMusicAPI():
    def __init__(self):
        self.cookies = {'CXID':'8395F0B8372971B31129DD3ED90998C7',
            'SUID':'7AF281B76573860A56CD6C8E0005DC29',
            'MP3SSUID':'C28B582F9A98A6ABF55D868914ABDDCA',
            'SUV':'00345E702F588BC2583FEA98ABA4C585',
            'IPLOC':'CN',
            'usid':'C28B582FC535900A00000000583FED74'}
        self.searchurl = 'http://mp3.sogou.com/music.so?st=1&debug=null&comp=1&page=1&len=30&query='
        self.headers = {'Referer':'http://mp3.sogou.com/music.so?query=%BA%F3%CC%EC&class=1&st=1&p=&w=&interV=',
            'User-Aget':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        self.s = requests.session()
        self.s.get('http://mp3.sogou.com',headers=self.headers, cookies=self.cookies)
        #self.mp3savepath = 'resource/mp3/BGM/playlist/diange/'
        self.mp3savepath = '/root/mp3/BGM/playlist/diange/'
        self.mp3 = ''



    def search(self, name, num=3):
        try:
            res = self.s.get(self.searchurl+name)
        except Exception as e:
            print(e)
            return False
        else:
            try:
                soup = bs4.BeautifulSoup(res.content.decode('gb2312','ignore'),'html.parser')
                slist = soup.find_all('li')
                if slist != []:
                    if slist.__len__() <= num:
                        num = slist.__len__()
                    else:
                        pass
                else:
                    return None
                songs = []
                for i in range(0,num):
                    mp3 = {}
                    song = slist[i]['param']
                    res = song.split('#,#')
                    mp3['link'] = res[2]
                    mp3['name'] = res[3]
                    mp3['singer'] = res[5]
                    songs.append(mp3)
            except Exception as e:
                print(e)
                return None
            else:
                return songs

    def checkExist(self, mp3name):
        return os.path.exists(self.mp3savepath + mp3name + '.mp3')

    def downloadMP3(self, song):
        mp3name = song['singer'] + '_' + song['name']
        if not self.checkExist(mp3name):
            mp3file = open(self.mp3savepath+mp3name+'.mp3', 'wb')
            try:
                mp3content = self.s.get(song['link'])
            except Exception as e:
                print(e)
                return 2
            mp3file.write(mp3content.content)
            mp3file.close()
            self.mp3 = self.mp3savepath + mp3name + '.mp3'
            return 0
        else:
            self.mp3 = self.mp3savepath + mp3name + '.mp3'
            return 1

    def getMP3FilePath(self):
        return self.mp3




if __name__ == "__main__":
    sg = SouGouMusicAPI()
    a = sg.search('脳浆炸裂ガール')
    print(a)

        
