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

        self.talkedToWorm = False
        self.happyWorm = False

        self.addVisibleElement(self.loadElement('Fire'))
        self.addVisibleElement(self.loadCharacter('Worm'))
        self.addVisibleElement(self.loadElement('Map'))
                
        self.Game.AudioController.playAmbienceSound('AMBI001')
                                    
        self.setPos1((24,500))
        self.setPos2((1000,500))
        self.setCameraPos((512,700))

        self.Game.Inventory.addItem(self.loadItem('Potion'))
        self.Game.Inventory.addItem(self.loadItem('Chili'))
        self.addExit(290,230,125,200,(330,400),"Bar",'NORTH')
        self.enter()

    def enter(self):
        self.Game.AudioController.playMusic('THEME')
        self.setInsertPoint((334,416))        
        self.show()
        
        #self.Game.Player.walkTo((500,670))