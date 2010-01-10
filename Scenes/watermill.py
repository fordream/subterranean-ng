#-coding:utf-8-
from Scene import Scene

class Room(Scene):
    def __init__(self,game):
        self.Game = game
        Scene.__init__(self,self.Game)
        self.setBackground('WATERMILL_BACKGROUND')
        self.setForeground('WATERMILL_FOREGROUND')
        self.addVisibleElement(self.loadElement('Map'))
        self.setMap('bar.map')
        self.addExit(490,305,110,180,(550,500),"blacksmith",'NORTH')
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