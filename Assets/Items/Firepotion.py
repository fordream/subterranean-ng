# -*- coding: utf-8 -*-
from Libraries.Elements import Item

class Firepotion(Item):
    def __init__(self,game):
        Item.__init__(self,game)
        self.Game = game
        self.setName("firepotion")
        self.setTitle("Fire potion")
        self.setImage("ITEM_0002")