import os
import pygame

class Scene:
	def __init__(self):
		self.visible = False
		self.name = None
		self.visibleElements = []
		self.hiddenElements = []
		self.insertPoint = ()

	def getName(self,sceneName):
		self.name = sceneName
		
	def getName(self):
		return self.name
		
	def getBackground(self):
		return self.backgroundImage
		
	def setBackground(self,backgroundImage):
		self.backgroundImage = pygame.image.load(os.path.join('data','backgrounds',backgroundImage)).convert()
		
	def addVisibleElement(self,element):
		self.visibleElements.append(element)
		
	def setInsertPoint(self,pos):
		self.insertPoint = pos

	def show(self):
		self.visible = True
