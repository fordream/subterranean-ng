# -*- coding: utf-8 -*-
from Elements import Character

class Worm(Character):
    def __init__(self,game):
        Character.__init__(self)
        self.Game = game
        self.setName("worm")
        self.setTitle('Mask')
        self.setImage('worm.png')
        self.setPosition((434,446))
        self.setTextColor((255,128,0))
        
        self.addTopic('whatsup','Hur är läget?',self.talkWhatsUp)        
        self.addTopic('sky','Vilken himmel vi har!',self.talkSky)
        
        self.addGiveMethod(self.giveChiliToWorm,'chili')
        self.addGiveMethod(self.givePotionToWorm,'potion')
        self.addGiveMethod(self.giveFirepotionToWorm,'firepotion')
        
        self.setUseMethod(self.wormUse)
        self.setLookMethod(self.wormLook)
        self.setTalkMethod(self.wormTalk)
        self.setPickupMethod(self.wormPickup)

    def talkDrink(self):
        self.Game.Player.scriptSay('Jaså? Vad vill du ha att dricka då?')
        self.scriptSay("Något hett!")

    def talkWhatsUp(self):
        self.Game.Player.scriptSay('Hur är läget?')
        self.scriptSay("Jag är törstig!")
        self.addTopic('drink','Vad vill du ha att dricka?',self.talkDrink)
        self.removeTopic('whatsup')

    def talkSky(self):
        self.Game.Player.scriptSay('Vilken himmel vi har!')
        self.scriptSay("Shoop the whoop!")
    
    def giveChiliToWorm(self):
        self.scriptSay("Hett, men jag vill ha något flytande")
    
    def givePotionToWorm(self):
        self.scriptSay("Visst, i flytande form men inte hett nog.")
    
    def giveFirepotionToWorm(self):
        self.Game.Inventory.removeItemFromName('firepotion')
        self.scriptSay("Tack! Du är min vän")
        self.happyWorm = True
    
    def wormLook(self):
        self.Game.Player.scriptSay("Det är en mask.")
    
    def wormUse(self):
        self.scriptSay("STOP POKING ME!")
    
    def wormPickup(self):
        self.scriptSay("Du kan ju inte bara plocka upp mig sådär!")
        
    def wormTalk(self):
        self.scriptSay("'sup?")                

 