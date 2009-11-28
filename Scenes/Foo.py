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
            self.Game.Player.scriptSay("Mmm... varmt","PLAYER003")

        def fireUse():
            self.Game.Player.scriptSay("Aj!")
            
        fire.setLookMethod(fireLook)
        fire.setUseMethod(fireUse)
        self.addVisibleElement(fire)

        firepotion = Item('firepotion','Eldig kärleksdryck')
    
        potion = Item('potion','Kärleksdryck')
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
        
        def talkDrink():
                self.Game.Player.scriptSay('Jaså? Vad vill du ha att dricka då?')
                worm.scriptSay("Något hett!")

        def talkWhatsUp():
                self.Game.Player.scriptSay('Hur är läget?')
                worm.scriptSay("Jag är törstig!")
                worm.addTopic('drink','Vad vill du ha att dricka?',talkDrink)
                worm.removeTopic('whatsup')

        def talkSky():
                self.Game.Player.scriptSay('Vilken himmel vi har!')
                worm.scriptSay("Shoop the whoop!")
                
        worm.addTopic('whatsup','Hur är läget?',talkWhatsUp)
        worm.addTopic('whatsup','Tror ni på hjulen?',talkSky)
        worm.addTopic('whatsup','Var är paketet?',talkSky)
        worm.addTopic('whatsup','Hur får man upp den röda dörren?',talkSky)
        worm.addTopic('whatsup','Vad är kärlek?',talkSky)
        worm.addTopic('whatsup','Är du en vampyr?',talkSky)


        worm.addTopic('sky','Vilken himmel vi har!',talkSky)
        
        def giveChiliToWorm():
            worm.scriptSay("Hett, men jag vill ha något flytande")
        
        def givePotionToWorm():
            worm.scriptSay("Visst, i flytande form men inte hett nog.")
        
        def giveFirepotionToWorm():
            self.Game.Inventory.removeItemFromName('firepotion')
            worm.scriptSay("Tack! Du är min vän")
            self.happyWorm = True
            
        worm.addGiveMethod(giveChiliToWorm,'chili')
        worm.addGiveMethod(givePotionToWorm,'potion')
        worm.addGiveMethod(giveFirepotionToWorm,'firepotion')
        
        def wormLook():
            self.Game.Player.scriptSay("Det är en mask.")
        
        def wormUse():
            worm.scriptSay("STOP POKING ME!")
        
        def wormPickup():
            worm.scriptSay("Du kan ju inte bara plocka upp mig sådär!")
            
        def wormTalk():
            worm.scriptSay("'sup?")                
        '''
            def talkDrink():
                worm.scriptSay("Jag vill ha något hett!")
                
            self.Game.TopicMenu.addTopic('Hejdå',self.Game.TopicMenu.hide)
            self.Game.TopicMenu.addTopic('Hur är läget?',talkWhatsup)
            
            if self.talkedToWorm is False:
                self.Game.Player.scriptSay('Hej din gamle mask!')
                worm.scriptSay('Hej hej...')
                self.talkedToWorm = True
            elif self.happyWorm:
                worm.scriptSay('Du är min vän, random huvudperson!')
            else:
                self.Game.Player.scriptSay('Hej igen')
                worm.scriptSay('Sluta stör mig och fixa mig en het dryck istället!')
        '''
        worm.setUseMethod(wormUse)
        worm.setLookMethod(wormLook)
        worm.setTalkMethod(wormTalk)
        worm.setPickupMethod(wormPickup)
        

        self.addVisibleElement(worm)        
        
        self.Game.AudioController.playAmbienceSound('AMBI001')
        self.show()
        
        #self.Game.Player.walkTo((500,670))