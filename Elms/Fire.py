from Elements import AnimatedElement

class Fire(AnimatedElement):
    def __init__(self,game):
        AnimatedElement.__init__(self)
        self.Game = game
        self.setName("fire")
        self.setTitle('Fire')
        self.setImage('fire1.png')
        self.addSequence('default',[
            'fire1.png',
            'fire2.png',
            'fire3.png',
            'fire4.png',
            'fire3.png',
            'fire2.png',
            'fire1.png',
            ])
        self.setPosition((540,276))
        self.setActionPosition((434,446))
        self.setLookMethod(self.fireLook)
        self.setUseMethod(self.fireUse)
        
    def fireLook(self):
        self.Game.Player.scriptSay("Mmm... varmt","PLAYER003")

    def fireUse(self):
        self.Game.Player.scriptSay("Aj!")
    
