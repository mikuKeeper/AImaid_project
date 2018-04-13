from AImaid.ability.equipment.mp3play.mp3player import MP3Player

class AllAbilities():
    def __init__(self):
        self.ability_mp = MP3Player()

    def run(self):
        self.ability_mp.playDefaultBGM()

if __name__ == '__main__':
    allabilities = AllAbilities()
    allabilities.run()
