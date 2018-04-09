from AImaid.action.mp3play.mp3player import MP3Player

class AllActions():
    def __init__(self):
        self.action_mp = MP3Player()

    def run(self):
        self.action_mp.playDefaultBGM()

if __name__ == '__main__':
    allactions = AllActions()
    allactions.run()
