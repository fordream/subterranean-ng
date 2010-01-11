#-coding:utf-8-
from Scene import Scene

class Room(Scene):

    def __init__(self,game):
        self.Game = game
        Scene.__init__(self,self.Game)
        self.setBackground('CRASHSITE_BACKGROUND')
        self.setMap('crashsite.map')
        
        self.enter()
        
    def enter(self):
        self.setInsertPoint((220,420))
        self.setFarthestPoint(350)
        self.setClosestPoint(715)
        self.setFarthestScale(45)
        self.setClosestScale(100)

        self.Game.AudioController.playMusic('DEFAULT')
        self.Game.AudioController.playAmbienceSound('AMBI001')

        self.Game.Player.scriptWalk((220,440))
        self.show()