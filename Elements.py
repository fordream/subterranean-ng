# -*- coding: utf-8 -*-
import os,pygame

    
class Element(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.debugMessage = self.__class__.__name__
        self.sprite = self.__class__.__name__
        self.name = None
        self.title = None
        self.dirty = 1
        
    def setName(self,name):
        self.name = name

    def getName(self):
        return self.name 
                
    def setTitle(self,title):
        self.title = title

    def getTitle(self):
        return self.title

    def setDebugText(self,text):
        self.debugMessage = text
            
class VisibleElement(Element):
    def __init__(self):
        Element.__init__(self)
        self.pos = (0,0)
        self.basePos = (0,0)
        self.actionPos = None
        self.image = None
        self.rect = None
        self.retrievable = False
        self.usable = False
        self.isCharacter = False
        self.useMethod = None
        self.lookMethod = None
        self.pickupMethod = None
        self.talkMethod = None
        self.giveMethods = {}
        self.textColor = (255,255,255)
        self.acceptElement = None
        self.resultElement = None
        self.animated = True

    def setTextColor(self,color):
        self.textColor = color
                
    def getTextPos(self):
        return (self.pos[0]-20,self.pos[1]-30)

    def setImage(self,image):
        self.image = image
        if self.rect is None:
            self.rect = self.image.get_rect()
    
    def setPosition(self,pos):
        self.pos = pos
        self.rect.move_ip(pos)
        if self.rect is not None:
            self.setBasePosition()
                
    def getPosition(self):
        return self.pos

    def setBasePosition(self):
        self.basePos = self.rect.midbottom

    def getBasePosition(self):
        return self.basePos

    def setActionPosition(self,pos):
        self.actionPos = pos

    def getActionPosition(self):
        return self.actionPos
        
    def setRetrievable(self,status):
        self.retrievable = status

    def getRetrievable(self):
        return self.retrievable
        
    def setUsable(self,status):
        self.usable = status

    def getUsable(self):
        return self.usable
        
    def setCharacter(self,status):
        self.isCharacter = status
        
    def getRetrievable(self):
        return self.isCharacter
        
    def setLookMethod(self,method):
        self.lookMethod = method

    def runLookMethod(self):
        self.lookMethod()

    def setUseMethod(self,method):
        self.useMethod = method

    def runUseMethod(self):
        self.useMethod()

    def setLookMethod(self,method):
        self.lookMethod = method

    def runLookMethod(self):
        self.lookMethod()

    def setTalkMethod(self,method):
        self.talkMethod = method

    def runTalkMethod(self):
        self.talkMethod()
        
    def setPickupMethod(self,method):
        self.pickupMethod = method

    def runPickupMethod(self):
        self.pickupMethod()
        
    def addGiveMethod(self,method,itemName):
        self.giveMethods[itemName] = method

    def runGiveMethod(self,item):
        method = self.giveMethods[item]
        method()
    
    def toItem(self):
        #Gets properties and returns an Item
        return Item(self.name,self.title,self.acceptElement,self.resultElement)
        
class AnimatedElement(VisibleElement):
    def __init__(self):
        VisibleElement.__init__(self)
        self.sequences = {}
        self.currentFrame = 0
        self.currentSequence = None
        self.animated = True
        
    def addSequence(self,sequenceName,sequence):
        imageFrames = []
        if self.isCharacter:
            directory = 'characters'
        else:
            directory = 'elements'

        #Load all frames in the sequence (Surface,length)
        for frame in sequence:
            try:
                for length in range(frame[1]):
                    imageFrames.append(frame[0])
            except TypeError:
                imageFrames.append(frame)
                
        self.sequences[sequenceName] = imageFrames
        if sequenceName == 'default':
            self.currentSequence = sequenceName
            
        #Just in case default loop stops:
        if self.image is None:
            self.setImage(self.sequences[sequenceName][0])
        
    def setSequence(self,sequence):
        if sequence in self.sequences:
            self.currentSequence = sequence
            self.currentFrame = 0
        else:
            self.currentSequence = None
            
    def getSequence(self):
        return self.currentSequence
    
    def update(self):
        if self.currentSequence is not None:
            try:
                frame = self.sequences[self.currentSequence][self.currentFrame]
                if self.currentFrame >= len(self.sequences[self.currentSequence])-1:
                    self.currentFrame = 0
                else:
                    self.currentFrame += 1
                self.image = frame
            except:
                return self.image
        else:
            return self.image

class Character(AnimatedElement):
    def __init__(self):
        AnimatedElement.__init__(self)
        self.isCharacter = True
        self.name = None
        self.topics = []
        self.textColor = (255,255,255)
        self.text = None
        self.textTimer = 0

    def setImage(self,image):
        self.image = image
        if self.rect is None:
            self.rect = self.image.get_rect()
        
    def loop(self):
        print self.name,"looped"
        
    def addTopic(self,topicName,topicTitle,callbackMethod):
        self.topics.append(Topic(self.Game,topicName,topicTitle,callbackMethod))
        #TODO Call this method in some nicer way and not on every topic add
        self.Game.TopicMenu.arrangeTopics()

    def removeTopic(self,topicName):
        for topic in self.topics:
            if topic.name == topicName:
                self.topics.remove(topic)
                self.Game.TopicMenu.arrangeTopics()
                
    def hasTopic(self,topicName):
        for topic in self.topics:
            if topic.name == topicName:
                return True
        return False
                    
    def getTextPos(self):
        return (self.rect.centerx,self.pos[1]-30)

    def setTextColor(self,textColor):
        self.textColor = textColor

    def getTextColor(self):
        return self.textColor
        
    def scriptSay(self,text,speech=None):
        self.Game.ScriptManager.addConversationPart(self,text,speech)

    def scriptSequence(self,sequenceName,duration=None):
        self.Game.ScriptManager.addSequencePart(self,sequenceName,duration)

    def scriptWalk(self,pos):
        self.Game.ScriptManager.addWalkPart(self,pos)
        
class Widget(AnimatedElement):
    def __init__(self):
        AnimatedElement.__init__(self)
        self.rect = None
        self.image = None
        self.parent = None
        self.rect = None
        self.clickMethod = None
        
    def setParent(self,parent):
        self.parent = parent
        self.alignToParent()
        
    def setPosition(self,pos):
        self.rect.left = pos[0]
        self.rect.top = pos[1]

    def alignToParent(self):
        #Moves the object to coordinates relative to parent
        self.rect.left += self.parent.rect.left
        self.rect.top += self.parent.rect.top
        
    def setImage(self,image):
        self.image = image
        self.rect = self.image.get_rect()
        
    def setClickMethod(self,method):
        self.clickMethod = method
        
    def runClickMethod(self):
        self.clickMethod()
        
class Topic: 
    def __init__(self,game,name,text,method):
        self.Game = game
        self.name = name
        self.text = text
        self.hover = False
        self.callbackMethod = method
        self.dialouge = []
        self.pos = (0,0)
        self.inactive = self.Game.Renderer.topicMenuFont.render(self.text,1,(216,203,163))
        self.active = self.Game.Renderer.topicMenuFont.render(self.text,1,(255,255,255))
        self.render = self.inactive
        self.rect = self.render.get_rect()
        self.rect.left,self.rect.top = self.pos
                
    def setDialogue(self):
        self.dialouge
        
    def setPos(self,pos):
        self.pos = pos
        self.rect.left,self.rect.top = self.pos
        
    def setActive(self):
        self.render = self.active

    def clearActive(self):
        self.render = self.inactive
        
    def setCallbackMethod(self,method):
        self.callbackMethod = method
        
    def runCallbackMethod(self):
        self.callbackMethod()
            
class Item:
    def __init__(self,name='unknown',title='Unknown item',acceptElement=None,resultElement=None):
        self.name = name
        self.title = title
        self.current = False
        self.acceptItem = None
        self.resultItem = None
        if acceptElement is not None and resultElement is not None:
            self.addCombimnation(acceptElement,resultElement)

        self.rect = pygame.Rect(10,10,48,48)
        self.loadImage(self.name)
        
    def setName(self,name):
        #Auto-reloads image on name change
        self.name = name
        self.loadImage(self.name)
        
    def getName(self):
        return self.name
        
    def setTitle(self,title):
        self.title = title

    def getTitle(self):
        return self.title
        
    def loadImage(self,name):
        try:
            self.image = pygame.image.load(os.path.join('data','items','%s.png' % (name)))
        except:
            self.image = pygame.image.load(os.path.join('data','items','unknown.png'))
                
    def setPos(self,pos):
        self.rect.move(pos)
        
    def setX(self,x):
        self.rect.left = x
        
    def setY(self,y):
        self.rect.top = y

    def addCombination(self,acceptItem,resultItem):
        self.acceptItem = acceptItem
        self.resultItem = resultItem
#        print self.name,"can recieve",acceptItem,"and will give you",resultItem
        
    def combine(self,comboItem):
        if self.acceptItem is not None and self.resultItem is not None and self.acceptItem == comboItem.name:
            self.Game.Inventory.combineItems(self,comboItem,self.resultItem)

class Exit:
    def __init__(self):
        self.rect = None
        self.sceneName = None
        self.direction = "NORTH"
        self.exitPoint = ()
        
    def getBasePosition(self):
        return (self.rect.centerx,self.rect.left)
    
    def setRect(self,rect):
        self.rect = rect
        
    def setExitPoint(self,point):
        self.exitPoint = point
        
    def setDirection(self,direction):
        self.direction = direction
        
    def setSceneName(self,sceneName):
        self.sceneName = sceneName