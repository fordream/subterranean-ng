# -*- coding: utf-8 -*-
import os,sys,time,pygame
import pygame.locals as pygl        
    
class Editor:
    def __init__(self,arguments):
        print "Editor started"
        self.screen = pygame.display.set_mode((1024,768))
        pygame.display.set_caption('Subterranean')
        pygame.display.set_icon(pygame.image.load(os.path.join('Resources','Icons','gameicon.png')))
        self.running = True
        self.mapSize = 64*48
        self.mapFile = None
        self.tiles = []

        self.normalTile = pygame.Surface((16,16))
        self.normalTile.fill((0,255,255))
        self.normalTile.set_alpha(0)
        
        self.startTileEmpty = True
        
        self.blockingTile = pygame.Surface((16,16))
        self.blockingTile.fill((0,255,255))
        self.blockingTile.set_alpha(175)
        
        self.createTiles()
        
        if len(arguments) > 1 and arguments[1] is not "":
            try:
                self.setBackground(arguments[1]+'.jpg')
            except pygame.error:
                self.setBackground(arguments[1]+'.png')
            self.loadTiles(arguments[1]+'.map')
        else:
            exit("You must specify a room to edit.")
                    
        self.loop()
        
    def setBackground(self,background):
        self.background = pygame.image.load(os.path.join('Resources','Graphics','Backgrounds',background))
        
    def createTiles(self):
        rows = 0
        tiles = 0
        while rows <= 48:
            while tiles <= 64:
                self.tiles.append(Tile(tiles*16,rows*16))
                tiles+=1
            tiles = 0
            rows+=1

    def rearrangeTiles(self):
        row = 0
        counter = 0
        for tile in self.tiles:
            if counter >= 64:
                row+=1
                counter = 0
            tile.rect.top = row*16
            tile.rect.left = counter*16
            counter+=1    
        
    def loop(self):
        while self.running:
            self.checkEvents()
            self.draw()
            
    def clearTiles(self):
        self.tiles = []
            
    def loadTiles(self,mapFileName):
        print "Loading from",mapFileName
        try:
            self.mapFile = os.path.join('Assets','Maps',mapFileName)
            mapHandle = open(self.mapFile,'r')
            self.clearTiles()
            mapTiles = mapHandle.read().rsplit(',')
            for tile in mapTiles:
                self.tiles.append(Tile(0,0,tile=="x"))
            self.rearrangeTiles()
            mapHandle.close()
        except IOError:
            print "No such map."
            
    def draw(self):
        self.screen.blit(self.background,(0,0))
        for tile in self.tiles:
            if tile.blocking:
                self.screen.blit(self.blockingTile,tile.rect)
            else:
                self.screen.blit(self.normalTile,tile.rect)
        pygame.display.flip()
        
    def dump(self):
        print self.prepareTiles()
        
    def clear(self):
        for tile in self.tiles:
            tile.blocking = False
        
    def prepareTiles(self):
        output = ""
        for tile in self.tiles:
            if tile.blocking:
                output+="x,"
            else:
                output+="1,"
        return output
        
    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygl.QUIT:
                self.running = False
            elif event.type == pygl.KEYDOWN:
                if event.key == pygl.K_q or event.key == pygl.K_ESCAPE:
                    self.running = False
                elif event.key == pygl.K_s:
                    self.save()                
                elif event.key == pygl.K_d:
                    self.dump()
                elif event.key == pygl.K_c:
                    self.clear()
            elif event.type == pygl.MOUSEMOTION and event.buttons[0] == 1:
                for tile in self.tiles:
                    if(tile.rect.collidepoint(pygame.mouse.get_pos())):
                        tile.blocking = (not self.startTileBlocking)
                        
            elif event.type == pygl.MOUSEBUTTONDOWN and event.button == 1:
                for tile in self.tiles:
                    if(tile.rect.collidepoint(pygame.mouse.get_pos())):
                        self.startTileBlocking = tile.blocking

                
    def save(self):
        print "Saving..."
        try:
            mapHandle = open(self.mapFile,'w')
            mapHandle.write(self.prepareTiles())
            mapHandle.close()
            print "Map saved."
        except IOError:
            print "Save failed. Outputing map to console."
            self.dump()

class Tile:
    def __init__(self,left,top,blocking=False):
        self.rect = pygame.Rect(left,top,16,16)
        self.blocking = blocking
        
    def toggle(self):
        if self.blocking:
            self.blocking = False
        else:
            self.blocking = True

Editor = Editor(sys.argv)