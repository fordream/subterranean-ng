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
		self.prefix = None
		self.currentElement = None
		
	def setPrefix(self,prefix):
		if prefix == 'USE':
			self.prefix = 'Use'
		elif prefix == 'PICKUP':
			self.prefix = 'Pick up'
		elif prefix == 'TALK':
			self.prefix = 'Talk to'
		elif prefix == 'LOOk':
			self.prefix = 'Look at'
					
	def setElement(self,element):
		self.currentElement = element

	def clearElement(self):
		self.currentElement = None
		
	def getTitle(self):
		if self.currentElement is not None:
			return '%s %s' % (self.prefix,self.currentElement.title)
							
class Conversation:
	def __init__(self,game):
		self.Game = game
		self.startFrame = None
		self.currentLineLenght = 100
		self.text = []
		
	def isActive(self):
		return len(self.text) > 0
		
	def setText(self,text):
		self.text = text
		
	def resetStartFrame(self):
		self.startFrame = self.Game.Renderer.Timer.currentFrame
		
	def getText(self):
		if self.startFrame is None:
			self.resetStartFrame()
		if len(self.text):
			if self.Game.Renderer.Timer.currentFrame - self.currentLineLenght == self.startFrame:
				self.text.pop()
				if len(self.text) < 1:
					self.startFrame = None
					return
				self.resetStartFrame()
			return self.text[0]

			
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
				self.Game.TitleManager.setPrefix(self.getCursor())
				self.currentElement = element
				if self.getCursor() == 'DEFAULT':
					self.setCursor(1)
				return

		self.Game.TitleManager.clearElement()
		self.setCursor(0)
		self.currentElement = None;