# -*- coding: utf-8 -*-
import os,pygame
import AStar
from time import time

class Player:
	def __init__(self,game):
		self.Game = game
		self.rect = None
		self.visible = False
		self.frameKey = 0
		self.startFrame = None
		self.startMillis = 0
		self.frameDuration = 3
		self.callbackMethod = None
		self.callbackArgument = None
		self.rect = pygame.Rect(0,0,60,20)
		self.direction = 's'
		self.directions = {
			'ns':self.loadFrames('north','stand',1),
			'es':self.loadFrames('east','stand',1),
			'ss':self.loadFrames('south','stand',1),
			'ws':self.loadFrames('west','stand',1),
			'nes':self.loadFrames('northeast','stand',1),
			'ses':self.loadFrames('southeast','stand',1),
			'sws':self.loadFrames('southwest','stand',1),
			'nws':self.loadFrames('northwest','stand',1),
			'nw':self.loadFrames('north','walk',1),
			'sw':self.loadFrames('south','walk',1),
			'sww':self.loadFrames('southwest','walk',1),
			'nww':self.loadFrames('northwest','walk',1),
			'sew':self.loadFrames('southeast','walk',1),
			'new':self.loadFrames('northeast','walk',1),
			'ew':self.loadFrames('east','walk',8),
			'ww':self.loadFrames('west','walk',8)
		}
		self.pos = (0,0)
		self.renderPos = (0,0)
		self.walking = False
		self.talking = False
		
		self.path = []
		
	def loadFrames(self,direction,status,frames=1):
		frameSet = []
		frameNum = 1
		while frameNum <= frames:
			frameSet.append(pygame.image.load(os.path.join('data','maincharacter','%s-%s-%d.png' % (direction,status,frameNum))))
			frameNum += 1
		return frameSet
			
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
		print callbackMethod
		if callbackMethod is not None and argument is not None:
			self.callbackMethod = callbackMethod
			self.argument = argument
		if not self.walking:
			if self.findPath(x,y):
				self.resetStartFrame()
				self.walking = True
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
		
	def resetStartFrame(self):
		self.startFrame = self.Game.Renderer.Timer.currentFrame

	def resetFrameKey(self):
		self.frameKey = 0
		
	def getFrameKey(self,sequence):
		if self.Game.Renderer.Timer.currentFrame - 3 == self.startFrame:
			self.walk()
			self.resetStartFrame()
			if self.frameKey < len(sequence)-1:
				self.frameKey += 1
			else:
				self.resetFrameKey()
		elif self.Game.Renderer.Timer.currentFrame == self.startFrame or self.frameKey is None:
			self.resetFrameKey()
		return self.frameKey
		
	def getCurrentFrame(self):
		if not self.Game.paused:
			if self.walking:
				state = 'w'
			else:
				state = 's'
				
			sequence = self.directions.get('%s%s' % (self.getDirection(),state))
			if sequence is not None:
				#FIXME: Bugging
				try:
					currentFrame = sequence[self.getFrameKey(sequence)]
				except IndexError:
					currentFrame = sequence[0]
	
			self.currentFrame = currentFrame
		return self.currentFrame

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
		return self.direction
		
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
		
	def pickUp(self,element):
		if self.inRange(element):
			self.Game.currentScene.visibleElements.remove(element)
			self.Game.Inventory.addItem(element)
			if element.pickupMethod is not None:
				element.pickupMethod()
		
	def use(self,element):
		if self.inRange(element) and element.useMethod is not None:
			element.useMethod()
			
	def look(self,element):
		if element.lookMethod is not None:
			element.lookMethod()

	def talk(self,element):
		if self.inRange(element) and element.talkMethod is not None:
			element.talkMethod()
			
	def say(self,text):
		self.Game.Conversation.setText(text)