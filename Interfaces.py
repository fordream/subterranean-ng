# -*- coding: utf-8 -*-
import os,pygame
from Elements import Item

class Inventory:
    def __init__(self,game):
        self.Game = game
        self.currentItem = None
        self.items = []
        self.visible = False
        self.surface = pygame.Surface((1024,68))
        self.rect = self.surface.get_rect()
        self.surface.fill((25,25,25),self.rect)
        self.surface.set_alpha(145)
        self.animating = False
        self.y = -80
        self.spacing = 20

    def addItem(self,item,runEffect=True):
        #Need game reference to talk to Inventory later
        item.Game = self.Game
        self.items.append(item)
        if not self.visible:
            self.hideItems()
        self.arrangeItems()
        
    def removeItem(self,item):
        self.items.remove(item)

    def removeItemFromName(self,itemName):
        self.items.remove(self.getItemFromName(itemName))

    def getItemFromName(self,name):
        for item in self.items:
            if item.name == name:
                return item
        return False

    def itemExists(self,name):
        for item in self.items:
            if item.name == name:
                return True
        return False

    def combineItems(self,firstElement,secondElement,resultElement):
        self.clearCurrentItem()
        self.removeItem(firstElement)
        self.removeItem(secondElement)
        self.addItem(resultElement,False)
                
    def arrangeItems(self):
        number = 0
        for item in self.items:
            if item.current is False:
                item.setX(number*60+self.spacing)
                number += 1
            else:
                item.setX(-100)
                                                
    def show(self):
        if not self.visible:
            self.visible = True
            self.animating = True
            self.Game.AudioController.playUISound('SLIDEIN')

    def hide(self):
        if self.visible:
            self.visible = False
            self.animating = True
            self.Game.AudioController.playUISound('SLIDEOUT')

    def hideItems(self):
        for item in self.items:
            item.setY(-80)
            
    def setCurrentItem(self,item):
        if self.currentItem is None:
            self.currentItem = item
            self.currentItem.current = True
            self.arrangeItems()
            
    def getCurrentItem(self):
        return self.currentItem
        
    def clearCurrentItem(self):
        self.Game.TitleManager.clearElement()
        self.Game.Cursor.currentItem = None
        self.currentItem.current = False
        self.currentItem = None
        self.arrangeItems()
                    
    def animateHeight(self):
        if self.animating:
            if self.visible and self.y < 10:
                self.y+=10
                for item in self.items:
                    item.setY(self.y+10)
            elif not self.visible and self.y > -80:
                self.y-=10
                for item in self.items:
                    item.setY(self.y+10)
            else:
                self.animating = False
        
    def toggle(self):
        if self.visible:
            self.hide()
        else:
            self.show()
            
class TitleManager:
    def __init__(self,game):
        self.Game = game
        self.prefix = ''
        self.suffix = ''
        self.currentElement = None
        self.prefixes = {
            'USE':'Use',    
            'PICKUP':'Pick up',
            'TALK':'Talk to',
            'LOOK':'Look at',
            'GIVE':'Give',
            'COMBINE':'Combine'
        }

        self.suffixes = {
            'WITH':'with',    
            'TO':'to'
        }
        
    def setPrefix(self,prefix=None):
        if prefix in self.prefixes:
            self.prefix = self.prefixes.get(prefix)
        else:
            self.prefix = ''

    def setSuffix(self,suffix=None):
        if suffix in self.suffixes:
            self.suffix = self.suffixes.get(suffix)
        else:
            self.suffix = ''
                    
    def setElement(self,element):
        self.currentElement = element

    def clearElement(self):
        self.currentElement = None
        self.prefix = ''
        
    def getTitle(self):
        if not self.Game.paused and self.currentElement is not None:
            if self.prefix == 'Combine' or self.prefix == 'Give':
                return '%s %s %s %s' % (self.prefix,self.Game.Inventory.currentItem.title,self.suffix,self.currentElement.title)
            else:
                return '%s %s' % (self.prefix,self.currentElement.title)
                        
