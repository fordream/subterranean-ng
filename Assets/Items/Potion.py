# -*- coding: utf-8 -*-
from Libraries.Elements import Item

class Potion(Item):
    def __init__(self,game):
        Item.__init__(self,game)
        self.Game = game
        self.setName("potion")
        self.setTitle("Potion")
        self.setImage("ITEM_0001")
        self.addCombination("chili",'Firepotion')