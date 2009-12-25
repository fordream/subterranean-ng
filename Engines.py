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
        self.screen = pygame.Surface((1024,768))
        self.scene = pygame.Surface((1024,768))
        self.sceneRect = self.scene.get_rect()
        
        self.rect = self.screen.get_rect()
        self.camera = pygame.Rect((0,0),(1024,768))

        self.setupScreen(False)
        self.loadIcon()
        self.loadFonts()
        self.loadGraphics()
        self.setupTimer()
        self.frame = 0
        
        self.fadingOut = False
        
    def translate(self,x):
        x = (self.camera.centerx-self.Game.Player.rect.centerx)
        return x
        
    def translateMouse(self,pos):
        return pos
        #return (self.translate(pos[0]),pos[1])
        
    def transitionFade(self):
        pass
        
    def fadeOut(self):
        print "fading Out"
        if self.fading and self.overlay.get_alpha() < 100:
            self.overlay.set_alpha(self.overlay.get_alpha()+2)
        elif self.fading and self.overlay.get_alpha() > 99:
            self.fading = False
        else:
            self.fading = True
            
    def fadeIn(self):
        print "fading In"
        if self.fading and self.overlay.get_alpha() < 100:
            self.overlay.set_alpha(self.overlay.get_alpha()+2)
        else:
            pass
            
                    
    def setupTimer(self):
        self.Timer = Timer()
        self.Timer.setFPS(24)
        
    def setupScreen(self,fullscreen=False):
        #There seems to be no way to make this work right other than doing this:
        if fullscreen:
            self.window = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
            self.rect.center = self.window.get_rect().center 
        else:
            self.window = pygame.display.set_mode((1024,768))
            self.rect.center = self.window.get_rect().center 
        pygame.display.set_caption('Subterranean')
        
    def loadGraphics(self):
        #self.backgroundImage = pygame.image.load(os.path.join('data','backgrounds','game.png'))
        self.borderImage = pygame.image.load(os.path.join('data','ui','border.png'))
        self.inventoryImage = pygame.image.load(os.path.join('data','ui','inventory.png'))
        self.topicMenuImage = pygame.image.load(os.path.join('data','ui','topicmenu.png'))
        self.debugPoint = pygame.Surface((2,2))
        self.debugPoint.fill((255,0,0))
        self.overlay = pygame.Surface((1024,768))
        self.overlay.fill((0,0,0))
        self.overlay.set_alpha(0)

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
        #Draw game screen
        #Put this somewhere else?
        #self.sceneRect.left = self.translate(self.sceneRect.left)
            
        self.window.blit(self.screen,self.rect)
        self.screen.blit(self.scene,self.sceneRect)
        
        if self.Game.currentScene.visible:
            #Draw current background
            self.scene.blit(self.Game.currentScene.getBackground(),(0,0))
            
            #Draw room objects
            self.Game.currentScene.visibleElements.update()
            self.Game.currentScene.visibleElements.draw(self.scene)
        
            #Draw main character
            self.scene.blit(self.Game.Player.getCurrentFrame(),self.Game.Player.getRenderPos())
            
            #Draw current foreground
            if self.Game.currentScene.getForeground():
                self.scene.blit(self.Game.currentScene.getForeground(),(0,0))
            
        #Draw border
        #self.screen.blit(self.borderImage,(0,0))
            
        #Draw inventory
        self.Game.Inventory.animateHeight()
        self.screen.blit(self.inventoryImage,(0,self.Game.Inventory.y))
        for item in self.Game.Inventory.items:
            if item.current is False:
                self.screen.blit(item.image,item.rect)

        #Topicmenu
        if self.Game.TopicMenu.visible and not self.Game.ScriptManager.isActive():
            self.screen.blit(self.topicMenuImage,self.Game.TopicMenu.rect)
            for topic in self.Game.TopicMenu.topics:
                self.screen.blit(topic.render,topic.pos)
                
        #Window widgets
        if self.Game.currentWindow is not None:
            self.screen.blit(self.Game.currentWindow.background,self.Game.currentWindow.rect)
            for widget in self.Game.currentWindow.widgets:
                self.screen.blit(widget.image,widget.rect)
                
        #Draw element titles
        if self.Game.TitleManager.currentElement is not None and not self.Game.TopicMenu.visible:
            elementTitle = self.elementTitleFont.render(self.Game.TitleManager.getTitle(),1,self.defaultTitleColor)
            self.screen.blit(elementTitle,(self.screen.get_rect().centerx-elementTitle.get_width()/2,710))           
                        
        #Draw dialouge
        if self.Game.ScriptManager.isActive():
            #Load all the script values from the current part
            if not self.Game.ScriptManager.valuesLoaded:
                self.Game.ScriptManager.loadScriptValues(self.Game.ScriptManager.script[0])
            if self.Game.ScriptManager.getCurrentPartType() == 'ScriptConversationPart':
            
                if self.Game.currentWindow is not None:
                    #If we have HUD open, put all dialouge on top of screen
                    posX = 512
                    posY = 50
                else:
                    posX = self.Game.ScriptManager.getTextPos()[0]
                    posY = self.Game.ScriptManager.getTextPos()[1]

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

        #Draw mouse cursor
        self.Game.Cursor.checkCollisions()
        self.screen.blit(self.Game.Cursor.getCursor(),pygame.mouse.get_pos())
            
        #Debug points
        if self.Game.debug:
            if len(self.Game.Player.path) > 1:
                pygame.draw.lines(self.screen, (255,255,255,255), 0, self.Game.Player.path)
            for element in self.Game.currentScene.visibleElements:
                pygame.draw.lines(self.scene,(255,0,255),1,[element.rect.topleft,element.rect.topright,element.rect.bottomright,element.rect.bottomleft])
                if element.actionPos is not None:
                    self.scene.blit(self.debugPoint,element.actionPos)
            self.screen.blit(self.debugPoint,pygame.mouse.get_pos())
            pygame.draw.lines(self.screen,(000,255,255),1,[self.Game.Player.rect.topleft,self.Game.Player.rect.topright,self.Game.Player.rect.bottomright,self.Game.Player.rect.bottomleft])
            for exit in self.Game.currentScene.exits:
                pygame.draw.lines(self.screen,(000,255,255),1,[exit.rect.topleft,exit.rect.topright,exit.rect.bottomright,exit.rect.bottomleft])
                self.scene.blit(self.debugPoint,exit.exitPoint)
            pygame.draw.lines(self.scene,(255,100,255),0,[(0,self.Game.currentScene.farthestPoint),(1024,self.Game.currentScene.farthestPoint)])
            pygame.draw.lines(self.scene,(255,110,24),0,[(0,self.Game.currentScene.closestPoint),(1024,self.Game.currentScene.closestPoint)])
        #Overlay
        if self.fadingOut:
            self.fadeOut()
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
            'AMBI001':os.path.join('data','sound','ambience','ambience001.ogg'),
            'WATER001':os.path.join('data','sound','ambience','water001.ogg')
        }
        
        self.UISounds = {
            'SLIDEIN':os.path.join('data','sound','ui','slidein.ogg'),
            'SLIDEOUT':os.path.join('data','sound','ui','slideout.ogg'),
            'MAP':os.path.join('data','sound','ui','map.ogg'),
        }        
        
        self.speechSounds = {
            'PLAYER001':os.path.join('data','sound','speech','player001.ogg'),
            'PLAYER002':os.path.join('data','sound','speech','player002.ogg'),
            'PLAYER003':os.path.join('data','sound','speech','player003.ogg')
        }

    def playMusic(self,trackName):
        if self.soundEnabled and self.musicEnabled and trackName in self.musicTracks:
            if self.currentMusicTrack is not None and self.currentMusicTrack != trackName:
                pygame.mixer.music.fadeout(0)
            self.currentMusicTrack = trackName
            pygame.mixer.music.load(self.musicTracks.get(trackName))
            pygame.mixer.music.play(-1)
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
        if self.soundEnabled:
            self.playSound(self.ambienceChannel,self.ambienceSounds,soundName,-1)

    def playSpeechSound(self,soundName):
        if self.soundEnabled:
            self.decreaseMusicVolume()
            self.playSound(self.speechChannel,self.speechSounds,soundName)

    def playUISound(self,soundName):
        if self.soundEnabled:
            self.playSound(self.UIChannel,self.UISounds,soundName)
                
    def playSound(self,channel,soundList,soundName,loops=0):
        if self.soundEnabled and soundName in soundList:
            channel.play(pygame.mixer.Sound(soundList.get(soundName)),loops)
        else:
            print "Cound not find sound!:",soundName

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
        pygame.mixer.stop()
        pygame.mixer.music.stop()
        self.soundEnabled = False
        self.musicEnabled = False
        
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
            else:
                if self.Game.TopicMenu.currentTopic:
                    self.Game.TopicMenu.currentTopic.callbackMethod()
                elif self.Game.Cursor.currentElement is not None:
                    pos = self.Game.Cursor.currentElement.getActionPosition()
                    if pos is None:
                        pos = self.Game.Cursor.currentElement.getBasePosition()
                    if self.Game.currentWindow is not None and self.Game.Cursor.currentElement.clickMethod is not None: 
                        self.Game.Cursor.currentElement.clickMethod()
                    elif self.Game.Cursor.currentItem is not None and self.Game.Cursor.currentElement is not None:
                        self.Game.Player.walkTo(pos,self.Game.Player.give,self.Game.Cursor.currentElement)
                    elif self.Game.Cursor.getCursorName() == 'PICKUP':
                        self.Game.Player.walkTo(pos,self.Game.Player.pickUp,self.Game.Cursor.currentElement)
                    elif self.Game.Cursor.getCursorName() == 'USE':
                        self.Game.Player.walkTo(pos,self.Game.Player.use,self.Game.Cursor.currentElement)
                    elif self.Game.Cursor.getCursorName() == 'TALK':
                        self.Game.Player.walkTo(pos,self.Game.Player.talk,self.Game.Cursor.currentElement)
                    elif self.Game.Cursor.getCursorName() == 'LOOK':
                        self.Game.Player.look(self.Game.Cursor.currentElement)
                elif self.Game.Cursor.currentExit is not None:
                    self.Game.Player.walkTo(self.Game.Cursor.currentExit.exitPoint,self.Game.Player.exit,self.Game.Cursor.currentExit)
                else:
                    self.Game.Player.walkTo(pygame.mouse.get_pos())
        else:
            if self.Game.ScriptManager.durationFrames > 0 and self.Game.ScriptManager.currentPartType == 'ScriptConversationPart':
                self.Game.ScriptManager.skip()

    
    def handleRightClick(self,event):
        #Right click cancels.
        if not self.Game.paused and self.Game.Inventory.getCurrentItem() is not None:
                self.Game.Inventory.clearCurrentItem()
        elif self.Game.currentWindow is not None:
            self.Game.currentWindow.hide()
        elif self.Game.currentWindow is not None:
            self.Game.currentWindow.hide()
        
    def handleScrollClick(self,event):
        pass
    
    def handleScrollUp(self,event):
        if self.Game.Cursor.currentElement is not None:
            self.Game.Cursor.scrollCursor(event.button)
    
    def handleScrollDown(self,event):
        if self.Game.Cursor.currentElement is not None:
            self.Game.Cursor.scrollCursor(event.button)
