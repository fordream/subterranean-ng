#-coding:utf-8-
from Scene import Scene
from Elements import Element,VisibleElement,AnimatedElement,Area,Puzzle,Character,Item,Widget
from Interfaces import ElementWindow

class Room(Scene):

    def __init__(self,game):
        self.Game = game
        Scene.__init__(self,self.Game)
        self.setBackground('bar.jpg')
        self.setForeground('bar.png')
        self.setMap('Bar.map')
        self.addVisibleElement(self.loadElement('Map'))
        self.addExit(490,305,110,180,(550,500),"Foo",'NORTH')
        
        self.enter()
        
    def enter(self):
        self.Game.AudioController.playMusic('NOTEXPECTED')
        self.Game.AudioController.playAmbienceSound('WATER001')
        self.setInsertPoint((550,500))
        
        self.setFarthestPoint(415)
        self.setClosestPoint(715)
        self.setFarthestScale(50)
        self.setClosestScale(100)

        self.Game.Player.scriptWalk((550,570))
        self.show()