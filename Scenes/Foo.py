from Scene import Scene
from Elements import Element,VisibleElement,AnimatedElement,Area,Puzzle,Character,Widget

class Room(Scene):

	def __init__(self,game):
		self.Game = game
		Scene.__init__(self,self.Game)
		self.setBackground('foo.jpg')
		self.setMap('Foo.map')
		self.setInsertPoint((0,300))

		wastebin = VisibleElement()
		wastebin.setTitle("Wastebin")
		wastebin.setImage('wastebin.png')	
		wastebin.setPosition((650,550))	
		wastebin.setDebugText("USE THE BIN")	
		wastebin.setUsable(True)	
		self.addVisibleElement(wastebin)
	
		worm = VisibleElement()
		worm.setTitle("Worm")
		worm.setImage('worm.png')	
		worm.setPosition((550,610))	
		worm.setDebugText("WORMZOR")	
		worm.setRetrievable(True)	
		self.addVisibleElement(worm)
				
		self.show()
		
		#self.Game.Player.walkTo((500,670))