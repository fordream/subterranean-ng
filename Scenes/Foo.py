from Scene import Scene
from Elements import Element,VisibleElement,AnimatedElement,Area,Puzzle,Character,Widget

class Room(Scene):

	def __init__(self,game):
		self.Game = game
		Scene.__init__(self,self.Game)
		self.setBackground('foo.jpg')
		self.setMap('Foo.map')
		self.setInsertPoint((16,352))
				
		fooElement = VisibleElement()
		fooElement.setImage('worm.png')	
		fooElement.setPosition((550,650))	
		fooElement.setDebugText("OMGLAWLS")	
		fooElement.setRetrievable(True)	
		self.addVisibleElement(fooElement)
		
		self.show()
		
		#self.Game.Player.walkTo((500,670))
	