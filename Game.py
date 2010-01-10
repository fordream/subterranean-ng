# -*- coding: utf-8 -*-
import os,sys,time,pygame,imp
from Constants import *
from Loader import Loader
from Player import Player
from Renderer import Renderer
from AudioController import AudioController
from EventManager import EventManager
from ScriptManager import ScriptManager
from Cursor import Cursor
from Inventory import Inventory
from TitleManager import TitleManager
from TopicMenu import TopicMenu

class Game:
    def __init__(self,arguments):
        self.debug = False
        self.capturing = False
        self.captureFPSWait = 0
        self.running = True
        self.fullscreen = False
        self.paused = False
        self.cachedScenes = {}
        self.currentScene = None
        self.currentElement = None
        self.currentWindow = None
        self.currentWidget = None
        
        self.values = {}

        self.Loader = Loader(self)
        self.setupScreen()
        self.setupAudio()
        self.displayTitle()
        self.Loader.preload()

        self.TitleManager = TitleManager(self)
        self.Cursor = Cursor(self)
        self.Renderer = Renderer(self)
        self.AudioController = AudioController(self)
        
        
        self.Inventory = Inventory(self)
        self.TopicMenu = TopicMenu(self)

        self.ScriptManager = ScriptManager(self)
        self.Player = Player(self)
        self.EventManager = EventManager(self)
        self.parseArguments(arguments)

        self.loadScene("blacksmith")
        self.run()
        
    def setupScreen(self,fullscreen=False):
        #There seems to be no way to make this work right other than doing this:
        if fullscreen:
            self.window = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode((1024,768),pygame.NOFRAME)
        pygame.display.set_caption('Subterranean')
        
    def displayTitle(self):
        #Temporary but neat
        logo = pygame.image.load(os.path.join('data','ui','logo.png'))
        self.window.blit(logo,(self.window.get_rect().centerx - logo.get_width()/2,self.window.get_rect().centery - logo.get_height()/2))
        pygame.display.flip()
    
    def setupAudio(self):
        pygame.mixer.init(44100)
        
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
            self.Renderer.draw()
            self.Renderer.Timer.tick()

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
            self.setupScreen(True)
        else:
            self.fullscreen = False
            self.setupScreen(False)
            
    def log(self,value):
        #TODO: Something fancier here.
        print value
        
    def setValue(self,key,value):
        self.values[key] = value
    
    def getValue(self,key):
        return self.values.get(key)
        
    def dump(self):
        if self.debug:
            self.debug = False
        else:
            self.debug = True
                        
    def toggleCapture(self):
        if self.capturing:
            self.capturing = False
            print "Stopped capturing. Saving to disk"
            count = 0
            print "Got",len(self.capturedImages),"images"
            for image in self.capturedImages:
                pygame.image.save(image,'/Users/kallepersson/Desktop/captures/capture-'+str(count)+'.png')
                count+=1
            self.capturedImages = []
            print "Done"
        else:
            print "Started capturing"
            self.capturedImages = []
            self.captureFPSWait = 0
            self.capturing = True
            
    def captureScreen(self):
        if self.captureFPSWait > 2:
            self.capturedImages.append(self.Renderer.screen.copy())
            self.captureFPSWait = 0
        else:
            self.captureFPSWait+=1
            
    def get(self,key):
        return self.Loader.get(key)