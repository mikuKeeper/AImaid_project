from AImaid.sense.word_input import CmdlineInput

class AllInput():
    def __init__(self):
        self.ci = CmdlineInput()

    def run(self):
        while True:
            self.ci.cmdInput()

if __name__ == "__main__":
    ai = AllInput()
    ai.run()
        
