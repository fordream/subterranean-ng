# -*- coding: utf-8 -*-
import os,pygame
from Timer import Timer

class Renderer:
    def __init__(self,game):
        self.Game = game
        self.screen = pygame.Surface((1024,768))
        self.scene = pygame.Surface((1024,768))
        self.sceneRect = self.scene.get_rect()
        
        self.rect = self.screen.get_rect()
        self.camera = pygame.Rect((0,0),(1024,768))

        self.setupScreen(False)
        self.loadIcon()
        self.loadFonts()
        self.loadGraphics()
        self.setupTimer()
        self.frame = 0
        
        self.fadeMode = None
        self.fadeCallback = None
        self.fadeCallbackArgument = None
        
    def translate(self,x):
        x = (self.camera.centerx-self.Game.Player.rect.centerx)
        return x
        
    def translatePos(self,pos):
        return (self.translate(pos[0]),pos[1])
        
    def transitionFade(self):
        pass
        
    def handleOverlay(self):
        if self.fadeMode == 'fadeOut':
            if self.overlay.get_alpha() < 255:
                self.overlay.set_alpha(self.overlay.get_alpha()+25)
            else:
                self.resetFade()
                
        elif self.fadeMode == 'fadeIn':
            if self.overlay.get_alpha() > 0:
                self.overlay.set_alpha(self.overlay.get_alpha()-25)
            else:
                self.resetFade()

    def resetFade(self):
        self.fadeMode = None
        if self.fadeCallback:
            self.fadeCallback(self.fadeCallbackArgument)
        self.fadeCallback = None
        self.fadeCallbackArgument = None
    
    def fadeIn(self,fadeCallback=None,fadeCallbackArgument=None):
        self.fadeCallback = fadeCallback
        self.fadeCallbackArgument = fadeCallbackArgument
        self.fadeMode = 'fadeIn'
        self.overlay.set_alpha(255)
                    
    def fadeOut(self,fadeCallback=None,fadeCallbackArgument=None):
        self.fadeCallback = fadeCallback
        self.fadeCallbackArgument = fadeCallbackArgument
        self.fadeMode = 'fadeOut'
        self.overlay.set_alpha(0)

    def setupTimer(self):
        self.Timer = Timer()
        self.Timer.setFPS(24)
        
    def setupScreen(self,fullscreen=False):
        #There seems to be no way to make this work right other than doing this:
        if fullscreen:
            self.window = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
            self.rect.center = self.window.get_rect().center 
        else:
            self.window = pygame.display.set_mode((1024,768))
            self.rect.center = self.window.get_rect().center 
        pygame.display.set_caption('Subterranean')
        
    def loadGraphics(self):
        #self.backgroundImage = pygame.image.load(os.path.join('data','backgrounds','game.png'))
        self.borderImage = pygame.image.load(os.path.join('data','ui','border.png'))
        self.inventoryImage = pygame.image.load(os.path.join('data','ui','inventory.png'))
        self.topicMenuImage = pygame.image.load(os.path.join('data','ui','topicmenu.png'))
        self.debugPoint = pygame.Surface((2,2))
        self.debugPoint.fill((255,0,0))
        self.overlay = pygame.Surface((1024,768))
        self.overlay.fill((0,0,0))
        self.overlay.set_alpha(0)

    def loadFonts(self):
        pygame.font.init()
        self.defaultFontColor = (255,255,255)
        self.defaultTitleColor = (239,240,173)
        self.defaultOutlineFontColor = (0,0,0)
        self.generalFont = pygame.font.Font(os.path.join('data','fonts','HVD_Edding.otf'),26)
        self.topicMenuFont = pygame.font.Font(os.path.join('data','fonts','HVD_Edding.otf'),24)
        self.elementTitleFont = pygame.font.Font(os.path.join('data','fonts','HVD_Edding.otf'),26)

    def loadIcon(self):
        pygame.display.set_icon(pygame.image.load(os.path.join('data','icons','gameicon.png')))
        
    def draw(self):
        pygame.mouse.set_visible(0)
        #Draw game screen
        #Put this somewhere else?
        #self.sceneRect.left = self.translate(self.sceneRect.left)
            
        self.window.blit(self.screen,self.rect)
        self.screen.blit(self.scene,self.sceneRect)
        
        if self.Game.currentScene.visible:
            #Draw current background
            self.scene.blit(self.Game.currentScene.getBackground(),(0,0))
            
            #Draw room objects
            self.Game.currentScene.visibleElements.update()
            self.Game.currentScene.visibleElements.draw(self.scene)
        
            #Draw main character
            self.scene.blit(self.Game.Player.getCurrentFrame(),self.Game.Player.getRenderPos())
            
            #Draw current foreground
            if self.Game.currentScene.getForeground():
                self.scene.blit(self.Game.currentScene.getForeground(),(0,0))
            
        #Draw border
        #self.screen.blit(self.borderImage,(0,0))
            
        #Draw inventory
        self.Game.Inventory.animateHeight()
        self.screen.blit(self.inventoryImage,(0,self.Game.Inventory.y))
        for item in self.Game.Inventory.items:
            if item.current is False:
                self.screen.blit(item.image,item.rect)

        #Topicmenu
        if self.Game.TopicMenu.visible and not self.Game.ScriptManager.isActive():
            self.screen.blit(self.topicMenuImage,self.Game.TopicMenu.rect)
            for topic in self.Game.TopicMenu.topics:
                self.screen.blit(topic.render,topic.pos)
                
        #Window widgets
        if self.Game.currentWindow is not None:
            self.screen.blit(self.Game.currentWindow.background,self.Game.currentWindow.rect)
            for widget in self.Game.currentWindow.widgets:
                self.screen.blit(widget.image,widget.rect)
                
        #Draw element titles
        if self.Game.TitleManager.currentElement is not None and not self.Game.TopicMenu.visible:
            elementTitle = self.elementTitleFont.render(self.Game.TitleManager.getTitle(),1,self.defaultTitleColor)
            self.screen.blit(elementTitle,(self.screen.get_rect().centerx-elementTitle.get_width()/2,710))           
                        
        #Draw dialouge
        if self.Game.ScriptManager.isActive():
            #Load all the script values from the current part
            if not self.Game.ScriptManager.valuesLoaded:
                self.Game.ScriptManager.loadScriptValues(self.Game.ScriptManager.script[0])
            if self.Game.ScriptManager.getCurrentPartType() == 'ScriptConversationPart':
            
                if self.Game.currentWindow is not None:
                    #If we have HUD open, put all dialouge on top of screen
                    posX = 512
                    posY = 50
                else:
                    posX = self.Game.ScriptManager.getTextPos()[0]
                    posY = self.Game.ScriptManager.getTextPos()[1]

                words = self.Game.ScriptManager.getText().split(' ')
                lines = []
                    
                while len(words):
                    currentLine = ""
                    for word in words[0:7]:
                        currentLine += " "+word
                    lines.append(currentLine)
                    del words[0:7]
                
                lines.reverse()
                for line in lines:
                    lineRender = self.generalFont.render(line,1,self.Game.ScriptManager.currentColor)
                    lineShadow = self.generalFont.render(line,1,self.defaultOutlineFontColor)
                    lineX = posX-lineRender.get_width()/2
                    #Handling for text that goes outside the screen
                    if lineX+lineRender.get_width() > 1000:
                        lineX -= (lineX+lineRender.get_width())-1000
                    self.screen.blit(lineShadow,(lineX,posY-2))
                    self.screen.blit(lineShadow,(lineX+2,posY))
                    self.screen.blit(lineShadow,(lineX-2,posY))
                    self.screen.blit(lineShadow,(lineX,posY+2))
                    self.screen.blit(lineRender,(lineX,posY))
                    posY -= 30                
                
            elif self.Game.ScriptManager.getCurrentPartType() == 'ScriptWalkPart':
                self.Game.ScriptManager.runScriptedWalk()
            self.Game.ScriptManager.loop()            

        #Draw mouse cursor
        self.Game.Cursor.checkCollisions()
        self.screen.blit(self.Game.Cursor.getCursor(),pygame.mouse.get_pos())

        #Draw overlay
        self.handleOverlay()
        self.window.blit(self.overlay,self.rect)
            
        #Debug points
        if self.Game.debug:
            if len(self.Game.Player.path) > 1:
                pygame.draw.lines(self.screen, (255,255,255,255), 0, self.Game.Player.path)
            for element in self.Game.currentScene.visibleElements:
                pygame.draw.lines(self.scene,(255,0,255),1,[element.rect.topleft,element.rect.topright,element.rect.bottomright,element.rect.bottomleft])
                if element.actionPos is not None:
                    self.scene.blit(self.debugPoint,element.actionPos)
            self.screen.blit(self.debugPoint,pygame.mouse.get_pos())
            pygame.draw.lines(self.screen,(000,255,255),1,[self.Game.Player.rect.topleft,self.Game.Player.rect.topright,self.Game.Player.rect.bottomright,self.Game.Player.rect.bottomleft])
            for exit in self.Game.currentScene.exits:
                pygame.draw.lines(self.screen,(000,255,255),1,[exit.rect.topleft,exit.rect.topright,exit.rect.bottomright,exit.rect.bottomleft])
                self.scene.blit(self.debugPoint,exit.exitPoint)
            pygame.draw.lines(self.scene,(255,100,255),0,[(0,self.Game.currentScene.farthestPoint),(1024,self.Game.currentScene.farthestPoint)])
            pygame.draw.lines(self.scene,(255,110,24),0,[(0,self.Game.currentScene.closestPoint),(1024,self.Game.currentScene.closestPoint)])

        pygame.display.flip()
