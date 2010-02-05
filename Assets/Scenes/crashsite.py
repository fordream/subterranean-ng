#-coding:utf-8-
from Libraries.Scene import Scene

class Room(Scene):

    def __init__(self,game):
        self.Game = game
        Scene.__init__(self,self.Game)
        self.setBackground('CRASHSITE_BACKGROUND')
        self.setMap('crashsite.map')
        self.enter()
        
    def enter(self):
        self.setInsertPoint((140,560))
        self.setFarthestPoint(420)
        self.setClosestPoint(725)

        self.Game.AudioController.playMusic('CRASHSITE')
        self.Game.AudioController.playAmbienceSound('AMBI_RIVER')
        #self.Game.Player.scriptWalk((220,640))
        self.show()