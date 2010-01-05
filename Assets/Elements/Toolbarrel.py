# -*- coding: utf-8 -*-
from Elements import VisibleElement

class Toolbarrel(VisibleElement):
    def __init__(self,game):
        VisibleElement.__init__(self)
        self.Game = game
        self.setName("toolbarrel")
        self.setTitle('Barrel of tools')
        self.setImage('toolbarrel.png')
        self.setPosition((750,346))
        self.setActionPosition((644,486))
        self.setLookMethod(self.look)
        self.setUseMethod(self.use)
        self.setPickupMethod(self.pickup)
        
    def look(self):
        self.Game.Player.scriptSay("It's a barrel of tools")
        
    def pickup(self):
        self.use()

    def use(self):
        self.Game.Player.scriptSay("I'd best not take any of those tools")