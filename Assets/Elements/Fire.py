# -*- coding: utf-8 -*-
from Libraries.Elements import AnimatedElement

class Fire(AnimatedElement):
    def __init__(self,game):
        AnimatedElement.__init__(self)
        self.Game = game
        self.setName("fire")
        self.setTitle('Fire')
        self.addSequence('default',[
            self.Game.get('FIRE_DEFAULT_1'),
            self.Game.get('FIRE_DEFAULT_2'),
            self.Game.get('FIRE_DEFAULT_3'),
            self.Game.get('FIRE_DEFAULT_4'),
            self.Game.get('FIRE_DEFAULT_3'),
            self.Game.get('FIRE_DEFAULT_2'),
            self.Game.get('FIRE_DEFAULT_1')
            ])
        self.setPosition((540,276))
        self.setActionPosition((434,446))
        self.setLookMethod(self.fireLook)
        self.setUseMethod(self.fireUse)
        
    def fireLook(self):
        self.Game.Player.scriptSay("Mmm... varmt","PLAYER003")

    def fireUse(self):
        self.Game.Player.scriptSay("Aj!")