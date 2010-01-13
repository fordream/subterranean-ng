# -*- coding: utf-8 -*-
from Libraries.Elements import Item

class Potion(Item):
    def __init__(self,game):
        Item.__init__(self)
        self.Game = game
        self.setName("potion")
        self.setTitle("Kärleksdryck")
        self.addCombination("chili",Item("firepotion","Eldig"))