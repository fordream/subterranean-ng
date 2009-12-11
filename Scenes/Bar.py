#-coding:utf-8-
from Scene import Scene
from Elements import Element,VisibleElement,AnimatedElement,Area,Puzzle,Character,Item,Widget
from Interfaces import ElementWindow

class Room(Scene):

    def __init__(self,game):
        self.Game = game
        Scene.__init__(self,self.Game)
        self.setBackground('wheel.jpg')
        self.setMap('Bar.map')
        self.setInsertPoint((465,434))
        self.Game.AudioController.playMusic('THEME')
        self.addExit(440,260,100,150,(465,420),"Foo",'NORTH')
        self.show()
        
        #self.Game.Player.walkTo((500,670))