# -*- coding: utf-8 -*-
import os,pygame


class Cursor:
    def __init__(self,game):
        self.Game = game
        self.currentElement = None;
        self.currentItem = None
        self.cursorName = None
        self.currentCursor = None

        self.cursors = {
            'DEFAULT': pygame.image.load(os.path.join('data','cursors','cursor_default.png')),
            'USE': pygame.image.load(os.path.join('data','cursors','cursor_use.png')),
            'PICKUP': pygame.image.load(os.path.join('data','cursors','cursor_pickup.png')),
            'LOOK': pygame.image.load(os.path.join('data','cursors','cursor_look.png')),
            'TALK': pygame.image.load(os.path.join('data','cursors','cursor_talk.png'))
        }
        
        #Keep these here so we don't loop over it while scrolling.
        self.pausedCursor = pygame.image.load(os.path.join('data','cursors','cursor_paused.png'))
        self.exitCursors = {
            'EXIT_NORTH': pygame.image.load(os.path.join('data','cursors','cursor_exit_north.png')),
            'EXIT_EAST': pygame.image.load(os.path.join('data','cursors','cursor_exit_east.png')),
            'EXIT_SOUTH': pygame.image.load(os.path.join('data','cursors','cursor_exit_south.png')),
            'EXIT_WEST': pygame.image.load(os.path.join('data','cursors','cursor_exit_west.png'))

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
            
    def checkCollisions(self):
        #translatedPos = self.Game.Renderer.translatePos(pygame.mouse.get_pos())
        translatedPos = pygame.mouse.get_pos()
        if pygame.mouse.get_pos()[1] < 80:
                for item in self.Game.Inventory.items:
                    if(item.rect.collidepoint(translatedPos)):
                        if self.Game.Inventory.currentItem is not None and item.current is False:
                            self.Game.TitleManager.setElement(item)
                            self.Game.TitleManager.setPrefix('COMBINE')
                            self.Game.TitleManager.setSuffix('WITH')
                            self.currentItem = item
                            return item
                        elif(item.rect.collidepoint(translatedPos)):
                            self.Game.TitleManager.setElement(item)
                            self.setCursor('USE')
                            self.currentItem = item
                            return item
        elif pygame.mouse.get_pos()[1] > 660 and self.Game.TopicMenu.visible:
            self.Game.TopicMenu.clearCurrentTopic()
            for topic in self.Game.TopicMenu.topics:
                if(topic.rect.collidepoint(translatedPos)):
                    self.Game.TopicMenu.setCurrentTopic(topic)
        elif pygame.mouse.get_pos()[1] < 660 and self.Game.TopicMenu.visible:
            self.Game.TopicMenu.clearCurrentTopic()
        else:
            if self.Game.currentWindow is not None:
                for widget in self.Game.currentWindow.widgets:
                    if(widget.rect.collidepoint(translatedPos)):
                        self.Game.TitleManager.setElement(widget)
                        self.currentElement = widget
                        self.setCursor('USE')
                        return self.currentElement
            else:
                for element in self.Game.currentScene.visibleElements:
                    #Calculate center for item cursor to avoid pixel hunting.
                    #Also set the prefix correctly.
                    #TODO: Make this loop smarter. Really.
                    if self.Game.Cursor.currentItem is not None:
                        mouse = translatedPos
                        pos = (mouse[0]+24,mouse[1]+24)
                    else:
                        pos = translatedPos
                    if(element.rect.collidepoint(pos)):
                        self.Game.TitleManager.setElement(element)
                        self.currentElement = element
                        if self.Game.Inventory.currentItem is not None:
                            self.Game.TitleManager.setPrefix('GIVE')
                            self.Game.TitleManager.setSuffix('TO')
                        else:
                            self.Game.TitleManager.setPrefix(self.getCursorName())
                        if self.getCursorName() == 'DEFAULT':
                            if element.isCharacter:
                                self.setCursor('TALK')
                            else:
                                self.setCursor('USE')
                        return self.currentElement
                
                #Last resorts, are there any exits here?
                for exit in self.Game.currentScene.exits:
                    if(exit.rect.collidepoint(translatedPos)):
                        self.setCursor('EXIT_'+exit.direction)
                        self.currentExit = exit
                        return self.currentExit

        self.Game.TitleManager.clearElement()
        self.setCursor('DEFAULT')
        self.currentElement = None;
        self.currentExit = None