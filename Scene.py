import os
import pygame

class Scene:
    def __init__(self,game):
        self.Game = game
        self.visible = False
        self.name = None
        self.mapFileName = None
        self.visibleElements = pygame.sprite.Group()
        self.hiddenElements = pygame.sprite.Group()
        self.mapData = []
        self.insertPoint = ()
        self.backgroundImage = None
        
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