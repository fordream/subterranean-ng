# -*- coding: utf-8 -*-
import os
import imp
import pygame
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
        self.pos1 = (0,0)
        self.pos2 = (0,0)
        self.cameraPos = (0,0)
        self.exits = []
        
    def setPos1(self,pos):
        self.pos1 = pos
    
    def setPos2(self,pos):
        self.pos2 = pos
        
    def setCameraPos(self,pos):
        self.cameraPos = pos
                
    def getName(self,sceneName):
        self.name = sceneName
        
    def getName(self):
        return self.name
        
    def getBackground(self):
        return self.backgroundImage
        
    def setBackground(self,backgroundImage):
        self.backgroundImage = pygame.image.load(os.path.join('data','backgrounds',backgroundImage)).convert()
        
    def addVisibleElement(self,element):
        self.visibleElements.add(element)
              
    def getElement(self,elementName):
        for element in self.visibleElements:
            if element.name == elementName:
                return element
        
    def setInsertPoint(self,pos):
        #TODO: Check that it is a valid placement on the map
        posX = pos[0]/16
        posY = pos[0]/16
        
        
        self.insertPoint = pos
        self.Game.Player.setPosition(pos)

    def show(self):
        self.visible = True
        
    def setMap(self,mapFileName):
        self.mapFileName = mapFileName
        self.loadMap(mapFileName)

    #This is just me being lazy. Coda makes a neat line of the syntax highlight if I have 1 and x.
    def loadMap(self,mapFileName):
        self.mapFile = open(os.path.join('Scenes',mapFileName))
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