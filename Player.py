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
		self.x = 0
		self.y = 0
		self.destinationX = 0
		self.destinationY = 0
		self.moving = False
		
		self.path = []
		self.mapdata = []
		size = 64*48;
		for i in range(size):
			self.mapdata.append(1)

	def walkTo(self,(x,y)):
	
		sx = self.x/16
		sy = self.y/16
		
		ex = x/16
		ey = y/16
		
		astar = AStar.AStar(AStar.SQ_MapHandler(self.mapdata,64,48))
		start = AStar.SQ_Location(sx,sy)
		end = AStar.SQ_Location(ex,ey)
		s = time()
		p = astar.findPath(start,end)
		e = time()
		print "Found path in %d moves and %f seconds." % (len(p.nodes),(e-s))
		self.path = []
		self.path.append((start.x*16+8,start.y*16+8))
		for n in p.nodes:
			self.path.append((n.location.x*16+8,n.location.y*16+8))
		self.path.append((end.x*16+8,end.y*16+8))
		
		self.x = x
		self.y = y
		self.rect.move_ip(x,y)
		
		print self.path
		self.step()
	
	def step(self):
		if len(self.path):
			print self.path[0]
			