import os,pygame
import AStar
from time import time

class Player:
	def __init__(self,game):
		self.Game = game
		self.rect = None
		self.visible = False
		self.defaultImage = pygame.image.load(os.path.join('data','maincharacter','ss.png'))
		self.rect = self.defaultImage.get_rect()
		self.pos = (0,0)
		self.walking = False
		
		self.path = []

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

	def walkTo(self,(x,y)):
		if not self.walking:
			if self.findPath(x,y):
				self.walking = True
				self.walk()
				
	def walk(self):
		if len(self.path):
			self.setPosition(self.path[0])
			self.path.pop(0)
		else:
			self.walking = False
		
	def walkToAnd(self,x,y,callbackMethod):
		self.walkTo(x,y)
		while not self.walking:
			print "AS"
			
	def setPosition(self,pos):
		self.rect.move_ip(pos[0],pos[1])
		self.lastPos = self.pos
		self.pos = pos
			
	def getPosition(self):
		return self.pos
		
	def getRenderPosition(self):
		return (self.getX(),self.getY()-215)
		
	def getX(self):
		return self.pos[0]
		
	def getY(self):
		return self.pos[1]