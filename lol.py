import os, math, pygame
import pygame.locals as pygl

class Audio :

    def __init__(self, audioFile) :
        pygame.mixer.init();
        self.setStatus('initialized')
        self.setFile(audioFile)
    
    def setStatus(self, audioStatus) :
        self.audioStatus = audioStatus
    
    def getStatus(self) :
        return self.audioStatus
    
    def setFile(self, audioFile) :
        self.audioFile = audioFile
        self.audio = pygame.mixer.Sound(audioFile)
    
    def getFile(self) :
        return self.audioFile
    
    def setChannel(self, channelNumber) :
        self.channelNumber = channelNumber
        self.channel = pygame.mixer.Channel(channelNumber)
    
    def getChannel(self) :
        return self.channel
        
    def getChannelNumber(self) :
        return self.channelNumber
    
    def setVolume(self, volume) :
        self.audioVolume = volume
        self.channel.set_volume(volume)
    
    def getVolume(self) :
        return self.audioVolume
    
    def setPan(self, balance) :
        self.audioBalance = balance
        left = abs(balance)
        right = abs(left - 1.0)
        self.channel.set_volume(left, right)
    
    def getPan(self) :
        return self.audioBalance
    
    def getLength(self) :
        return self.audio.get_length()
        
    def play(self) :
        self.channel.play(self.audio)
        


pygame.display.get_surface()
pygame.display.set_mode()
pygame.display.set_caption('Subterranean')

def loop():
    running = True
    while running:
        pygame.event.pump()
    
            
ambi = Audio('data/music/default.ogg')
ambi.setChannel(1)
ambi.play()
loop()
