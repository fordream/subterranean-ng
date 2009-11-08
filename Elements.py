import os,pygame

class Element:
    def __init__(self):
        self.debugMessage = self.__class__.__name__
        self.name = None
        self.title = None
        
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
        self.image = None
        self.rect = None
        self.retrievable = False
        self.usable = False
        self.isCharacter = False
        self.useMethod = None
        self.lookMethod = None
        self.pickupMethod = None
        self.talkMethod = None

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
        
    def setRetrievable(self,status):
        self.retrievable = status
        
    def setUsable(self,status):
        self.usable = status

    def setCharacter(self,status):
        self.isCharacter = status
        
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

class Character(AnimatedElement):
    def __init__(self):
        AnimatedElement.__init__(self)
        self.character = True
        self.name = None
        self.topics = ()
        def addTopic(topic):
            self.topics.append(topic)
            
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