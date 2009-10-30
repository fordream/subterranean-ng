import os,pygame
from time import time
import pygame.locals as pygl
	
class Timer:
	def __init__(self):
		pass
		
	def setFPS(self,fps):
		self.currentFrame = 0
		if fps == 0: 
			self.tick = self._blank
			return
		self.wait = 1000/fps
		self.nt = pygame.time.get_ticks()
		pygame.time.wait(0)
	
	def _blank(self):
		pass
	
	def tick(self):
		self.currentTicks = pygame.time.get_ticks()
		if self.currentTicks < self.nt:
			pygame.time.wait(self.nt-self.currentTicks)
			self.nt+=self.wait
		else: 
			self.nt = pygame.time.get_ticks()+self.wait
		self.currentFrame += 1

class Renderer:
	def __init__(self,game):
		self.Game = game
		self.setupScreen()
		self.loadIcon()
		self.loadFonts()
		self.loadCursors()
		self.loadGraphics()
		self.setupTimer()
		self.frame = 0
		
	def setupTimer(self):
		self.Timer = Timer()
		self.Timer.setFPS(32)
		
	def setupScreen(self,fullscreen=False):
		pygame.display.get_surface()
		if fullscreen:
			self.screen = pygame.display.set_mode((1025,768),pygame.FULLSCREEN)
		else:
			self.screen = pygame.display.set_mode((1025,768))
		pygame.display.set_caption('Subterranean')
		
	def loadCursors(self):
		pygame.mouse.set_visible(0)
	   	self.cursors = {
		   	'DEFAULT': pygame.image.load(os.path.join('data','cursors','cursor_default.png')),
		   	'USE': pygame.image.load(os.path.join('data','cursors','cursor_use.png')),
		   	'PICKUP': pygame.image.load(os.path.join('data','cursors','cursor_pickup.png')),
		   	'TALK': pygame.image.load(os.path.join('data','cursors','cursor_talk.png'))
	   	}
		
	def loadGraphics(self):
		self.backgroundImage = pygame.image.load(os.path.join('data','backgrounds','game.png'))
	   	self.debugPoint = pygame.Surface((2,2));
	   	self.debugPoint.fill((255,0,0))

	def loadFonts(self):
		pygame.font.init()
		self.defaultFontColor = (255,255,255)
		self.defaultOutlineFontColor = (0,0,0)
		self.generalFont = pygame.font.Font(os.path.join('data','fonts','prviking.ttf'),20)
		self.elementFont = pygame.font.Font(os.path.join('data','fonts','freesansbold.ttf'),12)
		self.symbolFont = pygame.font.Font(os.path.join('data','fonts','prvikingsymbols.ttf'),18)

	def loadIcon(self):
		pygame.display.set_icon(pygame.image.load(os.path.join('data','icons','gameicon.png')))
		
	def draw(self):
		#Draw game background
		self.screen.blit(self.backgroundImage,(0,0))

		if self.Game.currentScene.visible:
			#Draw current background
			self.screen.blit(self.Game.currentScene.getBackground(),(0,0))
			
			#Draw room objects
			for element in self.Game.currentScene.visibleElements:
				self.screen.blit(element.image,element.getPosition())
				text = self.elementFont.render(element.title,1,self.defaultFontColor)
				self.screen.blit(text,element.getBasePosition())
		
			#Draw main character
			self.screen.blit(self.Game.Player.getCurrentFrame(),self.Game.Player.getRenderPos())
		
		#Draw conversations
		if self.Game.Conversation.isActive:
			s = time()
			#THIS IS ONLY FOR TESTING ATM. WILL BE DYNAMIC LATER OF COURSE
			posX = 50
			posY = 700
			
			text = self.generalFont.render(self.Game.Conversation.currentText,1,self.defaultFontColor)
			textOutline = self.generalFont.render(self.Game.Conversation.currentText,1,self.defaultOutlineFontColor)
			
			self.screen.blit(textOutline,(posX,posY-1))
			self.screen.blit(textOutline,(posX+1,posY))
			self.screen.blit(textOutline,(posX-1,posY))
			self.screen.blit(textOutline,(posX,posY+1))
			self.screen.blit(text,(posX,posY))

		#Draw mouse cursor
		self.Game.Cursor.checkCollisions()
		self.screen.blit(self.cursors.get(self.Game.Cursor.cursor),pygame.mouse.get_pos())
    		
    		
		if self.Game.debug:
			if len(self.Game.Player.path) > 1:
				pygame.draw.lines(self.screen, (255,255,255,255), 0, self.Game.Player.path)
			for element in self.Game.currentScene.visibleElements:
				pygame.draw.lines(self.screen,(255,0,255),1,[element.rect.topleft,element.rect.topright,element.rect.bottomright,element.rect.bottomleft])
			self.screen.blit(self.debugPoint,pygame.mouse.get_pos())
			pygame.draw.lines(self.screen,(000,255,255),1,[self.Game.Player.rect.topleft,self.Game.Player.rect.topright,self.Game.Player.rect.bottomright,self.Game.Player.rect.bottomleft])

		pygame.display.flip()
		e = time()
	    
