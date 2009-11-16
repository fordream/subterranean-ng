import os,pygame

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

    def update(self):
        pass

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

    def setTextColor(self,color):
        self.textColor = color
                
    def getTextPos(self):
        return (self.pos[0]-20,self.pos[1]-30)

    def setImage(self,fileName):
        self.image = pygame.image.load(os.path.join('data','elements',fileName))
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
        
    def addSequence(sequenceName,frames):
        self.sequences[sequenceName] = frames
        
    def getFrame():
        frame = self.sequences[self.currentSequence][self.currentFrame]
        if self.currentFrame >= len(self.sequences[currentSequence]-1):
            self.currentFrame = 0
        else:
            self.currentFrame = self.currentFrame + 1
        return frame

class Area(Element):
    def __init__(self):
        self.rect = pygame.Rect(0,0,0,0)
        
    def setSize(w,h):
        self.rect.inflate_ip(w,h)
    
    def setPosition(pos):
        self.rect.move_ip(pos)

class Puzzle(VisibleElement):
    def __init__(self):
        print self.__class__.__name__
        
class ConversationPart:
    def __init__(self,actor,text):
        self.actor = actor
        self.text = text

class Character(AnimatedElement):
    def __init__(self,game):
        AnimatedElement.__init__(self)
        self.Game = game
        self.isCharacter = True
        self.name = None
        self.topics = ()
        self.textColor = (255,255,255)
        self.text = None
        self.textTimer = 0
        
    def loop(self):
        print self.name,"looped"
        
    def addTopic(topic):
        self.topics.append(topic)
                    
    def getTextPos(self):
        return (self.rect.centerx,self.pos[1]-30)

    def setTextColor(self,textColor):
        self.textColor = textColor

    def getTextColor(self):
        return self.textColor
        
    def scriptSay(self,text):
        self.Game.ScriptManager.addConversationPart(self,text)

    def scriptWalk(self,pos):
        self.Game.ScriptManager.addWalkPart(self,pos)

            
class Widget(AnimatedElement):
    def __init__(self):
        print self.__class__.__name__

class Topic:
    def __init__(self,topicName):
        self.topicName
        self.dialouge
        
    def addDialouge(dialouge):
        pass
        #TODO