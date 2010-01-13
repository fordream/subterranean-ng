# -*- coding: utf-8 -*-
from Libraries.Elements import Item

class Chili(Item):
    def __init__(self,game):
        Item.__init__(self)
        self.Game = game
        self.setName("chili")
        self.setTitle("Chilifrukt")
        self.addCombination("potion",Item("firepotion","Eldig"))