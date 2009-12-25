#-coding:utf-8-
from Scene import Scene
from Elements import Element,VisibleElement,AnimatedElement,Area,Puzzle,Character,Item,Widget
from Interfaces import ElementWindow

class Room(Scene):

    def __init__(self,game):
        self.Game = game
        Scene.__init__(self,self.Game)
        self.setBackground('crashsite.jpg')
        self.setMap('crashsite.map')
        
        self.enter()
        
    def enter(self):
        self.setInsertPoint((240,420))
        self.setFarthestPoint(350)
        self.setClosestPoint(715)
        self.setFarthestScale(45)
        self.setClosestScale(100)

        self.Game.AudioController.playMusic('DEFAULT')
        self.Game.AudioController.playAmbienceSound('AMBI001')

        self.show()