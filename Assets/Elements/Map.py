# -*- coding: utf-8 -*-
from Libraries.Elements import VisibleElement,AnimatedElement,Widget
from Libraries.ElementWindow import ElementWindow

class Map(AnimatedElement):
    def __init__(self,game):
        AnimatedElement.__init__(self)
        self.Game = game
        
        self.setName("dungeonmap")
        self.setTitle('Dungeon map')
        self.setImage(self.Game.get('MAP_DEFAULT'))
        self.setPosition((330,326))
        self.setActionPosition((410,500))
     
        self.setLookMethod(self.mapLook)
        self.setUseMethod(self.mapUse)        
        
        self.window = ElementWindow(self.Game)
        self.window.setBackground(self.Game.get('MAP_BACKGROUND'))
        self.window.setOpenMethod(self.openMapWindow)
        self.window.setCloseMethod(self.closeMapWindow)
                   
        cross = Widget()
        cross.setName('cross')
        cross.setTitle('You are here')
        cross.setImage(self.Game.get('MAP_CROSS'))
        cross.setPosition((338,208))
        self.window.addWidget(cross)

        room1 = Widget()
        room1.setName('cross')
        room1.setTitle('The Sunmine')
        room1.setImage(self.Game.get('MAP_SUNMINE'))
        room1.setPosition((80,127))
        self.window.addWidget(room1)

        room2 = Widget()
        room2.setName('cross')
        room2.setTitle('The Gates')
        room2.setImage(self.Game.get('MAP_GATES'))
        room2.setPosition((360,64))
        self.window.addWidget(room2)
        
        room3 = Widget()
        room3.setName('cross')
        room3.setTitle("The Elderbeards' chamber")
        room3.setImage(self.Game.get('MAP_CHAMBER'))
        room3.setPosition((520,84))
        self.window.addWidget(room3)
        
        room4 = Widget()
        room4.setName('cross')
        room4.setTitle('The Underfjord')
        room4.setImage(self.Game.get('MAP_UNDERFJORD'))
        room4.setPosition((530,365))
        self.window.addWidget(room4)
        
        room5 = Widget()
        room5.setName('cross')
        room5.setTitle('The altar')
        room5.setImage(self.Game.get('MAP_ALTAR'))
        room5.setPosition((244,378))
        self.window.addWidget(room5)

        room6 = Widget()
        room6.setName('cross')
        room6.setTitle('The Quarry')
        room6.setImage(self.Game.get('MAP_QUARRY'))
        room6.setPosition((125,305))
        self.window.addWidget(room6)

        cross.setClickMethod(self.crossClick)        
        room1.setClickMethod(self.room1Click)
        room2.setClickMethod(self.room2Click)
        room3.setClickMethod(self.room3Click)
        room4.setClickMethod(self.room4Click)
        room5.setClickMethod(self.room5Click)
        room6.setClickMethod(self.room6Click)
        
    def mapUse(self):
        self.window.show()

    def mapLook(self):
        self.mapUse()
        
    def openMapWindow(self):
        self.Game.AudioController.playUISound("MAP_OPEN")
        
    def closeMapWindow(self):
        self.Game.AudioController.playUISound('MAP')
        self.Game.Player.scriptSay("Too bad I'm worthless at orientation")

    def crossClick(self):
        self.Game.Player.scriptSay("I am here, but where is \"here\"?")
    
    def room1Click(self):
        self.Game.Player.scriptSay("Perhaps there's a way out at the Sunmine?")
    
    def room2Click(self):
        self.Game.Player.scriptSay("The Gates to where?")
    
    def room3Click(self):
        self.Game.Player.scriptSay("Perhaps I can find answers there.")
    
    def room4Click(self):
        self.Game.Player.scriptSay("There's water this deep underground?")
    
    def room5Click(self):
        self.Game.Player.scriptSay("Sounds mysterious.")
        
    def room6Click(self):
        self.Game.Player.scriptSay("Perhaps I can borrow some tools an dig a way out.")