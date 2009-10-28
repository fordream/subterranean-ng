import os
import pygame

class Scene:
	def __init__(self):
		self.visible = False
		self.name = None
		self.mapFileName = None
		self.visibleElements = []
		self.hiddenElements = []
		self.mapData = []
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
		
	def setMap(self,mapFileName):
		self.mapFileName = mapFileName
		self.loadMap(mapFileName)

	def loadMap(self,mapFileName):
		self.mapFile = open(os.path.join('Scenes',mapFileName))
		for line in self.mapFile:
			for char in line.rsplit(','):
				if char == '1' or char == '-1':
					self.mapData.append(int(char))
		self.mapFile.close()