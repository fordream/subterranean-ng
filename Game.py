#from RenderEnigne
import os,pygame
import Constants
from Player import Player
from Engines import Renderer,AudioController,EventManager,Timer
from Interfaces import Conversation,Cursor,Inventory,Menu

class Game:
	def __init__(self):
		self.running = True;
		self.Cursor = Cursor(self)
		self.Renderer = Renderer(self)
		self.Inventory = Inventory(self)
		self.AudioController = AudioController(self)
		self.Conversation = Conversation(self)
		self.EventManager = EventManager(self)
		
		self.Player = Player(self)


		self.loadScene("someScene")
		self.run()
		
	def loop(self):
		while self.running:
			self.EventManager.checkEvents()
			self.Renderer.Timer.tick()
			self.Renderer.draw()

	def loadScene(self,sceneName):
		from Scenes.Foo import Room
		self.currentRoom = Room()
		
	def quit(self):
		self.running = False

	def run(self):
		self.loop()
