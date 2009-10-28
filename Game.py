import os,pygame
from Constants import *
from Player import Player
from Engines import Renderer,AudioController,EventManager,Timer
from Interfaces import Conversation,Cursor,Inventory,Menu

class Game:
	def __init__(self,arguments):
		self.debug = False;
		self.running = True;
		self.currentScene = None;

		self.Cursor = Cursor(self)
		self.Renderer = Renderer(self)
		self.Inventory = Inventory(self)
		self.AudioController = AudioController(self)
		self.Conversation = Conversation(self)
		self.EventManager = EventManager(self)
		self.Player = Player(self)

		self.loadScene("someScene")
		self.parseArguments(arguments)
		self.run()
		
	def parseArguments(self,arguments):
		avalibleArguments = {
 			'--nomusic':self.AudioController.disableMusic,
			'--nosound':self.AudioController.disableSound,
		}
		
		for argument in avalibleArguments.keys():
			if argument in arguments:
				argumentMethod = avalibleArguments.get(argument)
				argumentMethod()
	
	def loop(self):
		while self.running:
			self.EventManager.checkEvents()
			self.Renderer.Timer.tick()
			self.Renderer.draw()

	def loadScene(self,sceneName):
		from Scenes.Foo import Room
		self.currentScene = Room(self)
		
	def quit(self):
		self.running = False

	def run(self):
		self.loop()
		
	def dump(self):
		if self.debug:
			self.debug = False
		else:
			self.debug = True
		
		print 'Inventory:',self.Inventory.items
		print 'Player position:',self.Player.getPosition()
		print 'Player feet:',self.Player.getRenderPosition()