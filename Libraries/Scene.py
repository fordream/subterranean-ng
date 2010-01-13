# -*- coding: utf-8 -*-
import os,imp,time,pygame
from Elements import Exit

class Scene:
    def __init__(self,game):
        self.Game = game
        self.Game.currentRoom = self
        self.visible = False
        self.name = None
        self.mapFileName = None
        self.visibleElements = pygame.sprite.Group()
        self.hiddenElements = pygame.sprite.Group()
        self.mapData = []
        self.insertPoint = ()
        self.backgroundImage = None
        self.foregroundImage = None
        self.farthestPoint = 250
        self.closestPoint = 768
        self.farthestScale = 50
        self.closestScale = 100
        self.exits = []
        
    def setFarthestPoint(self,pos):
        self.farthestPoint = pos
    
    def setClosestPoint(self,pos):
        self.closestPoint = pos

    def setFarthestScale(self,scale):
        self.farthestScale = scale
    
    def setClosestScale(self,scale):
        self.closestScale = scale
                        
    def getName(self,sceneName):
        self.name = sceneName
        
    def getName(self):
        return self.name
        
    def getBackground(self):
        return self.backgroundImage
        
    def setBackground(self,backgroundImage):
        self.backgroundImage = self.Game.get(backgroundImage)

    def getForeground(self):
        return self.foregroundImage

    def setForeground(self,foregroundImage):
        self.foregroundImage = self.Game.get(foregroundImage)
        
    def addVisibleElement(self,element):
        self.visibleElements.add(element)
              
    def getElement(self,elementName):
        for element in self.visibleElements:
            if element.name == elementName:
                return element
        
    def setInsertPoint(self,pos):
        #TODO: Check that it is a valid placement on the map
        posX = pos[0]/16
        posY = pos[1]/16
        self.insertPoint = pos

        #Sadly neccesary    
#        self.Game.Player.scaleImage()
        self.Game.Player.setPosition(pos)
        
    def show(self):
        self.Game.Renderer.fadeIn()
        self.visible = True
        
    def setMap(self,mapFileName):
        self.mapFileName = mapFileName
        self.loadMap(mapFileName)

    #This is just me being lazy. Coda makes a neat line of the syntax highlight if I have 1 and x.
    def loadMap(self,mapFileName):
        self.mapFile = open(os.path.join('Assets','Maps',mapFileName))
        mapTiles = self.mapFile.read().rsplit(',')
        for tile in mapTiles:
            tile = tile.replace('x','-1')
            try:
                self.mapData.append(int(tile))
            except:
                pass
        
        return 
        for line in self.mapFile:
            for char in line.rsplit(','):
                if char == 'x':
                    self.mapData.append(-1)
                elif char == '1':
                    self.mapData.append(int(char))
        print self.mapData
        self.mapFile.close()
        
    def loadItem(self,itemName):
        return self.loadAsset('Items',itemName)

    def loadElement(self,elementName):
        return self.loadAsset('Elements',elementName)
        
    def loadCharacter(self,characterName):
        return self.loadAsset('Characters',characterName)
        
    def loadAsset(self,assetType,assetName):
        try:
            module = imp.load_source(assetName,os.path.join('Assets',assetType,assetName+'.py'))
            assetClass = getattr(module,assetName); 
            asset = assetClass(self.Game)
            return asset
        except IOError:
            print "Fatal error: Could not load",assetName,"from",assetType
            exit()

    def addExit(self,exitX,exitY,exitW,exitH,exitPoint,roomName,direction):
        exit = Exit()
        exit.setRect(pygame.Rect(exitX,exitY,exitW,exitH))
        exit.setSceneName(roomName)
        exit.setExitPoint(exitPoint)
        exit.setDirection(direction)
        self.exits.append(exit)
        
    def enter(self):
        pass
    
    def exit(self,sceneName):
        self.Game.AudioController.stopAmbience()
        self.Game.Renderer.fadeOut(self.Game.loadScene,sceneName)