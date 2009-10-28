from Scene import Scene
from Elements import Element,VisibleElement,AnimatedElement,Area,Puzzle,Character,Widget

class Room(Scene):

	def __init__(self):
		Scene.__init__(self)
		self.setBackground('foo.jpg')
		self.setMap('Foo.map')
		
		self.setInsertPoint((10,10))
				
		fooElement = VisibleElement()
		fooElement.setImage('worm.png')	
		fooElement.setPosition((344,232))	
		fooElement.setDebugText("OMGLAWLS")	
		fooElement.setRetrievable(True)	
		self.addVisibleElement(fooElement)
		
		self.show()
	