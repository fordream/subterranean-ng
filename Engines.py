# -*- coding: utf-8 -*-
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
        self.setupScreen(False)
        self.loadIcon()
        self.loadFonts()
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
        
    def loadGraphics(self):
        #self.backgroundImage = pygame.image.load(os.path.join('data','backgrounds','game.png'))
        self.borderImage = pygame.image.load(os.path.join('data','ui','border.png'))
        self.inventoryImage = pygame.image.load(os.path.join('data','ui','inventory.png'))
        self.topicMenuImage = pygame.image.load(os.path.join('data','ui','topicmenu.png'))
        self.debugPoint = pygame.Surface((2,2));
        self.debugPoint.fill((255,0,0))

    def loadFonts(self):
        pygame.font.init()
        self.defaultFontColor = (255,255,255)
        self.defaultTitleColor = (239,240,173)
        self.defaultOutlineFontColor = (0,0,0)
        self.generalFont = pygame.font.Font(os.path.join('data','fonts','HVD_Edding.otf'),26)
        self.topicMenuFont = pygame.font.Font(os.path.join('data','fonts','HVD_Edding.otf'),24)
        self.elementTitleFont = pygame.font.Font(os.path.join('data','fonts','HVD_Edding.otf'),26)

    def loadIcon(self):
        pygame.display.set_icon(pygame.image.load(os.path.join('data','icons','gameicon.png')))
        
    def draw(self):
        pygame.mouse.set_visible(0)
        #Draw game background
        #self.screen.blit(self.backgroundImage,(0,0))

        if self.Game.currentScene.visible:
            #Draw current background
            self.screen.blit(self.Game.currentScene.getBackground(),(0,0))
            
            #Draw room objects
            self.Game.currentScene.visibleElements.update()
            self.Game.currentScene.visibleElements.draw(self.screen)
        
            #Draw main character
            self.screen.blit(self.Game.Player.getCurrentFrame(),self.Game.Player.getRenderPos())

        #Draw element titles
        if self.Game.TitleManager.currentElement is not None:
            elementTitle = self.elementTitleFont.render(self.Game.TitleManager.getTitle(),1,self.defaultTitleColor)
            self.screen.blit(elementTitle,(self.screen.get_rect().centerx-elementTitle.get_width()/2,710))           
            
        #Draw dialouge
        if self.Game.ScriptManager.isActive():
            #Load all the script values from the current part
            if not self.Game.ScriptManager.valuesLoaded:
                self.Game.ScriptManager.loadScriptValues(self.Game.ScriptManager.script[0])
            if self.Game.ScriptManager.getCurrentPartType() == 'ScriptConversationPart':
            
                posX = self.Game.ScriptManager.getTextPos()[0];
                posY = self.Game.ScriptManager.getTextPos()[1];
                words = self.Game.ScriptManager.getText().split(' ')
                lines = []
                    
                while len(words):
                    currentLine = ""
                    for word in words[0:7]:
                        currentLine += " "+word
                    lines.append(currentLine)
                    del words[0:7]
                
                lines.reverse()
                for line in lines:
                    lineRender = self.generalFont.render(line,1,self.Game.ScriptManager.currentColor)
                    lineShadow = self.generalFont.render(line,1,self.defaultOutlineFontColor)
                    lineX = posX-lineRender.get_width()/2
                    #Handling for text that goes outside the screen
                    if lineX+lineRender.get_width() > 1000:
                        lineX -= (lineX+lineRender.get_width())-1000
                    self.screen.blit(lineShadow,(lineX,posY-2))
                    self.screen.blit(lineShadow,(lineX+2,posY))
                    self.screen.blit(lineShadow,(lineX-2,posY))
                    self.screen.blit(lineShadow,(lineX,posY+2))
                    self.screen.blit(lineRender,(lineX,posY))
                    posY -= 30                
                
            elif self.Game.ScriptManager.getCurrentPartType() == 'ScriptWalkPart':
                self.Game.ScriptManager.runScriptetWalk()
            self.Game.ScriptManager.loop()
            
        #Draw border
        self.screen.blit(self.borderImage,(0,0))

            
        #Draw inventory
        self.Game.Inventory.animateHeight()
        self.screen.blit(self.inventoryImage,(0,self.Game.Inventory.y))
        for item in self.Game.Inventory.items:
            if item.current is False:
                self.screen.blit(item.image,item.rect)

        #Topicmenu
        if self.Game.TopicMenu.visible:
            self.screen.blit(self.topicMenuImage,self.Game.TopicMenu.rect)
            for topic in self.Game.TopicMenu.topics:
                self.screen.blit(topic.render,topic.pos)
                

        #Draw mouse cursor
        self.Game.Cursor.checkCollisions()
        self.screen.blit(self.Game.Cursor.getCursor(),pygame.mouse.get_pos())
            
        if self.Game.debug:
            if len(self.Game.Player.path) > 1:
                pygame.draw.lines(self.screen, (255,255,255,255), 0, self.Game.Player.path)
            for element in self.Game.currentScene.visibleElements:
                pygame.draw.lines(self.screen,(255,0,255),1,[element.rect.topleft,element.rect.topright,element.rect.bottomright,element.rect.bottomleft])
            self.screen.blit(self.debugPoint,pygame.mouse.get_pos())
            pygame.draw.lines(self.screen,(000,255,255),1,[self.Game.Player.rect.topleft,self.Game.Player.rect.topright,self.Game.Player.rect.bottomright,self.Game.Player.rect.bottomleft])

        pygame.display.flip()
        
