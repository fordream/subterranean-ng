import os,pygame
import AStar
from time import time

class Player:
	def __init__(self,game):
		self.Game = game
		self.rect = None
		self.visible = False
		self.callbackMethod = None
		self.callbackArgument = None
		self.rect = self.loadFrame('north','stand').get_rect()
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
		}
		self.pos = (0,0)
		self.walking = False
		
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
			self.setDirection((x,y))
			if self.findPath(x,y):
				self.walking = True
				self.walk()
			else:
				print "CANT GO THAR"
		
	def walk(self):
		if len(self.path):
			self.setPosition(self.path[0])
			self.path.pop(0)
		else:
			self.walking = False
			if self.callbackMethod is not None:
				self.runCallback()
				
	def runCallback(self):
		self.callbackMethod(self.argument)
		self.callbackMethod = None
		self.callbackArgument = None
		
	def getFrame(self):
		#Todo, fix frames for walking
		#if not self.walking:
		return self.directions.get(self.getDirection()+'s')

	def setPosition(self,pos):
		self.rect.move_ip(pos[0],pos[1])
		self.pos = pos
		
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
		
	def getRenderPosition(self):
		return (self.getX()-self.rect.width/2,self.getY()-self.rect.height+10)
		
	def getX(self):
		return self.pos[0]
		
	def getY(self):
		return self.pos[1]
		
	def inRange(self,element):
		#TODO: Refine this? Currently has a range of 100px
		closenessX = self.getPosition()[0] - element.getPosition()[0]
		closenessY = self.getPosition()[1] - element.getPosition()[1]
		return(closenessX + closenessY < 100 and closenessX + closenessY > -100)
		
	def pickUp(self,item):
		if self.inRange(item):
			self.Game.currentScene.visibleElements.remove(item)
			self.Game.Inventory.addItem(item)
		
	def use(self,widget):
		if self.inRange(widget):
			print "IUSETHIS!"

	def talk(self,person):
		if self.inRange(person):
			print "WHO IS MARCELLUS WALLACE!?"
