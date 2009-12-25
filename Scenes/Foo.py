#-coding:utf-8-
from Scene import Scene
from Elements import Element,VisibleElement,AnimatedElement,Area,Puzzle,Character,Item,Widget
from Interfaces import ElementWindow

class Room(Scene):

    def __init__(self,game):
        self.Game = game
        Scene.__init__(self,self.Game)
        self.setBackground('foo.jpg')
        self.setForeground('foo.png')
        self.setMap('Foo.map')

        self.talkedToWorm = False
        self.happyWorm = False

        self.addVisibleElement(self.loadElement('Fire'))
        self.addVisibleElement(self.loadElement('Map'))
        self.addVisibleElement(self.loadCharacter('Grumpley'))
                
        self.Game.Inventory.addItem(self.loadItem('Potion'))
        self.Game.Inventory.addItem(self.loadItem('Chili'))
        self.addExit(290,230,125,200,(330,400),"bar",'NORTH')
        self.addExit(550,600,125,75,(640,590),"crashsite",'WEST')
        self.enter()

    def enter(self):
        self.Game.AudioController.playMusic('THEME')
        self.Game.AudioController.playAmbienceSound('AMBI001')
        self.setInsertPoint((334,416))        
        
        self.setFarthestPoint(415)
        self.setClosestPoint(715)
        self.setFarthestScale(50)
        self.setClosestScale(100)

        self.show()
        
        #self.Game.Player.walkTo((500,670))