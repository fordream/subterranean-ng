#-coding:utf-8-
from Scene import Scene
from Elements import Element,VisibleElement,AnimatedElement,Area,Puzzle,Character,Widget

class Room(Scene):

    def __init__(self,game):
        self.Game = game
        Scene.__init__(self,self.Game)
        self.setBackground('foo.jpg')
        self.setMap('Foo.map')
        self.setInsertPoint((334,416))
        self.talkedToWorm = False

        wastebin = VisibleElement()
        wastebin.setName("wastebin")
        wastebin.setTitle('Wastebin of the frozen throne!')
        wastebin.setImage('wastebin.png')   
        wastebin.setPosition((652,365)) 
        #self.addVisibleElement(wastebin)
        
        fire = VisibleElement()
        fire.setName("fire")
        fire.setTitle('Fire')
        fire.setImage('fire.png')
        fire.setPosition((537,275))   

        def fireLook():
            self.Game.Player.scriptSay("Mmm... varmt")

        def fireUse():
            self.Game.Player.scriptSay("Aj!")
            
        fire.setLookMethod(fireLook)
        fire.setUseMethod(fireUse)

        self.addVisibleElement(fire)

        potion = VisibleElement()
        potion.setName("potion")
        potion.setTitle('Love potion')
        potion.setImage('potion.png')
        potion.setPosition((500,610))
        self.Game.Inventory.addItem(potion)                

        chili = VisibleElement()
        chili.setName("chili")
        chili.setTitle('Hot chili')
        chili.setImage('chili.png')   
        chili.setPosition((470,610))
        self.Game.Inventory.addItem(chili)                
        
        worm = Character(self.Game)
        worm.setName("worm")
        worm.setTitle('Worm')
        worm.setImage('worm.png')
        worm.setPosition((434,446))
        worm.setTextColor((255,128,0))

        def wormLook():
            self.Game.Player.scriptSay("Det är en mask.")

        def wormUse():
            worm.scriptSay("STOP POKING ME!")

        def wormPickup():
            worm.scriptSay("Du kan ju inte bara plocka upp mig sådär!")
            
        def wormTalk():
            self.Game.TopicMenu.display()
            self.Game.TopicMenu.addTopic('I can has lazor?')
            self.Game.TopicMenu.addTopic('Arn us the go')
            self.Game.TopicMenu.addTopic('Vem är du?')
            self.Game.TopicMenu.addTopic('What is love?')
            self.Game.TopicMenu.addTopic('Slarn the garn!')
            self.Game.TopicMenu.addTopic('Bye for now')
            
            if self.talkedToWorm is False:
                self.Game.Player.scriptSay('Hej din gamle mask')
                worm.scriptSay('Hej där, random huvudperson')
                self.Game.Player.scriptSay('Jag har så mycket att prata med dig om!')
                worm.scriptSay('Samma här, men ämnesmenyn är inte klar än.')
                self.Game.Player.scriptSay('Okej. Åtminstone kan vi se den')
                self.talkedToWorm = True
            else:
                self.Game.Player.scriptSay('Hej igen')
                worm.scriptSay('Sluta stör mig och gör klart ämnesmenyn istället!')

        worm.setUseMethod(wormUse)
        worm.setLookMethod(wormLook)
        worm.setTalkMethod(wormTalk)
        worm.setPickupMethod(wormPickup)
        
        self.addVisibleElement(worm)        
        self.show()
        
        #self.Game.Player.walkTo((500,670))