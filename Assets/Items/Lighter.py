# -*- coding: utf-8 -*-
from Libraries.Elements import Item

class Lighter(Item):
    def __init__(self,game):
        Item.__init__(self,game)
        self.Game = game
        self.setName("lighter")
        self.setTitle("Lighter")
        self.setImage("ITEM_0004")