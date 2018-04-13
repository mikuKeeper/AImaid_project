import pygame
import time
import threading
import os 
import queue
import sys
class Display():
    def __init__(self,position='middle'):
        #right_bottom
        #wpositionx = 3600
        #wpositiony = 700
        #middle
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(self.current_path,'..','..','resource','img','Animation')
        self.position = {'middle':'2600,500', 'right_bottom':'4200,1200'}
        self.action_queue = queue.Queue()
        os.environ['SDL_VIDEO_WINDOW_POS'] = self.position[position]
        talk_frames = []
        normal_frames = []
        for i in range(0,108):
            framex = pygame.image.load(os.path.join(img_path, 'NORMAL','NORMAL_'+str(i).zfill(6)+'.png'))
            normal_frames.append(framex)
        
        for i in range(0,93):
            framey = pygame.image.load(os.path.join(img_path, 'TALK','TALK_'+str(i).zfill(6)+'.png'))
            talk_frames.append(framey)
        #self.screen = pygame.display.set_mode([300,900],pygame.NOFRAME,32)
        self.screen = pygame.display.set_mode([300,400],pygame.NOFRAME,32)
        self.action_list = ['normal','talk','exit']
        self.action_map = {'normal':normal_frames, 'talk':talk_frames,'exit':[]}

    def runPlay(self):
        thread_a = threading.Thread(target=self.playAction)
        thread_a.setDaemon(True)
        thread_a.start()

        
    def playAction(self):
        n=0
        action_name = 'normal'
        frames = self.action_map[action_name]
        infoframe = pygame.image.load(os.path.join(self.current_path, '..','..','resource','img','info.jpg'))
        backframe = pygame.image.load(os.path.join(self.current_path, '..','..','resource','img','back.png'))
        rectmaid = pygame.Rect(0,500,300,400)
        #rectinfo = pygame.Rect(0,0,300,500)
        #self.screen.fill([255,255,255])
        #self.screen.blit(infoframe,[0,0])
        pygame.display.update()
        #self.screen.blit(infoframe,[0,0])
        while True:
            try:
                next_action = self.action_queue.get(block=False)
            except Exception as e:
                pass
            else:
                if next_action == 'exit':
                    print('exit thread')
                    break
                elif next_action != action_name:
                    frames = self.action_map[next_action]
                    action_name = next_action
                    n = 0
                else:
                    pass
            self.screen.fill([20,20,20])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            n=n+1
            if n>(len(frames))*1-1:
                n=0
            pygame.time.delay(10)
            #self.screen.blit(frames[int(n)],[0,500])
            self.screen.blit(frames[int(n)],[0,0])
            #pygame.display.update(rectmaid)
            pygame.display.flip()
            #self.screen.blit(infoframe,[0,0])
            #pygame.display.update(rectinfo)

    def nextAction(self, next_action):
        self.action_queue.put(next_action)



