#-coding:utf-8-
from Libraries.Scene import Scene

class Room(Scene):
    def __init__(self,game):
        self.Game = game
        Scene.__init__(self,self.Game)
        self.setBackground('BLACKSMITH_BACKGROUND')
        self.setForeground('BLACKSMITH_FOREGROUND')
        self.setMap('foo.map')

        self.talkedToWorm = False
        self.happyWorm = False

        self.addVisibleElement(self.loadElement('Fire'))
        self.addVisibleElement(self.loadElement('Toolbarrel'))
        self.addVisibleElement(self.loadCharacter('Grimvald'))
                
        self.Game.Inventory.addItem(self.loadItem('Potion'))
        self.Game.Inventory.addItem(self.loadItem('Chili'))
        self.Game.Inventory.addItem(self.loadItem('Lighter'))
        self.addExit(290,230,125,200,(330,420),"watermill",'NORTH')
        self.addExit(550,600,125,75,(550,670),"crashsite",'WEST')
        self.enter()

    def enter(self):
        self.Game.AudioController.playMusic('STANDARDMYS')
        self.Game.AudioController.playAmbienceSound('AMBI_DEFAULT')
        self.setInsertPoint((360,420))      
        
        self.setFarthestPoint(415)
        self.setClosestPoint(715)
        self.setFarthestScale(50)
        self.setClosestScale(100)

        self.show()
        self.Game.Player.scriptWalk((360,490))