class AudioController:

	def __init__(self,game):
		pygame.mixer.init()
		self.soundEnabled = True
		self.musicEnabled = True
		self.musicState = None
		self.musicVolume= None
		self.currentMusicTrack = None
		self.ambienceChannel = pygame.mixer.Channel(2)
		self.currentAmbienceTrack = None		
		self.speechChannel = pygame.mixer.Channel(3)
		self.musicTracks = {
			'FOO':os.path.join('data','music','default.ogg')
		}
		self.ambienceTracks = {
			
		}
		self.playMusic('FOO')

	def playMusic(self,trackName):
		if self.musicEnabled and trackName in self.musicTracks:
			if self.currentMusicTrack is not None and self.currentMusicTrack != trackName:
				pygame.mixer.music.fadeout(1500)
				pygame.mixer.music.stop()
			self.currentMusicTrack = trackName
			pygame.mixer.music.load(self.musicTracks.get(trackName))
			pygame.mixer.music.play()
			self.musicState = 'unpaused'
			self.musicVolume= 'normal'

	def stopMusic(self):
		pygame.mixer.music.stop()
		
	def toggleMusicVolume(self):
		if self.musicVolume == 'normal':
			self.decreaseMusicVolume()
		else:
			self.restoreMusicVolume()
		
	def decreaseMusicVolume(self):
		pygame.mixer.music.set_volume(0.2)
		self.musicVolume = 'decreased'
		
	def restoreMusicVolume(self):
		pygame.mixer.music.set_volume(1.0)
		self.musicVolume = 'normal'
		
	def toggleMusicPause(self):
		if self.musicState == 'unpaused':
			self.pauseMusic()
		else:
			self.unpauseMusic()
		
	def pauseMusic(self):
		pygame.mixer.music.pause()
		self.musicState = 'paused'
		
	def unpauseMusic(self):
		pygame.mixer.music.unpause()
		self.musicState = 'unpaused'
	
	def playAmbience(self):
		pass
		
	def stopSound(self):
		pass
		
	def enableMusic(self):
		self.musicEnabled = True

	def disableMusic(self):
		self.stopMusic()
		self.musicEnabled = False
		
	def enableSound(self):
		self.soundEnabled = True

	def disableSound(self):
		self.stopMusic()
		self.stopSound()
		self.soundEnabled = False
		
class EventManager:
	def __init__(self,game):
		self.Game = game
		self.eventSignals = {pygl.QUIT: self.Game.quit,
							pygl.KEYDOWN: self.readKey,
							pygl.MOUSEBUTTONDOWN: self.readMouseClick}
							
		self.keySignals = {pygl.K_q: self.Game.quit,
							pygl.K_ESCAPE: self.Game.quit,
							pygl.K_m: self.Game.AudioController.toggleMusicPause,
							pygl.K_l: self.Game.AudioController.toggleMusicVolume,
							pygl.K_d: self.Game.dump
							}
							
		self.mouseSignals = {1: self.Game.quit}
		
		
	def checkEvents(self):
		for event in pygame.event.get():
			eventMethod = self.eventSignals.get(event.type)
			if eventMethod is not None:
				eventMethod(event)
							
	def readKey(self,event):
		eventMethod = self.keySignals.get(event.key)
		if eventMethod is not None:
			eventMethod()

	def readMouseClick(self,event):
		if self.Game.Cursor.currentElement is not None:
			pos = self.Game.Cursor.currentElement.getBasePosition()
			if self.Game.Cursor.currentElement.retrievable:
				self.Game.Player.walkTo(pos,self.Game.Player.pickUp,self.Game.Cursor.currentElement)
			elif self.Game.Cursor.currentElement.usable:
				self.Game.Player.walkTo(pos,self.Game.Player.use,self.Game.Cursor.currentElement)
			elif self.Game.Cursor.currentElement.isCharacter:
				self.Game.Player.walkTo(pos,self.Game.Player.talk,self.Game.Cursor.currentElement)
			else:
				print self.Game.Cursor.currentElement.debugMessage
		else:
			self.Game.Player.walkTo(pygame.mouse.get_pos())