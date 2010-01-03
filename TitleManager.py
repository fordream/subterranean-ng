# -*- coding: utf-8 -*-
import os,pygame

class TitleManager:
    def __init__(self,game):
        self.Game = game
        self.prefix = ''
        self.suffix = ''
        self.currentElement = None
        self.prefixes = {
            'USE':'Use',    
            'PICKUP':'Pick up',
            'TALK':'Talk to',
            'LOOK':'Look at',
            'GIVE':'Give',
            'COMBINE':'Combine'
        }

        self.suffixes = {
            'WITH':'with',    
            'TO':'to'
        }
        
    def setPrefix(self,prefix=None):
        if prefix in self.prefixes:
            self.prefix = self.prefixes.get(prefix)
        else:
            self.prefix = ''

    def setSuffix(self,suffix=None):
        if suffix in self.suffixes:
            self.suffix = self.suffixes.get(suffix)
        else:
            self.suffix = ''
                    
    def setElement(self,element):
        self.currentElement = element

    def clearElement(self):
        self.currentElement = None
        self.prefix = ''
        
    def getTitle(self):
        if not self.Game.paused and self.currentElement is not None:
            if self.prefix == 'Combine' or self.prefix == 'Give':
                return '%s %s %s %s' % (self.prefix,self.Game.Inventory.currentItem.title,self.suffix,self.currentElement.title)
            else:
                return '%s %s' % (self.prefix,self.currentElement.title)