class AudioController:

    def __init__(self,game):
        try:
            pygame.mixer.init(44100)
        except:
            self.soundEnabled = False
            self.musicEnabled = False
            return
        self.soundEnabled = True
        self.musicEnabled = True
        self.musicState = None
        self.musicVolume= None
        self.currentMusicTrack = None
        self.currentSound = None
        self.ambienceChannel = pygame.mixer.Channel(1)
        self.speechChannel = pygame.mixer.Channel(2)
        self.UIChannel = pygame.mixer.Channel(3)
        try:
            self.musicTracks = {
                'DEFAULT':os.path.join('data','music','default.ogg'),
                'THEME':os.path.join('data','music','theme.ogg'),
                'NOTEXPECTED':os.path.join('data','music','notexpected.ogg')
            }
        except:
            self.musicTracks = {}

        self.ambienceSounds = {
            'AMBI001':os.path.join('data','sound','ambience','ambience001.ogg')
        }
        
        self.UISounds = {
            'SLIDEIN':os.path.join('data','sound','ui','slidein.ogg'),
            'SLIDEOUT':os.path.join('data','sound','ui','slideout.ogg')
        }        
        
        self.speechSounds = {
            'PLAYER001':os.path.join('data','sound','speech','player001.ogg'),
            'PLAYER002':os.path.join('data','sound','speech','player002.ogg'),
            'PLAYER003':os.path.join('data','sound','speech','player003.ogg')
        }
        self.playMusic('THEME')

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
        pygame.mixer.music.set_volume(0.5)
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
    
    def playAmbienceSound(self,soundName):
        self.playSound(self.ambienceChannel,self.ambienceSounds,soundName,-1)
        print "Started ambience sound"

    def playSpeechSound(self,soundName):
        self.decreaseMusicVolume()
        self.playSound(self.speechChannel,self.speechSounds,soundName)

    def playUISound(self,soundName):
        self.playSound(self.UIChannel,self.UISounds,soundName)
                
    def playSound(self,channel,soundList,soundName,loops=0):
        if self.soundEnabled and soundName in soundList:
            channel.play(pygame.mixer.Sound(soundList.get(soundName)),loops)
        else:
            print "Cound not find sound!"

    def stopSpeech(self):
        self.stopSound(self.speechChannel)

    def stopAmbience(self):
        self.stopSound(self.ambienceChannel)
        
    def stopSound(self,channel):
        if channel.get_busy():
            channel.stop()
        
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
                            pygl.MOUSEBUTTONDOWN: self.readMouseClick,
                            pygl.MOUSEMOTION: self.readMousePos}
                            
        self.keySignals = {pygl.K_q: self.Game.quit,
                            pygl.K_ESCAPE: self.Game.quit,
                            pygl.K_m: self.Game.AudioController.toggleMusicPause,
                            pygl.K_l: self.Game.AudioController.toggleMusicVolume,
                            pygl.K_d: self.Game.dump,
                            pygl.K_f: self.Game.toggleFullscreen,
                            pygl.K_t: self.Game.Player.randomTalk
                            }
                            
        self.mouseSignals = {1: self.handleLeftClick,
                            2: self.handleScrollClick,
                            3: self.handleRightClick,
                            4: self.handleScrollDown,
                            5: self.handleScrollUp
                            }
                            
    def checkEvents(self):
        for event in pygame.event.get():
            eventMethod = self.eventSignals.get(event.type)
            if eventMethod is not None:
                eventMethod(event)
                            
    def readKey(self,event):
        eventMethod = self.keySignals.get(event.key)
        if eventMethod is not None:
            eventMethod()
            
    def readMousePos(self,event):
        if not self.Game.paused:
            if event.pos[1] < 50 and self.Game.Inventory.visible is False:
                self.Game.Inventory.show()
            elif event.pos[1] > 50 and self.Game.Inventory.visible:
                self.Game.Inventory.hide()
        else:
            #Hide the inventory if the game is paused.
            self.Game.Inventory.hide()
        
    def readMouseClick(self,event):
        eventMethod = self.mouseSignals.get(event.button)
        if eventMethod is not None:
            eventMethod(event)
            
    def handleLeftClick(self,event):
        if not self.Game.paused:
            if pygame.mouse.get_pos()[1] < 70:
                if self.Game.Cursor.currentItem is not None and self.Game.Inventory.currentItem is None:
                    self.Game.Inventory.setCurrentItem(self.Game.Cursor.currentItem)
                elif self.Game.Cursor.currentItem is not None and self.Game.Inventory.currentItem is not None and self.Game.Cursor.currentItem.current is False:
                    self.Game.Cursor.currentItem.combine(self.Game.Inventory.currentItem)
                else:
                    self.Game.Inventory.clearCurrentItem()
            elif pygame.mouse.get_pos()[1] > 660:
                if self.Game.TopicMenu.currentTopic:
                    self.Game.TopicMenu.currentTopic.callbackMethod()            
            else:
                if self.Game.Cursor.currentElement is not None:
                    pos = self.Game.Cursor.currentElement.getActionPosition()
                    if pos is None:
                        pos = self.Game.Cursor.currentElement.getBasePosition()
                    if self.Game.Cursor.currentItem is not None and self.Game.Cursor.currentElement is not None:
                        self.Game.Player.walkTo(pos,self.Game.Player.give,self.Game.Cursor.currentElement)
                    elif self.Game.Cursor.getCursorName() == 'PICKUP':
                        self.Game.Player.walkTo(pos,self.Game.Player.pickUp,self.Game.Cursor.currentElement)
                    elif self.Game.Cursor.getCursorName() == 'USE':
                        self.Game.Player.walkTo(pos,self.Game.Player.use,self.Game.Cursor.currentElement)
                    elif self.Game.Cursor.getCursorName() == 'TALK':
                        self.Game.Player.walkTo(pos,self.Game.Player.talk,self.Game.Cursor.currentElement)
                    elif self.Game.Cursor.getCursorName() == 'LOOK':
                        self.Game.Player.look(self.Game.Cursor.currentElement)
                else:
                    self.Game.Player.walkTo(pygame.mouse.get_pos())
        else:
            if self.Game.ScriptManager.durationFrames > 0 and self.Game.ScriptManager.currentPartType == 'ScriptConversationPart':
                self.Game.ScriptManager.skip()

    
    def handleRightClick(self,event):
        if not self.Game.paused and self.Game.Inventory.getCurrentItem() is not None:
                self.Game.Inventory.clearCurrentItem()
        
    def handleScrollClick(self,event):
        pass
    
    def handleScrollUp(self,event):
        if self.Game.Cursor.currentElement is not None:
            self.Game.Cursor.scrollCursor(event.button)
    
    def handleScrollDown(self,event):
        if self.Game.Cursor.currentElement is not None:
            self.Game.Cursor.scrollCursor(event.button)
