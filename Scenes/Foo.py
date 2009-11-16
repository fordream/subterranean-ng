#-coding:utf-8-
from Scene import Scene
from Elements import Element,VisibleElement,AnimatedElement,Area,Puzzle,Character,Widget,Item

class Room(Scene):

    def __init__(self,game):
        self.Game = game
        Scene.__init__(self,self.Game)
        self.setBackground('foo.jpg')
        self.setMap('Foo.map')
        self.setInsertPoint((334,416))
        self.talkedToWorm = False
        self.happyWorm = False
        
        fire = VisibleElement()
        fire.setName("fire")
        fire.setTitle('Fire')
        fire.setImage('fire.png')
        fire.setPosition((534,306))
        fire.setActionPosition((434,446))

        def fireLook():
            self.Game.Player.scriptSay("Mmm... varmt")

        def fireUse():
            self.Game.Player.scriptSay("Aj!")
            
        fire.setLookMethod(fireLook)
        fire.setUseMethod(fireUse)
        self.addVisibleElement(fire)

        firepotion = Item('firepotion','Eldig k�rleksdryck')
    
        potion = Item('potion','K�rleksdryck')
        potion.addCombination('chili',firepotion)
        self.Game.Inventory.addItem(potion)

        chili = Item('chili','Het chili')
        chili.addCombination('potion',firepotion)
        self.Game.Inventory.addItem(chili) 

        worm = Character(self.Game)
        worm.setName("worm")
        worm.setTitle('Mask')
        worm.setImage('worm.png')
        worm.setPosition((434,446))
        worm.setTextColor((255,128,0))
        
        def giveChiliToWorm():
            worm.scriptSay("Hett, men jag vill ha n�got flytande")

        def givePotionToWorm():
            worm.scriptSay("Visst, i flytande form men inte hett nog.")

        def giveFirepotionToWorm():
            self.Game.Inventory.removeItemFromName('firepotion')
            worm.scriptSay("Tack! Du �r min v�n")
            self.happyWorm = True
            
        worm.addGiveMethod(giveChiliToWorm,'chili')
        worm.addGiveMethod(givePotionToWorm,'potion')
        worm.addGiveMethod(giveFirepotionToWorm,'firepotion')

        def wormLook():
            self.Game.Player.scriptSay("Det �r en mask.")

        def wormUse():
            worm.scriptSay("STOP POKING ME!")

        def wormPickup():
            worm.scriptSay("Du kan ju inte bara plocka upp mig s�d�r!")
            
        def wormTalk():
            self.Game.TopicMenu.display()
            self.Game.TopicMenu.addTopic('I can has lazor?')
            self.Game.TopicMenu.addTopic('Vem �r du?')
            self.Game.TopicMenu.addTopic('What is love?')
            self.Game.TopicMenu.addTopic('Slarn the garn!')
            self.Game.TopicMenu.addTopic('Hej s� l�nge')
            
            if self.talkedToWorm is False:
                self.Game.Player.scriptSay('Hej din gamle mask')
                worm.scriptSay('Hej d�r, random huvudperson')
                self.Game.Player.scriptSay('Du ser lite nerkyld ut')
                worm.scriptSay('Jag vet, ge mig n�got som �r hett att dricka!')
                self.Game.Player.scriptSay('Jag ska se vad jag kan g�ra.')
                self.talkedToWorm = True
            elif self.happyWorm:
                worm.scriptSay('Du �r min v�n, random huvudperson!')
            else:
                self.Game.Player.scriptSay('Hej igen')
                worm.scriptSay('Sluta st�r mig och fixa mig en het dryck ist�llet!')

        worm.setUseMethod(wormUse)
        worm.setLookMethod(wormLook)
        worm.setTalkMethod(wormTalk)
        worm.setPickupMethod(wormPickup)
        
        self.addVisibleElement(worm)        
        self.show()
        
        #self.Game.Player.walkTo((500,670))