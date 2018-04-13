from AImaid.core.components.message.selector import MessageSelector

class MainService():
    def __init__(self):
        self.messelector = MessageSelector()

    def run(self):
        self.messelector.messageHub()

if __name__ == '__main__':
    ms = MainService()
    ms.run()
