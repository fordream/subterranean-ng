# -*- coding: utf-8 -*-
import os,sys,time,pygame,imp
from Constants import *
from Player import Player
from Engines import Renderer,AudioController,EventManager,Timer
from Interfaces import ScriptManager,Cursor,Inventory,TitleManager,TopicMenu

class Game:
    def __init__(self,arguments):
        self.debug = False;
        self.running = True;
        self.fullscreen = False
        self.paused = False
        self.cachedScenes = {}
        self.currentScene = None
        self.currentElement = None
        self.currentWindow = None
        self.currentWidget = None

        self.TitleManager = TitleManager(self)
        self.Cursor = Cursor(self)
        self.Renderer = Renderer(self)
        self.Inventory = Inventory(self)
        self.TopicMenu = TopicMenu(self)
        self.AudioController = AudioController(self)
        self.ScriptManager = ScriptManager(self)
        self.Player = Player(self)
        self.EventManager = EventManager(self)
        self.parseArguments(arguments)
        self.loadScene("Foo")
        self.run()
        
    def parseArguments(self,arguments):
        avalibleArguments = {
            '--fullscreen':self.toggleFullscreen,
            '--nomusic':self.AudioController.disableMusic,
            '--nosound':self.AudioController.disableSound,
        }
        
        for argument in avalibleArguments.keys():
            if argument in arguments:
                argumentMethod = avalibleArguments.get(argument)
                argumentMethod()

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False
    
    def loop(self):
        while self.running:
            self.EventManager.checkEvents()
            self.Renderer.Timer.tick()
            self.Renderer.draw()

    def loadScene(self,sceneName):
        if sceneName in self.cachedScenes:
            self.log("Got "+sceneName+" from cache")
            self.currentScene = self.cachedScenes.get(sceneName)
            #Run the enter method if it is not the first time we do
            self.currentScene.enter()
        else:
            self.log("Loaded "+sceneName+" from file")
            scene = imp.load_source(sceneName,os.path.join('Scenes',sceneName+'.py'))
            sceneClass = getattr(scene,'Room');
            self.currentScene = sceneClass(self)
            self.cacheScene(self.currentScene,sceneName)
        
    def cacheScene(self,sceneObject,sceneName):
        self.cachedScenes[sceneName] = sceneObject
        
    def quit(self,event=None):
        self.running = False
        sys.exit()

    def run(self):
        self.loop()
        
    def toggleFullscreen(self):
        if self.fullscreen == False:
            self.fullscreen = True
            self.Renderer.setupScreen(True)
        else:
            self.fullscreen = False
            self.Renderer.setupScreen(False)
            
    def log(self,value):
        #TODO: Something fancier here.
        print value
        
    def dump(self):
        if self.debug:
            self.debug = False
        else:
            self.debug = True