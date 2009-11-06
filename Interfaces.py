import os,pygame

class Inventory:
	def __init__(self,game):
		self.Game = game
		self.items = []
		self.visible = False
		self.surface = pygame.Surface((1024,70))
		self.surface.fill((25,25,25))
		self.pos = (0,0)
		
	def addItem(self,item):
		self.items.append(item)
		
	def show(self):
		self.Game.pause()
		self.visible = True

	def hide(self):
		self.Game.unpause()
		self.visible = False
		
	def toggle(self):
		if self.visible:
			self.hide()
		else:
			self.show()
			
class TitleManager:
	def __init__(self,game):
		self.Game = game
		self.currentElement = None
		
	def setElement(self,element):
		self.currentElement = element

	def clearElement(self):
		self.currentElement = None
		
	def getTitle(self):
		if self.currentElement is not None:
			return self.currentElement.title
		
class ActionMenu:
	#UNUSED
	def __init__(self,game):
		self.Game = game
		self.visible = False
		self.image = pygame.image.load(os.path.join('data','interface','actionmenu.png'))
		
	def getFrame(self):
		if self.visible:
			return self.image
			
	def getPosition(self):
		return self.pos
	
	def setPosition(self,pos):
		newpos = (pos[0]-self.image.get_width()/2,pos[1]-self.image.get_height()/2)
		self.pos = newpos
		
	def show(self):
		self.Game.pause()
		self.visible = True
		self.setPosition(pygame.mouse.get_pos())

	def hide(self):
		self.Game.unpause()
		self.visible = False
		self.setPosition((0,0))
		
	def toggle(self):
		if self.visible:
			self.hide()
		else:
			self.show()
							
class Conversation:
	def __init__(self,game):
		self.Game = game
		self.isActive = False
		self.currentText = None
		
	def setText(self,text):
		self.currentText = text
		
	def activate(self):
		self.isActive = True

	def deactivate(self):
		self.isActive = False
			
class Cursor():
	def __init__(self,game):
		self.Game = game
		self.currentElement = None;
		self.cursors = ['DEFAULT','USE','PICKUP','TALK','LOOK']
		self.cursorIndex = None
		self.setCursor(0)
     
	def setCursor(self,cursorIndex):
		if self.cursors[cursorIndex] is not None:
			self.cursorIndex = cursorIndex
			
	def getCursor(self):
		return self.cursors[self.cursorIndex]
		
	def nextCursor(self):
		if self.cursorIndex < len(self.cursors)-1:
			return self.cursorIndex + 1
		else:
			return 0

	def previousCursor(self):
		if self.cursorIndex > 1:
			return self.cursorIndex-1
		else:
			return len(self.cursors)-1
					
	def scrollCursor(self,direction):
		if direction == 4:
			self.setCursor(self.nextCursor())
		else:
			self.setCursor(self.previousCursor())
			
	def checkCollisions(self):
		for element in self.Game.currentScene.visibleElements:
			if(element.rect.collidepoint(pygame.mouse.get_pos())):
				self.Game.TitleManager.setElement(element)
				self.currentElement = element
				if self.getCursor() == 'DEFAULT':
					self.setCursor(1)
				return

		self.Game.TitleManager.clearElement()
		self.setCursor(0)
		self.currentElement = None;