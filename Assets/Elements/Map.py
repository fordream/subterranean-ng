# -*- coding: utf-8 -*-
from Elements import VisibleElement,AnimatedElement,Widget
from Interfaces import ElementWindow

class Map(AnimatedElement):
    def __init__(self,game):
        AnimatedElement.__init__(self)
        self.Game = game
        
        self.setName("dungeonmap")
        self.setTitle('Dungeon map')
        self.setImage('dungeonmap.png')
        self.setPosition((624,276))
        self.setActionPosition((624,476))
     
        self.setLookMethod(self.mapLook)
        self.setUseMethod(self.mapUse)        
        
        self.window = ElementWindow(self.Game)
        self.window.setBackground('dungeonmap.png')
        self.window.setOpenMethod(self.openMapWindow)
        self.window.setCloseMethod(self.closeMapWindow)
                   
        cross = Widget()
        cross.setName('cross')
        cross.setTitle('Du är här')
        cross.setImage('cross.png')
        cross.setPosition((338,208))
        self.window.addWidget(cross)

        room1 = Widget()
        room1.setName('cross')
        room1.setTitle('Solgruvan')
        room1.setImage('room1.png')
        room1.setPosition((80,127))
        self.window.addWidget(room1)

        room2 = Widget()
        room2.setName('cross')
        room2.setTitle('Portarna')
        room2.setImage('room2.png')
        room2.setPosition((360,64))
        self.window.addWidget(room2)
        
        room3 = Widget()
        room3.setName('cross')
        room3.setTitle('Undergård')
        room3.setImage('room3.png')
        room3.setPosition((520,84))
        self.window.addWidget(room3)

        room3.setClickMethod(self.room3Click)
        
        room4 = Widget()
        room4.setName('cross')
        room4.setTitle('Underjordsfloden')
        room4.setImage('room4.png')
        room4.setPosition((530,365))
        self.window.addWidget(room4)
        
        room5 = Widget()
        room5.setName('cross')
        room5.setTitle('Smedjan')
        room5.setImage('room5.png')
        room5.setPosition((244,378))
        self.window.addWidget(room5)

        room6 = Widget()
        room6.setName('cross')
        room6.setTitle('Brytrummet')
        room6.setImage('room6.png')
        room6.setPosition((125,305))
        self.window.addWidget(room6)
        
    def mapUse(self):
        self.window.show()

    def mapLook(self):
        self.mapUse()
        
    def openMapWindow(self):
        self.Game.AudioController.playUISound('MAP')
        self.Game.Player.scriptSay('En karta. Så användarvänligt!')
        self.Game.Player.scriptSay('Hm, det verkar vara ett enda virrvarr av gångar.')
        
    def closeMapWindow(self):
        self.Game.AudioController.playUISound('MAP')
        self.Game.Player.scriptSay('Jag kommer inte att komma ihåg något ändå med mitt lokalsinne.')
    
    def room3Click(self):
        self.Game.Player.scriptSay("Undergård, det låter coolt. Jag borde gå dit.")    