 # -*- coding: utf-8 -*-
import os,pygame
import pygame.locals as pygl
        
class EventManager:
    def __init__(self,game):
        self.Game = game
        self.eventSignals = {pygl.QUIT: self.Game.quit,
                            pygl.KEYDOWN: self.readKey,
                            pygl.MOUSEMOTION: self.readMousePos,
                            pygl.MOUSEBUTTONDOWN: self.handleMouseDown,
                            pygl.MOUSEBUTTONUP: self.handleMouseUp,
                            }
                            
        self.keySignals = {pygl.K_q: self.Game.quit,
                            pygl.K_ESCAPE: self.Game.quit,
                            pygl.K_m: self.Game.AudioController.toggleMusicPause,
                            pygl.K_l: self.Game.AudioController.toggleMusicVolume,
                            pygl.K_d: self.Game.dump,
                            pygl.K_f: self.Game.toggleFullscreen,
                            pygl.K_t: self.Game.Player.testMessage,
                            }
                            
        self.mouseDownSignals = {
                            1: self.handleLeftMouseDown,
                            3: self.handleRightMouseDown,
                            }

        self.mouseUpSignals = {
                            1: self.handleLeftMouseUp,
                            3: self.handleRightMouseUp,
                            }
                            
    def checkEvents(self):
        for event in pygame.event.get():
            eventMethod = self.eventSignals.get(event.type)
            if eventMethod is not None:
                eventMethod(event)
                            
    def readKey(self,event):
        eventMethod = self.keySignals.get(event.key)
        if eventMethod is not None:
            eventMethod()
            
    def readMousePos(self,event):
        if not self.Game.paused:
            if event.pos[1] < 50 and self.Game.Inventory.visible is False:
                self.Game.Inventory.show()
            elif event.pos[1] > 50 and self.Game.Inventory.visible:
                self.Game.Inventory.hide()
        else:
            #Hide the inventory if the game is paused.
            self.Game.Inventory.hide()
            
    def handleMouseDown(self,event):
        eventMethod = self.mouseDownSignals.get(event.button)
        if eventMethod is not None:
            eventMethod(event)

    def handleMouseUp(self,event):
        eventMethod = self.mouseUpSignals.get(event.button)
        if eventMethod is not None:
            eventMethod(event)

        
    def handleLeftMouseDown(self,event):    
        #If the game is not paused
        if self.Game.currentScene and not self.Game.paused:    
            #If we are inside inventory
            if pygame.mouse.get_pos()[1] < 70:
                #If we are hovering over an item and anen't holding any item
                if self.Game.Cursor.currentItem is not None and self.Game.Inventory.currentItem is None:
                    self.Game.Inventory.setCurrentItem(self.Game.Cursor.currentItem)
                #If we are hovering over an item and are holding an item
                elif self.Game.Cursor.currentItem is not None and self.Game.Inventory.currentItem is not None and self.Game.Cursor.currentItem.current is False:
                    self.Game.Cursor.currentItem.combine(self.Game.Inventory.currentItem)
                #If we aren't hovering over any item and clicking (with item in hand or not)
                else:
                    self.Game.Inventory.clearCurrentItem()
            #If we are anywhere else on screen
            else:
                #If the mouse hovers a topic, activate it.
                if self.Game.TopicMenu.currentTopic:
                    self.Game.TopicMenu.currentTopic.callbackMethod()
                #If we have a window open and are hovering over any widget
                elif self.Game.currentWindow and self.Game.Cursor.currentElement.clickMethod: 
                    self.Game.Cursor.currentElement.clickMethod()
                #If we hare hovering over something and have an item in hand, give it            
                elif self.Game.Cursor.currentItem and self.Game.Cursor.currentElement:
                    pos = self.Game.Cursor.currentElement.getActionPosition()
                    if pos is None:
                        pos = self.Game.Cursor.currentElement.getBasePosition()
                    self.Game.Player.walkTo(pos,self.Game.Player.give,self.Game.Cursor.currentElement)
                #If we are hovering over an exit, go there
                elif self.Game.Cursor.currentExit and self.Game.Cursor.currentItem is None:
                    self.Game.Player.walkTo(self.Game.Cursor.currentExit.exitPoint,self.Game.Player.exit,self.Game.Cursor.currentExit)
                #If nothing else, just walk to the postion
                else:
                    self.Game.Player.walkTo(pygame.mouse.get_pos())    
        #If the game is paused (sequence), skip it                        
        elif self.Game.ScriptManager.durationFrames > 0 and self.Game.ScriptManager.currentPartType == 'ScriptConversationPart':
            self.Game.ScriptManager.skip()

    def handleRightMouseDown(self,event):
        #If the game is not paused
        if self.Game.currentScene and not self.Game.paused:    
            self.mouseHold = True
            #If there is an item in your hand, return it to inventory
            if self.Game.Inventory.getCurrentItem():
                self.Game.Inventory.clearCurrentItem()
            #If there is a window open, hide it
            elif self.Game.currentWindow:
                self.Game.currentWindow.hide()
            #If we have no item in hand, show ActionMenu
            elif self.Game.Cursor.currentElement and self.Game.Cursor.currentItem is None and self.Game.currentWindow is None:
                self.Game.Cursor.showActionMenu()

    def handleLeftMouseUp(self,event):
        pass

    def handleRightMouseUp(self,event):
        if self.Game.Cursor.actionMenuVisible and self.Game.Cursor.actionElement is not None:
            self.mouseHold = False
            gesture = self.checkGesture()        
            pos = self.Game.Cursor.actionElement.getActionPosition()
            if pos is None:
                pos = self.Game.Cursor.actionElement.getBasePosition()
            if gesture == 'PICKUP':
                self.Game.Player.walkTo(pos,self.Game.Player.pickUp,self.Game.Cursor.actionElement)
            elif gesture == 'USE':
                self.Game.Player.walkTo(pos,self.Game.Player.use,self.Game.Cursor.actionElement)
            elif gesture == 'TALK':
                self.Game.Player.walkTo(pos,self.Game.Player.talk,self.Game.Cursor.actionElement)
            elif gesture == 'LOOK':
                self.Game.Player.look(self.Game.Cursor.actionElement)
            self.Game.Cursor.hideActionMenu()
            
    def checkGesture(self):
        sx,sy = self.Game.Cursor.actionStartPos
        cx,cy = pygame.mouse.get_pos()

        if cx > sx and cy < sy:
            return "TALK"
        elif cx > sx and cy > sy:
            return "USE"
        elif cx < sx and cy < sy:
            return "LOOK"
        elif cx < sx and cy > sy:
            return "PICKUP"
        else:
            return "DEFAULT"
                        
    def handleScrollClick(self,event):
        pass
    
    def handleScrollUp(self,event):
        pass
    
    def handleScrollDown(self,event):
        pass
