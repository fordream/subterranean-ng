# -*- coding: utf-8 -*-
import os,pygame

class Cursor:
    def __init__(self,game):
        self.Game = game
        self.currentElement = None;
        self.currentItem = None
        self.cursorName = None
        self.currentCursor = None
        self.actionStartPos = (0,0)
        self.actionMenuImages = {
            'DEFAULT':self.Game.get('ACTIONMENU_DEFAULT'),
            'USE':self.Game.get('ACTIONMENU_USE'),        
            'PICKUP':self.Game.get('ACTIONMENU_PICKUP'),
            'LOOK':self.Game.get('ACTIONMENU_LOOK'),
            'TALK':self.Game.get('ACTIONMENU_TALK')
        }
        
        self.actionMenuImage = 'DEFAULT'
        self.actionMenuVisible = False
        self.actionElement = None
        

        self.cursors = {
            'DEFAULT': pygame.image.load(os.path.join('Resources','Cursors','cursor_default.png')).convert_alpha(),
            'USE': pygame.image.load(os.path.join('Resources','Cursors','cursor_use.png')).convert_alpha(),
        }
        
        #Keep these here so we don't loop over it while scrolling.
        self.pausedCursor = pygame.image.load(os.path.join('Resources','Cursors','cursor_paused.png'))
        self.exitCursors = {
            'EXIT_NORTH': pygame.image.load(os.path.join('Resources','Cursors','cursor_exit_north.png')).convert_alpha(),
            'EXIT_EAST': pygame.image.load(os.path.join('Resources','Cursors','cursor_exit_east.png')).convert_alpha(),
            'EXIT_SOUTH': pygame.image.load(os.path.join('Resources','Cursors','cursor_exit_south.png')).convert_alpha(),
            'EXIT_WEST': pygame.image.load(os.path.join('Resources','Cursors','cursor_exit_west.png')).convert_alpha()

        }
        self.setCursor('DEFAULT')
     
    def setCursor(self,cursorName):
        #TODO: Make this prettier 
        if cursorName in self.cursors:
            self.cursorName = cursorName
            self.currentCursor = self.cursors[cursorName]
        elif cursorName in self.exitCursors:
            self.cursorName = cursorName
            self.currentCursor = self.exitCursors[cursorName]
            
    def getCursor(self):
        if self.Game.paused:
            return self.pausedCursor
        elif self.Game.Inventory.currentItem is not None:
            return self.Game.Inventory.currentItem.image
        else:
            return self.currentCursor
            
    def getCursorName(self):
        return self.cursorName
        
    def nextCursor(self):
        keys = self.cursors.keys()
        cursorIndex = keys.index(self.cursorName)
        if cursorIndex < len(self.cursors)-1:
            self.setCursor(keys[cursorIndex + 1])
        else:
            self.setCursor("USE")

    def previousCursor(self):
        keys = self.cursors.keys()
        cursorIndex = keys.index(self.cursorName)
        if cursorIndex >  1:
            self.setCursor(keys[cursorIndex - 1])
        else:
            self.setCursor(keys[-1])
                                
    def scrollCursor(self,direction):
        if direction == 4:
            self.setCursor(self.nextCursor())
        else:
            self.setCursor(self.previousCursor())
            
    def findCurrentItem(self,pos):
        for item in self.Game.Inventory.items:
            if(item.rect.collidepoint(pos)):
                if self.Game.Inventory.currentItem is not None and item.current is False:
                    self.Game.TitleManager.setElement(item)
                    self.Game.TitleManager.setPrefix('COMBINE')
                    self.Game.TitleManager.setSuffix('WITH')
                    self.currentItem = item
                elif(item.rect.collidepoint(pos)):
                    self.Game.TitleManager.setElement(item)
                    self.setCursor('USE')
                    self.currentItem = item
                    return True
        return False
                    
    def findCurrentTopic(self,pos):
        self.Game.TopicMenu.clearCurrentTopic()
        for topic in self.Game.TopicMenu.topics:
            if(topic.rect.collidepoint(pos)):
                self.Game.TopicMenu.setCurrentTopic(topic)
                return True
        return False
                
    def findCurrentWidget(self,pos):
        for widget in self.Game.currentWindow.widgets:
            if(widget.rect.collidepoint(pos)):
                self.Game.TitleManager.setElement(widget)
                self.currentElement = widget
                self.setCursor('USE')
                return True
        return False
                
    def findCurrentElement(self,pos):
        if self.Game.Cursor.currentItem is not None:
            mouse = pos
            pos = (mouse[0]+24,mouse[1]+24)
        for element in self.Game.currentScene.visibleElements:
            if(element.rect.collidepoint(pos)):
                self.Game.TitleManager.setElement(element)
                self.currentElement = element
                if self.Game.Inventory.currentItem:
                    self.Game.TitleManager.setPrefix('GIVE')
                    self.Game.TitleManager.setSuffix('TO')
                if self.getCursorName() == 'DEFAULT':
                    self.setCursor('USE')
                    return True;
        return False
                
    def findCurrentExit(self,pos):
        for exit in self.Game.currentScene.exits:
            if(exit.rect.collidepoint(pos)):
                self.setCursor('EXIT_'+exit.direction)
                self.currentExit = exit
            
    def checkCollisions(self):
        #TODO:NEEDS MASSIVE CLEANING UP
        if self.Game.currentScene and not self.actionMenuVisible:
            #translatedPos = self.Game.Renderer.translatePos(pygame.mouse.get_pos())
            pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pos()[1] < 80:
                if self.findCurrentItem(pos):
                    return
            elif pygame.mouse.get_pos()[1] > 660 and self.Game.TopicMenu.visible:
                if self.findCurrentTopic(pos):
                    return
            elif pygame.mouse.get_pos()[1] < 660 and self.Game.TopicMenu.visible:
                self.Game.TopicMenu.clearCurrentTopic()
            else:
                if self.Game.currentWindow is not None:
                    self.findCurrentWidget(pos)
                else:
                    #Last resorts, are there any exits here?
                    if self.findCurrentElement(pos):
                        return
                    elif self.findCurrentExit(pos):
                        return
                    
            self.Game.TitleManager.clearElement()
            self.setCursor('DEFAULT')
            self.currentElement = None;
            self.currentExit = None
    
    def showActionMenu(self):
        self.actionMenuVisible = True
        self.actionElement = self.currentElement
        self.actionStartPos = pygame.mouse.get_pos()
        
    def hideActionMenu(self):
        self.actionMenuVisible = False
        self.actionElement = None
        self.actionStartPos = (0,0)
        
    def updateActionMenu(self):
        self.Game.TitleManager.setPrefix(self.Game.EventManager.checkGesture())
        self.actionMenuImage = self.actionMenuImages.get(self.Game.EventManager.checkGesture())