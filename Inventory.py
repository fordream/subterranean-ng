# -*- coding: utf-8 -*-
import os,pygame
from Elements import Item

class Inventory:
    def __init__(self,game):
        self.Game = game
        self.currentItem = None
        self.items = []
        self.visible = False
        self.surface = pygame.Surface((1024,68))
        self.rect = self.surface.get_rect()
        self.surface.fill((25,25,25),self.rect)
        self.surface.set_alpha(145)
        self.animating = False
        self.y = -80
        self.spacing = 20

    def addItem(self,item,runEffect=True):
        #Need game reference to talk to Inventory later
        item.Game = self.Game
        self.items.append(item)
        if not self.visible:
            self.hideItems()
        self.arrangeItems()
        
    def removeItem(self,item):
        self.items.remove(item)

    def removeItemFromName(self,itemName):
        self.items.remove(self.getItemFromName(itemName))

    def getItemFromName(self,name):
        for item in self.items:
            if item.name == name:
                return item
        return False

    def itemExists(self,name):
        for item in self.items:
            if item.name == name:
                return True
        return False

    def combineItems(self,firstElement,secondElement,resultElement):
        self.clearCurrentItem()
        self.removeItem(firstElement)
        self.removeItem(secondElement)
        self.addItem(resultElement,False)
                
    def arrangeItems(self):
        number = 0
        for item in self.items:
            if item.current is False:
                item.setX(number*60+self.spacing)
                number += 1
            else:
                item.setX(-100)
                                                
    def show(self):
        if not self.visible:
            self.visible = True
            self.animating = True
            self.Game.AudioController.playUISound('SLIDEIN')

    def hide(self):
        if self.visible:
            self.visible = False
            self.animating = True
            self.Game.AudioController.playUISound('SLIDEOUT')

    def hideItems(self):
        for item in self.items:
            item.setY(-80)
            
    def setCurrentItem(self,item):
        if self.currentItem is None:
            self.currentItem = item
            self.currentItem.current = True
            self.arrangeItems()
            
    def getCurrentItem(self):
        return self.currentItem
        
    def clearCurrentItem(self):
        self.Game.TitleManager.clearElement()
        self.Game.Cursor.currentItem = None
        self.currentItem.current = False
        self.currentItem = None
        self.arrangeItems()
                    
    def animateHeight(self):
        if self.animating:
            if self.visible and self.y < 10:
                self.y+=10
                for item in self.items:
                    item.setY(self.y+10)
            elif not self.visible and self.y > -80:
                self.y-=10
                for item in self.items:
                    item.setY(self.y+10)
            else:
                self.animating = False
        
    def toggle(self):
        if self.visible:
            self.hide()
        else:
            self.show()