import os,pygame

class Player:
	def __init__(self,game):
		self.Game = game
		self.rect = None
		self.visible = False
		self.defaultImage = pygame.image.load(os.path.join('data','maincharacter','ss.png'))
		self.x = 0
		self.y = 0
		self.destinationX = 0
		self.destinationY = 0
		self.moving = False

	def walkTo(self,(x,y)):
		self.destinationX = x
		self.destinationY = y
		print "I WANNA WALK TO THIS PLACE"
		print x,y
		
	def step():
		