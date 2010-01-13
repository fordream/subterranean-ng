# -*- coding: utf-8 -*-
import os,pygame

class ElementWindow:
    def __init__(self,game):
        self.Game = game
        self.background = None
        self.rect = None
        self.widgets = []
        self.openMethod = None
        self.closeMethod = None
        
    def setBackground(self,background):
        self.background = background
        self.rect = self.background.get_rect()
        self.align()
        
    def align(self):
        self.rect.left = (1024-self.rect.w)/2
        self.rect.top = (768-self.rect.h)/2
        
    def show(self):
        self.Game.currentWindow = self
        self.runOpenMethod()
        
    def hide(self):
        self.Game.currentWindow = None
        self.runCloseMethod()

    def addWidget(self,widget):
        widget.setParent(self)
        self.widgets.append(widget)
        
    def setOpenMethod(self,method):
        self.openMethod = method

    def setCloseMethod(self,method):
        self.closeMethod = method

    def runOpenMethod(self):
        if self.openMethod is not None:
            self.openMethod()
            
    def runCloseMethod(self):
        if self.closeMethod is not None:
            self.closeMethod()