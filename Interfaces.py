import os,pygame

class Inventory:
	def __init__(self,game):
		self.Game = game
		self.items = []
		
	def addItem(self,item):
		self.items.append(item)
		self.Game.currentRoom.visibleElements.remove(item)
		
class Menu:
	def __init__(self,game):
		pass
		
class Conversation:
	def __init__(self,game):
		self.isActive = True
		self.Game = game
		self.currentText="This is sparta!"
	
class Cursor():
	def __init__(self,game):
		self.Game = game
		self.cursor = None
		self.currentElement = None;
		self.loadCursors()
		self.setCursor('DEFAULT')
       
   	def loadCursors(self):
	   	self.cursors = ['DEFAULT','PICKUP','USE','TALK']
     
	def setCursor(self,cursorName):
		if cursorName in self.cursors:
			self.cursor = cursorName
			
	def checkCollisions(self):
		for element in self.Game.currentRoom.visibleElements:
			#FIXME: Weird Y offset by 24px
			weirdOffset = (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]-40)
			if(element.rect.collidepoint(weirdOffset)):
				if element.usable:
					self.setCursor('USE')
					self.currentElement = element;
				elif element.retrievable:
					self.setCursor('PICKUP')
					self.currentElement = element;
				elif element.isCharacter:
					self.setCursor('TALK')
					self.currentElement = element;
				return
		self.setCursor('DEFAULT')
		self.currentElement = None;