class TopicMenu:
    def __init__(self,game):
        self.Game = game
        self.visible = False
        self.rect = pygame.Rect(0,668,1024,100)
        self.topics = []
        self.currentTopic = None
        
    def loadCharacterTopics(self,character):
        self.clearTopics()
        self.topics = character.topics
        self.arrangeTopics()
        
    def arrangeTopics(self):
        currentY = 720
        currentX = 25
        for topic in self.topics:
            if currentX + topic.render.get_width() < 1024:
                topic.setPos((currentX,currentY))
                currentX += topic.render.get_width()+25
            else:
                currentY -= 35
                currentX = 25
                topic.setPos((currentX,currentY))
                currentX += topic.render.get_width()+25

    def setCurrentTopic(self,topic):
        self.currentTopic = topic
        topic.setActive()
    
    def clearCurrentTopic(self):
        self.currentTopic = None
        for topic in self.topics:
            topic.clearActive()
            
    def getCurrentTopic(self):
        return self.currentTopic
        
    def clearTopics(self):
        self.topics = []
                        
    def show(self):
        self.visible = True
        
    def hide(self):
        self.visible = False
        self.clearTopics()
    
class ScriptConversationPart:
    def __init__(self,actor,text,speech=None):
        self.actor = actor
        self.text = text
        self.speech = speech
        
    def getType(self):
        return self.__class__.__name__

class ScriptWalkPart:
    def __init__(self,actor,walkPos):
        self.actor = actor
        self.walkPos = walkPos

    def getType(self):
        return self.__class__.__name__

class ScriptSequencePart:
    def __init__(self,actor,sequenceName):
        self.actor = actor
        self.sequenceName = sequenceName

    def getType(self):
        return self.__class__.__name__

class ScriptMethodPart:
    def __init__(self,method,args):
        self.method = method
        self.args = args

    def getType(self):
        return self.__class__.__name__
                           
class ScriptManager:
    def __init__(self,game):
        self.Game = game
        self.startFrame = None
        #Frames for each part
        self.durationFrames = 100
        self.script = []
        #The values that are populated by each part        
        self.currentColor = None
        self.textPos = None
        self.walkPos = None
        self.method = None
        self.currentPartType = None
        self.valuesLoaded = False
        self.skipped = False
        
    def skip(self):
        self.skipped = True
        
    def setColor(self,color):
        self.currentColor = color
        
    def setDurationFrames(self,part):
        if part.getType() == 'ScriptConversationPart':
            if part.speech is not None:
                #If there is a sound, calculate the frames from it
                tmpSound = pygame.mixer.Sound(self.Game.AudioController.speechSounds.get(part.speech))
                self.durationFrames = int(tmpSound.get_length()*32)
            else:
                #If not, calculate from the text.
                #TODO: Calibrate
                self.durationFrames = int(round(len(part.text) * 1.9))
        elif part.getType == 'ScriptWalkPart':
            #Calculate frames from path length
            #TODO: Calculate this
            self.durationFrames = 100
        else:
            #Default
            self.durationFrames = 100
                
    def isActive(self):
        return len(self.script) > 0

    def setSpeaker(self,speaker):
        self.speaker = speaker

    def getSpeaker(self):
        return self.speaker
                
    def setTextPos(self,pos):
        self.textPos = pos

    def getTextPos(self):
        return self.textPos

    #Only getters because they are created in the Script*Part class        
    def getText(self):
        if self.startFrame is None:
            self.loadScriptValues(self.script[0])
        return self.script[0].text

    def getActor(self):
        return self.script[0].actor

    def getWalkPos(self):
        return self.script[0].walkPos

    def addConversationPart(self,actor,text,speech):
        self.script.append(ScriptConversationPart(actor,text,speech))

    def addWalkPart(self,actor,endPos):
        self.script.append(ScriptWalkPart(actor,endPos))

    def addSequencePart(self,actor,sequenceName):
        self.script.append(ScriptSequencePart(actor,sequenceName))

    def addMethodPart(self,method,args):
        self.script.append(ScriptMethodPart(method,args))
        
    def resetStartFrame(self):
        self.startFrame = self.Game.Renderer.Timer.currentFrame
        
    def getCurrentPartType(self):
        return self.script[0].__class__.__name__            
    
    #The loop is called after the current part has been executed.    
    def loop(self):
        if self.startFrame is None:
            #Start
            self.resetStartFrame()
            self.Game.pause()
        elif self.Game.Renderer.Timer.currentFrame - self.durationFrames == self.startFrame or self.skipped:
            #After each part is done or skipped
            self.Game.AudioController.stopSpeech()
            self.skipped = False
            self.script.pop(0)
            self.resetStartFrame()
            if not len(self.script):
                #End
                self.Game.AudioController.restoreMusicVolume()
                self.resetScriptValues()
                self.Game.unpause()
            else:
                #Load the part values
                self.loadScriptValues(self.script[0])

        if self.Game.Renderer.Timer.currentFrame == self.startFrame:
            #Every part
            if self.script[0].__class__.__name__ == 'ScriptConversationPart' and self.script[0].speech is not None:
                self.Game.AudioController.decreaseMusicVolume()
                self.Game.AudioController.playSpeechSound(self.script[0].speech)

                        
    def loadScriptValues(self,scriptPart):
        self.currentPartType = self.getCurrentPartType()
        #Determine what kind of part it is:
        if self.currentPartType == 'ScriptConversationPart':
            self.setColor(scriptPart.actor.getTextColor())
            self.setTextPos(scriptPart.actor.getTextPos())
        self.setDurationFrames(scriptPart)
        self.valuesLoaded = True
        
    def runScriptetWalk(self):
        if not self.getActor().walking:
            self.getActor().walkTo(self.getWalkPos())
        
    def resetScriptValues(self):
        self.durationFrames = 50
        self.setColor((255,255,255))
        self.setTextPos((0,0))
        self.valuesLoaded = False
        self.startFrame = None
                    
