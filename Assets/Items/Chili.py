# -*- coding: utf-8 -*-
from Libraries.Elements import Item

class Chili(Item):
    def __init__(self,game):
        Item.__init__(self,game)
        self.Game = game
        self.setName("chili")
        self.setTitle("Chili")
        self.setImage("ITEM_0003")
        self.addCombination("potion",'Firepotion')