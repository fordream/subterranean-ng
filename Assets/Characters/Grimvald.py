# -*- coding: utf-8 -*-
from Elements import Character

class Grimvald(Character):
    def __init__(self,game):
        Character.__init__(self)
        self.Game = game
        self.setName("grimvald")
        self.setTitle("Blacksmith")
        self.addSequence('default',[
            (self.Game.get('GRIMVALD_STAND_1'),25),
            (self.Game.get('GRIMVALD_STAND_2'),4),
            ])

        self.addSequence('talk',[
            (self.Game.get('GRIMVALD_TALK_1'),2),
            (self.Game.get('GRIMVALD_TALK_2'),4),
            (self.Game.get('GRIMVALD_TALK_3'),3),
            (self.Game.get('GRIMVALD_TALK_4'),4),
            (self.Game.get('GRIMVALD_TALK_5'),5),
            ])

        self.addSequence('silly',[
            (self.Game.get('GRIMVALD_SILLY_1'),2),
            (self.Game.get('GRIMVALD_SILLY_2'),4),
            (self.Game.get('GRIMVALD_SILLY_3'),14),
            (self.Game.get('GRIMVALD_SILLY_2'),3),
            (self.Game.get('GRIMVALD_SILLY_1'),2),
            ])

        self.setPosition((634,306))
        self.setActionPosition((604,486))
        self.setTextColor((255,128,0))        
        
        self.addTopic("what","Whar are you doing?",self.talkWhat)
        self.addTopic("where","Where are we?",self.talkWhere)
        self.setTalkMethod(self.startTalk)
        
        self.setUseMethod(self.onUse)
        self.setLookMethod(self.onLook)
        self.setPickupMethod(self.onPickup)
        
        self.knowName = False

    def talkWhat(self):
        self.Game.Player.scriptSay("What are you doing?")
        self.scriptSay("I'm working on a mushroom blade for Torvild.")
        self.addTopic("torvild","Who is Torvild?",self.talkTorvild)
        self.addTopic("mushroomblade","What's a mushroom blade?",self.talkBlade)
        
    def talkBlade(self):
        self.Game.Player.scriptSay("What's a mushroom blade?")
        self.scriptSay("Were you born yesterday? It is a tool for harvesting mushrooms of course!")

    def talkTorvild(self):
        self.Game.Player.scriptSay("Who's Torvild?")
        self.scriptSay("He's the mushroom harvester. About your age.")

    def talkWhere(self):
        self.Game.Player.scriptSay("Where are we?")
        self.scriptSay("Well to be exact, you are standing in my smith here in Undergård.")
        if not self.hasTopic("undergard"):
            self.addTopic("undergard","What is Undergård?",self.talkUndergard)

    def talkUndergard(self):
        self.Game.Player.scriptSay("What is Undergård?")
        self.scriptSay("By Thor's ox, This is the first and foremost city we have!")
        self.scriptSay("The most part of our population live here and the Elderbeards have their chambers here.")
        self.scriptSay("Don't you remember this?")
        self.Game.Player.scriptSay("Um, of course I did. I was only checking if you did.")

    def startTalk(self):
        self.Game.Player.scriptSay("Hi there!")
        self.scriptSay("I haven't seen you before. Who are you?")
        self.Game.Player.scriptSay("I'm Nils.")
        self.scriptSay("Nils. That's a peculiar name.")
        self.scriptSay("I'm Grimvald. The smith of Undergård.")
        self.setTitle("Grimvald")
        self.knowName = True
        if not self.hasTopic("undergard"):
            self.addTopic("undergard","What is Undergård?",self.talkUndergard)
        
    def onLook(self):
        if self.knowName:
            self.Game.Player.scriptSay("It's Grimvald, the blacksmith.")
        else:
            self.Game.Player.scriptSay("It's a blacksmith.")
    
    def onUse(self):
        self.scriptSay("This is not Facebook")
        self.scriptSequence("silly")

    def onPickup(self):
        self.scriptSay("Are you hitting on me, lad?")