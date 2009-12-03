#-coding:utf-8-
from Scene import Scene
from Elements import Element,VisibleElement,AnimatedElement,Area,Puzzle,Character,Item,Widget
from Interfaces import ElementWindow

class Room(Scene):

    def __init__(self,game):
        self.Game = game
        Scene.__init__(self,self.Game)
        self.setBackground('foo.jpg')
        self.setMap('Foo.map')
        self.setInsertPoint((334,416))
        self.talkedToWorm = False
        self.happyWorm = False
        
        Fire = self.addVisibleElement(self.loadElement('Fire'))

        firepotion = Item('firepotion','Eldig k�rleksdryck')
        potion = Item('potion','K�rleksdryck')
        potion.addCombination('chili',firepotion)
        self.Game.Inventory.addItem(potion)

        chili = Item('chili','Het chili')
        chili.addCombination('potion',firepotion)
        self.Game.Inventory.addItem(chili) 
        
        Worm = self.addVisibleElement(self.loadElement('Worm'))
        
        self.Game.AudioController.playAmbienceSound('AMBI001')
        
        dungeonMapWindow = ElementWindow(self.Game)
        dungeonMapWindow.setBackground('dungeonmap.png')
        
        def openMapWindow():
            self.Game.AudioController.playUISound('MAP')
            self.Game.Player.scriptSay('En karta. S� anv�ndarv�nligt!')
            self.Game.Player.scriptSay('Hm, det verkar vara ett enda virrvarr av g�ngar.')
            
        def closeMapWindow():
            self.Game.AudioController.playUISound('MAP')
            self.Game.Player.scriptSay('Jag kommer inte att komma ih�g n�got �nd� med mitt lokalsinne.')
            
        dungeonMapWindow.setOpenMethod(openMapWindow)
        dungeonMapWindow.setCloseMethod(closeMapWindow)
        
        cross = Widget()
        cross.setName('cross')
        cross.setTitle('Du �r h�r')
        cross.setImage('cross.png')
        cross.setPosition((338,208))
        dungeonMapWindow.addWidget(cross)

        room1 = Widget()
        room1.setName('cross')
        room1.setTitle('Solgruvan')
        room1.setImage('room1.png')
        room1.setPosition((80,127))
        dungeonMapWindow.addWidget(room1)

        room2 = Widget()
        room2.setName('cross')
        room2.setTitle('Portarna')
        room2.setImage('room2.png')
        room2.setPosition((360,64))
        dungeonMapWindow.addWidget(room2)
        
        room3 = Widget()
        room3.setName('cross')
        room3.setTitle('Underg�rd')
        room3.setImage('room3.png')
        room3.setPosition((520,84))
        dungeonMapWindow.addWidget(room3)
        
        def room3Click():
            self.Game.Player.scriptSay("Underg�rd, det l�ter coolt. Jag borde g� dit.")
        room3.setClickMethod(room3Click)
        
        room4 = Widget()
        room4.setName('cross')
        room4.setTitle('Underjordsfloden')
        room4.setImage('room4.png')
        room4.setPosition((530,365))
        dungeonMapWindow.addWidget(room4)
        
        room5 = Widget()
        room5.setName('cross')
        room5.setTitle('Smedjan')
        room5.setImage('room5.png')
        room5.setPosition((244,378))
        dungeonMapWindow.addWidget(room5)

        room6 = Widget()
        room6.setName('cross')
        room6.setTitle('Brytrummet')
        room6.setImage('room6.png')
        room6.setPosition((125,305))
        dungeonMapWindow.addWidget(room6)
                        
        dungeonMap = VisibleElement()
        dungeonMap.setName("dungeonmap")
        dungeonMap.setTitle('Dungeon map')
        dungeonMap.setImage('dungeonmap.png')
        dungeonMap.setPosition((624,276))
        dungeonMap.setActionPosition((624,476))


        def mapUse():
            dungeonMapWindow.show()

        def mapLook():
            mapUse()
            
        dungeonMap.setLookMethod(mapLook)
        dungeonMap.setUseMethod(mapUse)
        
        self.addVisibleElement(dungeonMap)

        self.setPos1((24,500))
        self.setPos2((1000,500))
        self.setCameraPos((512,700))
        self.Game.AudioController.playMusic('THEME')
        self.show()
        
        #self.Game.Player.walkTo((500,670))