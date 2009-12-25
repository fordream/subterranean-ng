# -*- coding: utf-8 -*-
from Elements import Character

class Grumpley(Character):
    def __init__(self,game):
        Character.__init__(self)
        self.Game = game
        self.setName("grumpley")
        self.setTitle("Ok�nd")
        self.setImage("grumpley.png")
        self.setPosition((634,306))
        self.setActionPosition((604,486))
        self.setTextColor((255,128,0))
        
        self.addTopic("who","Vem �r du?",self.talkWho)
        self.addTopic("where","Var �r vi?",self.talkWhere)
        self.setTalkMethod(self.grumpleyTalk)

    def talkWho(self):
        self.Game.Player.scriptSay("Vem �r du egentligen?")
        self.scriptSay("Grimvald. Smeden i Underg�rd. Vem �r du sj�lv pojkspoling?")
        self.setTitle("Grimvald")
        self.Game.Player.scriptSay("Jag �r... �h, strunt i det.")

    def talkWhere(self):
        self.Game.Player.scriptSay("Var �r vi?")
        self.scriptSay("F�r att vara exakt s� st�r du i min smedja, i Underg�rd.")
        self.addTopic("undergard","Vad �r Underg�rd?",self.talkUndergard)

    def talkUndergard(self):
        self.Game.Player.scriptSay("Vad �r Underg�rd f�r stad?")
        self.scriptSay("Vid Tors oxar, Det �r ju den f�rsta byn vi byggde upp n�r vi f�rst kom ned hit. Gammelsk�ggen har sin borg d�r.")
        self.scriptSay("K�nner du inte till det?")
        self.Game.Player.scriptSay("Det gjorde jag f�rst�s, jag ville bara kolla s� att du ocks� gjorde det.")

    def grumpleyTalk(self):
        self.scriptSay("Hm... Vad vill du?")