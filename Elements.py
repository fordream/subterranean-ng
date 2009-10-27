import os,pygame

class Element:
	def __init__(self):
		self.debugMessage = self.__class__.__name__
		
	def setDebugText(self,text):
		self.debugMessage = text
			
class VisibleElement(Element):
	def __init__(self):
		self.image = None
		self.rect = None
		self.retrievable = False
		self.usable = False
		self.isCharacter = False

	def setImage(self,fileName):
		self.image = pygame.image.load(os.path.join('data','elements',fileName))
		if self.rect is None:
			self.rect = self.image.get_rect()
	
	def setPosition(self,pos):
		self.rect.move_ip(pos)
		
	def setRetrievable(self,status):
		self.retrievable = status
		
	def setUsable(self,status):
		self.usable = status

	def setCharacter(self,status):
		self.isCharacter = status
		
class AnimatedElement(VisibleElement):
	def __init__(self):
		self.sequences = {}
		self.currentFrame = 0
		self.currentSequence = None
		
	def addSequence(sequenceName,frames):
		self.sequences[sequenceName] = frames
		
	def getFrame():
		frame = self.sequences[self.currentSequence][self.currentFrame]
		if self.currentFrame >= len(self.sequences[currentSequence]-1):
			self.currentFrame = 0
		else:
			self.currentFrame = self.currentFrame + 1
		return frame

class Area(Element):
	def __init__(self):
		self.rect = pygame.Rect(0,0,0,0)
		
	def setSize(w,h):
		self.rect.inflate_ip(w,h)
	
	def setPosition(pos):
		self.rect.move_ip(pos)

class Puzzle(VisibleElement):
	def __init__(self):
		print self.__class__.__name__

class Character(AnimatedElement):
	def __init__(self):
		self.character = True
		self.name = None
		self.topics = ()
		def addTopic(topic):
			self.topics.append(topic)
			
class Widget(AnimatedElement):
	def __init__(self):
		print self.__class__.__name__

class Topic:
	def __init__(self,topicName):
		self.topicName
		self.dialouge
		
	def addDialouge(dialouge):
		pass
		#TODO