# -*- coding: utf-8 -*-
from Elements import Character

class Grumpley(Character):
    def __init__(self,game):
        Character.__init__(self)
        self.Game = game
        self.setName("grumpley")
        self.setTitle("Okänd")
        self.setImage("grumpley.png")
        self.setPosition((634,306))
        self.setActionPosition((604,486))
        self.setTextColor((255,128,0))
        
        self.addTopic("who","Vem är du?",self.talkWho)
        self.addTopic("where","Var är vi?",self.talkWhere)
        self.setTalkMethod(self.grumpleyTalk)

    def talkWho(self):
        self.Game.Player.scriptSay("Vem är du egentligen?")
        self.scriptSay("Grimvald. Smeden i Undergård. Vem är du själv pojkspoling?")
        self.setTitle("Grimvald")
        self.Game.Player.scriptSay("Jag är... äh, strunt i det.")

    def talkWhere(self):
        self.Game.Player.scriptSay("Var är vi?")
        self.scriptSay("För att vara exakt så står du i min smedja, i Undergård.")
        self.addTopic("undergard","Vad är Undergård?",self.talkUndergard)

    def talkUndergard(self):
        self.Game.Player.scriptSay("Vad är Undergård för stad?")
        self.scriptSay("Vid Tors oxar, Det är ju den första byn vi byggde upp när vi först kom ned hit. Gammelskäggen har sin borg där.")
        self.scriptSay("Känner du inte till det?")
        self.Game.Player.scriptSay("Det gjorde jag förstås, jag ville bara kolla så att du också gjorde det.")

    def grumpleyTalk(self):
        self.scriptSay("Hm... Vad vill du?")