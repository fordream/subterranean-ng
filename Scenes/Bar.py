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
        self.addExit(490,305,110,180,(465,420),"Foo",'NORTH')
        
        self.enter()
        
    def enter(self):
        self.Game.AudioController.playMusic('NOTEXPECTED')
        self.Game.AudioController.playAmbienceSound('WATER001')
        self.setInsertPoint((465,500))
        
        self.setFarthestPoint(415)
        self.setClosestPoint(715)
        self.setFarthestScale(50)
        self.setClosestScale(100)

        self.show()
        
        #self.Game.Player.walkTo((500,670))