class Cursor():
    def __init__(self,game):
        self.Game = game
        self.currentElement = None;
        self.currentItem = None
        self.cursorName = None
        self.currentCursor = None

        self.cursors = {
            'DEFAULT': pygame.image.load(os.path.join('data','cursors','cursor_default.png')),
            'USE': pygame.image.load(os.path.join('data','cursors','cursor_use.png')),
            'PICKUP': pygame.image.load(os.path.join('data','cursors','cursor_pickup.png')),
            'LOOK': pygame.image.load(os.path.join('data','cursors','cursor_look.png')),
            'TALK': pygame.image.load(os.path.join('data','cursors','cursor_talk.png'))
        }
        
        #Keep these here so we don't loop over it while scrolling.
        self.pausedCursor = pygame.image.load(os.path.join('data','cursors','cursor_paused.png'))
        self.exitCursors = {
            'EXIT_NORTH': pygame.image.load(os.path.join('data','cursors','cursor_exit_north.png')),
            'EXIT_EAST': pygame.image.load(os.path.join('data','cursors','cursor_exit_east.png')),
            'EXIT_SOUTH': pygame.image.load(os.path.join('data','cursors','cursor_exit_south.png')),
            'EXIT_WEST': pygame.image.load(os.path.join('data','cursors','cursor_exit_west.png'))

        }
        self.setCursor('DEFAULT')
     
    def setCursor(self,cursorName):
        #TODO: Make this prettier 
        if cursorName in self.cursors:
            self.cursorName = cursorName
            self.currentCursor = self.cursors[cursorName]
        elif cursorName in self.exitCursors:
            self.cursorName = cursorName
            self.currentCursor = self.exitCursors[cursorName]
            
    def getCursor(self):
        if self.Game.paused:
            return self.pausedCursor
        elif self.Game.Inventory.currentItem is not None:
            return self.Game.Inventory.currentItem.image
        else:
            return self.currentCursor
            
    def getCursorName(self):
        return self.cursorName
        
    def nextCursor(self):
        keys = self.cursors.keys()
        cursorIndex = keys.index(self.cursorName)
        if cursorIndex < len(self.cursors)-1:
            self.setCursor(keys[cursorIndex + 1])
        else:
            self.setCursor("USE")

    def previousCursor(self):
        keys = self.cursors.keys()
        cursorIndex = keys.index(self.cursorName)
        if cursorIndex >  1:
            self.setCursor(keys[cursorIndex - 1])
        else:
            self.setCursor(keys[-1])
                                
    def scrollCursor(self,direction):
        if direction == 4:
            self.setCursor(self.nextCursor())
        else:
            self.setCursor(self.previousCursor())
            
    def checkCollisions(self):
        if pygame.mouse.get_pos()[1] < 80:
                for item in self.Game.Inventory.items:
                    if(item.rect.collidepoint(pygame.mouse.get_pos())):
                        if self.Game.Inventory.currentItem is not None and item.current is False:
                            self.Game.TitleManager.setElement(item)
                            self.Game.TitleManager.setPrefix('COMBINE')
                            self.Game.TitleManager.setSuffix('WITH')
                            self.currentItem = item
                            return item
                        elif(item.rect.collidepoint(pygame.mouse.get_pos())):
                            self.Game.TitleManager.setElement(item)
                            self.setCursor('USE')
                            self.currentItem = item
                            return item
        elif pygame.mouse.get_pos()[1] > 660 and self.Game.TopicMenu.visible:
            self.Game.TopicMenu.clearCurrentTopic()
            for topic in self.Game.TopicMenu.topics:
                if(topic.rect.collidepoint(pygame.mouse.get_pos())):
                    self.Game.TopicMenu.setCurrentTopic(topic)
        elif pygame.mouse.get_pos()[1] < 660 and self.Game.TopicMenu.visible:
            self.Game.TopicMenu.clearCurrentTopic()
        else:
            if self.Game.currentWindow is not None:
                for widget in self.Game.currentWindow.widgets:
                    if(widget.rect.collidepoint(pygame.mouse.get_pos())):
                        self.Game.TitleManager.setElement(widget)
                        self.currentElement = widget
                        self.setCursor('USE')
                        return self.currentElement
            else:
                for element in self.Game.currentScene.visibleElements:
                    #Calculate center for item cursor to avoid pixel hunting.
                    #Also set the prefix correctly.
                    #TODO: Make this loop smarter. Really.
                    if self.Game.Cursor.currentItem is not None:
                        mouse = pygame.mouse.get_pos()
                        pos = (mouse[0]+24,mouse[1]+24)
                    else:
                        pos = pygame.mouse.get_pos()
                    if(element.rect.collidepoint(pos)):
                        self.Game.TitleManager.setElement(element)
                        self.currentElement = element
                        if self.Game.Inventory.currentItem is not None:
                            self.Game.TitleManager.setPrefix('GIVE')
                            self.Game.TitleManager.setSuffix('TO')
                        else:
                            self.Game.TitleManager.setPrefix(self.getCursorName())
                        if self.getCursorName() == 'DEFAULT':
                            self.setCursor('USE')
                        return self.currentElement
                
                #Last resorts, are there any exits here?
                for exit in self.Game.currentScene.exits:
                    if(exit.rect.collidepoint(pygame.mouse.get_pos())):
                        self.setCursor('EXIT_'+exit.direction)
                        self.currentExit = exit
                        return self.currentExit

        self.Game.TitleManager.clearElement()
        self.setCursor('DEFAULT')
        self.currentElement = None;
        self.currentExit = None
        
class ElementWindow:
    def __init__(self,game):
        self.Game = game
        self.background = None
        self.rect = None
        self.widgets = []
        self.openMethod = None
        self.closeMethod = None
        
    def setBackground(self,background):
        self.background = pygame.image.load(os.path.join('data','windows',background))
        self.rect = self.background.get_rect()
        self.align()
        
    def align(self):
        self.rect.left = (1024-self.rect.w)/2
        self.rect.top = (768-self.rect.h)/2
        
    def show(self):
        self.Game.currentWindow = self
        self.runOpenMethod()
        
    def hide(self):
        self.Game.currentWindow = None
        self.runCloseMethod()

    def addWidget(self,widget):
        widget.setParent(self)
        self.widgets.append(widget)
        
    def setOpenMethod(self,method):
        self.openMethod = method

    def setCloseMethod(self,method):
        self.closeMethod = method

    def runOpenMethod(self):
        if self.openMethod is not None:
            self.openMethod()
            
    def runCloseMethod(self):
        if self.closeMethod is not None:
            self.closeMethod()