# -*- coding: utf-8 -*-
import os,pygame
from time import time
    
class Timer:
    def __init__(self):
        pass
        
    def setFPS(self,fps):
        self.currentFrame = 0
        if fps == 0: 
            self.tick = self._blank
            return
        self.wait = 1000/fps
        self.nt = pygame.time.get_ticks()
        pygame.time.wait(0)
    
    def _blank(self):
        pass
    
    def tick(self):
        self.currentTicks = pygame.time.get_ticks()
        if self.currentTicks < self.nt:
            pygame.time.wait(self.nt-self.currentTicks)
            self.nt+=self.wait
        else: 
            self.nt = pygame.time.get_ticks()+self.wait
        self.currentFrame += 1
