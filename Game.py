import os,pygame
from Constants import *
from Player import Player
from Engines import Renderer,AudioController,EventManager,Timer
from Interfaces import ConversationManager,Cursor,Inventory,TitleManager

class Game:
    def __init__(self,arguments):
        self.debug = False;
        self.running = True;
        self.fullscreen = False
        self.paused = False
        self.currentScene = None;

        self.TitleManager = TitleManager(self)
        self.Cursor = Cursor(self)
        self.Renderer = Renderer(self)
        self.Inventory = Inventory(self)
        self.AudioController = AudioController(self)
        self.ConversationManager = ConversationManager(self)
        self.Player = Player(self)
        self.EventManager = EventManager(self)

        self.loadScene("someScene")
        self.parseArguments(arguments)
        self.run()
        
    def parseArguments(self,arguments):
        avalibleArguments = {
            '--nomusic':self.AudioController.disableMusic,
            '--nosound':self.AudioController.disableSound,
        }
        
        for argument in avalibleArguments.keys():
            if argument in arguments:
                argumentMethod = avalibleArguments.get(argument)
                argumentMethod()

    def pause(self):
        #TODO: Fix later
        self.paused = False

    def unpause(self):
        self.paused = False
    
    def loop(self):
        while self.running:
            self.EventManager.checkEvents()
            self.Renderer.Timer.tick()
            self.Renderer.draw()

    def loadScene(self,sceneName):
        from Scenes.Foo import Room
        self.currentScene = Room(self)
        
    def quit(self):
        self.running = False

    def run(self):
        self.loop()
        
    def toggleFullscreen(self):
        if self.fullscreen == False:
            self.fullscreen = True
            self.Renderer.setupScreen(True)
        else:
            self.fullscreen = False
            self.Renderer.setupScreen(False)
        
    def dump(self):
        if self.debug:
            self.debug = False
        else:
            self.debug = True