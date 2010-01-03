# -*- coding: utf-8 -*-
from Elements import Character

class Grimvald(Character):
    def __init__(self,game):
        Character.__init__(self)
        self.Game = game
        self.setName("grimvald")
        self.setTitle("Smith")
        self.setImage("grimvald.png")
        self.addSequence('default',[
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',
            'grimvald-stand-1.png',                        
            'grimvald-stand-2.png',
            'grimvald-stand-2.png',
            'grimvald-stand-2.png',
            'grimvald-stand-2.png',
            ])

        self.addSequence('talk',[
            'grimvald-talk-1.png',
            'grimvald-talk-2.png',
            'grimvald-talk-3.png',
            'grimvald-talk-4.png',
            'grimvald-talk-5.png'
            ])

        self.setPosition((634,306))
        self.setActionPosition((604,486))
        self.setTextColor((255,128,0))        
        
        self.addTopic("who","Who are you?",self.talkWho)
        self.addTopic("what","Whar are you doing?",self.talkWhat)
        self.addTopic("where","Where are we?",self.talkWhere)
        self.setTalkMethod(self.startTalk)

    def talkWho(self):
        self.Game.Player.scriptSay("Who are you?")
        self.scriptSay("The name's Grimvald. The smith of Undergård. Who are you, youngster?")
        self.setTitle("Grimvald")
        if not self.hasTopic("undergard"):
            self.addTopic("undergard","What is Undergård?",self.talkUndergard)
        self.Game.Player.scriptSay("I'm Nils.")
        self.scriptSay("Nils. What a peculiar name.")

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
        self.scriptSay("What do you want?")