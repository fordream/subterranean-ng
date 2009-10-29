import os,pygame
import AStar
from time import time

class Player:
	def __init__(self,game):
		self.Game = game
		self.rect = None
		self.visible = False
		self.currentKeyframe = 0
		self.currentFrame = 0
		self.frameDuration = 3
		self.callbackMethod = None
		self.callbackArgument = None
		self.rect = pygame.Rect(0,0,60,20)
		self.direction = 's'
		self.directions = {
			'ns':self.loadFrame('north','stand'),
			'es':self.loadFrame('east','stand'),
			'ss':self.loadFrame('south','stand'),
			'ws':self.loadFrame('west','stand'),
			'nes':self.loadFrame('northeast','stand'),
			'ses':self.loadFrame('southeast','stand'),
			'sws':self.loadFrame('southwest','stand'),
			'nws':self.loadFrame('northwest','stand'),
			'ew':[self.loadFrame('east','walk','1'),self.loadFrame('east','walk','2'),self.loadFrame('east','walk','3'),self.loadFrame('east','walk','4')],
			'ww':[self.loadFrame('west','walk','1'),self.loadFrame('west','walk','2'),self.loadFrame('west','walk','3'),self.loadFrame('west','walk','4')],
		}
		self.pos = (0,0)
		self.renderPos = (0,0)
		self.walking = False
		self.talking = False
		
		self.path = []
		
	def loadFrame(self,direction,status,frame=None):
		if frame is not None:
			return pygame.image.load(os.path.join('data','maincharacter',direction+'-'+status+'-'+frame+'.png'))
		else:
			return pygame.image.load(os.path.join('data','maincharacter',direction+'-'+status+'.png'))
			
	def findPath(self,x,y):
		startX = self.getX()/16
		startY = self.getY()/16
		endX = x/16
		endY = y/16
		astar = AStar.AStar(AStar.SQ_MapHandler(self.Game.currentScene.mapData,64,48))
		start = AStar.SQ_Location(startX,startY)
		end = AStar.SQ_Location(endX,endY)
		path = astar.findPath(start,end)
		if path is not None:
			self.path = []
			self.path.append((start.x*16,start.y*16))
			for node in path.nodes:
				self.path.append((node.location.x*16,node.location.y*16))
			self.path.append((end.x*16,end.y*16))
			return True
		else:
			return False

	def walkTo(self,(x,y),callbackMethod=None,argument=None):
		if callbackMethod is not None and argument is not None:
			self.callbackMethod = callbackMethod
			self.argument = argument
		if not self.walking:
			if self.findPath(x,y):
				self.walking = True
				self.walk()
			else:
				print "No avalible tiles at",x,y
		
	def walk(self):
		if len(self.path):
			self.setPosition(self.path[0])
			self.path.pop(0)
			if len(self.path) > 1:
				self.setDirection(self.path[1])
		else:
			self.walking = False
			if self.callbackMethod is not None:
				self.runCallback()
				
	def runCallback(self):
		self.callbackMethod(self.argument)
		self.callbackMethod = None
		self.callbackArgument = None
		
	def getFrame(self):
		if self.walking:
			sequence = self.directions.get(self.getDirection()+'w')
			if sequence is not None:
				if self.currentFrame <= self.frameDuration:
					print "FRAMECOUNT"
					self.currentFrame += 1
				else:
					self.currentFrame = 0
					print "NEXT"
					if self.currentKeyframe < len(sequence)-1:
						self.currentKeyframe += 1
					else:
						self.currentKeyframe = 0
				print self.currentKeyframe
				print self.currentFrame
				return sequence[self.currentKeyframe]
			else:
				#Stand if fail
				return self.directions.get(self.getDirection()+'s')
		elif self.talking:
			pass
		else:
			return self.directions.get(self.getDirection()+'s')
			
	def getRenderPos(self):
		return self.renderPos

	def setPosition(self,pos):
		self.rect.move_ip(pos[0],pos[1])
		self.pos = pos
		self.renderPos = (self.pos[0],self.pos[1]-180)
		
	def setDirection(self,newPos):
		if self.getPosition()[0] < newPos[0] and self.getPosition()[1] == newPos[1]:
			self.direction = 'e'
		elif self.getPosition()[0] > newPos[0] and self.getPosition()[1] == newPos[1]:
			self.direction = 'w'
		elif self.getPosition()[0] == newPos[0] and self.getPosition()[1] < newPos[1]:
			self.direction = 's'
		elif self.getPosition()[0] == newPos[0] and self.getPosition()[1] > newPos[1]:
			self.direction = 'n'
		elif self.getPosition()[0] < newPos[0] and self.getPosition()[1] < newPos[1]:
			self.direction = 'se'
		elif self.getPosition()[0] > newPos[0] and self.getPosition()[1] > newPos[1]:
			self.direction = 'nw'
		elif self.getPosition()[0] < newPos[0] and self.getPosition()[1] > newPos[1]:
			self.direction = 'ne'
		elif self.getPosition()[0] > newPos[0] and self.getPosition()[1] < newPos[1]:
			self.direction = 'sw'
		
	def getDirection(self):
		return self.direction
			
	def getPosition(self):
		return self.pos
						
	def getX(self):
		return self.pos[0]
		
	def getY(self):
		return self.pos[1]
		
	def inRange(self,element):
		#TODO: Refine this? Currently has a range of 100px
		closenessX = self.getPosition()[0] - element.getBasePosition()[0]
		closenessY = self.getPosition()[1] - element.getBasePosition()[1]
		return(closenessX + closenessY < 100 and closenessX + closenessY > -100)
		
	def pickUp(self,item):
		if self.inRange(item):
			self.Game.currentScene.visibleElements.remove(item)
			self.Game.Inventory.addItem(item)
			print "Picked up",item.getTitle()
		
	def use(self,widget):
		if self.inRange(widget):
			print "Used",widget.getTitle()

	def talk(self,person):
		if self.inRange(person):
			print "Talking to",person.getTitle()
			self.Game.Conversation.activate()