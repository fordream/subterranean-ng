 # -*- coding: utf-8 -*-
import os,pygame
import pygame.locals as pygl
        
class EventManager:
    def __init__(self,game):
        self.Game = game
        self.eventSignals = {pygl.QUIT: self.Game.quit,
                            pygl.KEYDOWN: self.readKey,
                            pygl.MOUSEBUTTONDOWN: self.readMouseClick,
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
                            pygl.K_t: self.Game.Player.randomTalk,
                           #pygl.K_s: self.Game.toggleCapture
                            }
                            
        self.mouseSignals = {1: self.handleLeftClick,
                            2: self.handleScrollClick,
                            3: self.handleRightClick,
                            4: self.handleScrollDown,
                            5: self.handleScrollUp
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
        
    def readMouseClick(self,event):
        eventMethod = self.mouseSignals.get(event.button)
        if eventMethod is not None:
            eventMethod(event)
            
    def handleMouseDown(self,event):
        self.mouseHold = True
        if self.Game.Cursor.currentElement is not None and self.Game.Cursor.currentItem is None:
            self.Game.Cursor.showActionMenu()
        else:
            self.handleLeftClick(event)
                       
    def handleMouseUp(self,event):
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
            
    def handleLeftClick(self,event):
        #not used atm, sry
        if not self.Game.paused:    
            if pygame.mouse.get_pos()[1] < 70:
                if self.Game.Cursor.currentItem is not None and self.Game.Inventory.currentItem is None:
                    self.Game.Inventory.setCurrentItem(self.Game.Cursor.currentItem)
                elif self.Game.Cursor.currentItem is not None and self.Game.Inventory.currentItem is not None and self.Game.Cursor.currentItem.current is False:
                    self.Game.Cursor.currentItem.combine(self.Game.Inventory.currentItem)
                else:
                    self.Game.Inventory.clearCurrentItem()
            else:
                if self.Game.TopicMenu.currentTopic:
                    self.Game.TopicMenu.currentTopic.callbackMethod()
                #REMOVE FALSE OMG
                elif False and self.Game.Cursor.currentElement is not None:
                    pos = self.Game.Cursor.currentElement.getActionPosition()
                    if pos is None:
                        pos = self.Game.Cursor.currentElement.getBasePosition()
                    if self.Game.currentWindow is not None and self.Game.Cursor.currentElement.clickMethod is not None: 
                        self.Game.Cursor.currentElement.clickMethod()
                    elif self.Game.Cursor.currentItem is not None and self.Game.Cursor.currentElement is not None:
                        self.Game.Player.walkTo(pos,self.Game.Player.give,self.Game.Cursor.currentElement)
                    elif self.Game.Cursor.getCursorName() == 'PICKUP':
                        self.Game.Player.walkTo(pos,self.Game.Player.pickUp,self.Game.Cursor.currentElement)
                    elif self.Game.Cursor.getCursorName() == 'USE':
                        self.Game.Player.walkTo(pos,self.Game.Player.use,self.Game.Cursor.currentElement)
                    elif self.Game.Cursor.getCursorName() == 'TALK':
                        self.Game.Player.walkTo(pos,self.Game.Player.talk,self.Game.Cursor.currentElement)
                    elif self.Game.Cursor.getCursorName() == 'LOOK':
                        self.Game.Player.look(self.Game.Cursor.currentElement)
                elif self.Game.Cursor.currentExit is not None:
                    self.Game.Player.walkTo(self.Game.Cursor.currentExit.exitPoint,self.Game.Player.exit,self.Game.Cursor.currentExit)
                else:
                    self.Game.Player.walkTo(pygame.mouse.get_pos())
        else:
            if self.Game.ScriptManager.durationFrames > 0 and self.Game.ScriptManager.currentPartType == 'ScriptConversationPart':
                self.Game.ScriptManager.skip()

    
    def handleRightClick(self,event):
        #Right click cancels.
        if not self.Game.paused and self.Game.Inventory.getCurrentItem() is not None:
                self.Game.Inventory.clearCurrentItem()
        elif self.Game.currentWindow is not None:
            self.Game.currentWindow.hide()
        elif self.Game.currentWindow is not None:
            self.Game.currentWindow.hide()
        
    def handleScrollClick(self,event):
        pass
    
    def handleScrollUp(self,event):
        if self.Game.Cursor.currentElement is not None:
            self.Game.Cursor.scrollCursor(event.button)
    
    def handleScrollDown(self,event):
        if self.Game.Cursor.currentElement is not None:
            self.Game.Cursor.scrollCursor(event.button)
