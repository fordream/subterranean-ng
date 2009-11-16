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
        self.y = -70
        self.spacing = 10

    def addItem(self,item,runEffect=True):
        #Need game reference to talk to Inventory later
        item.Game = self.Game
        self.items.append(item)
        if runEffect:
            self.arrangeItems()
            self.y = 0
            self.hide()
        
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
                item.setX(number*60+10)
                number += 1
            else:
                item.setX(-100)
                                                
    def show(self):
        self.visible = True
        self.animating = True

    def hide(self):
        self.visible = False
        self.animating = True
        
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
            if self.visible and self.y < 0:
                self.y+=10
                for item in self.items:
                    item.setY(self.y+10)
            elif not self.visible and self.y > -70:
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

class Topic: 
    def __init__(self,game,text,pos):
        self.Game = game
        self.text = text
        self.hover = False
        self.dialouge = []
        self.pos = pos
        self.render = self.Game.Renderer.generalFont.render(self.text,1,(255,255,255))
        
    def setDialogue(self):
        self.dialouge
        
    def setPos(self,pos):   
        self.pos = pos
        
    def update(self):
        return 
                        
class TopicMenu:
    def __init__(self,game):
        self.Game = game
        self.visible = False
        self.surface = pygame.Surface((1024,168))
        self.rect = self.surface.get_rect()
        self.surface.fill((25,25,25),self.rect)
        self.surface.set_alpha(145)
        self.topics = []
        self.rect.y = 700
        self.rect.x = 0
        
    def addTopic(self,text):
        totalLen = 0
        index = 0
        if len(self.topics):
            for topic in self.topics:
                totalLen += topic.render.get_width()
        index = len(self.topics)
        pos = (totalLen+index*25+25,710)

        self.topics.append(Topic(self.Game,text,pos))
                
    def display(self):
        self.visible = True
        
    def hide(self):
        self.visible = False

class ScriptConversationPart:
    def __init__(self,actor,text):
        self.actor = actor
        self.text = text

class ScriptWalkPart:
    def __init__(self,actor,walkPos):
        self.actor = actor
        self.walkPos = walkPos

class ScriptSequencePart:
    def __init__(self,actor,sequenceName):
        self.actor = actor
        self.sequenceName = sequenceName

class ScriptMethodPart:
    def __init__(self,method,args):
        self.method = method
        self.args = args
                           
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
        
    def setColor(self,color):
        self.currentColor = color
        
    def setDurationFrames(self,textLength):
        self.durationFrames = textLength * 1
                
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

    def addConversationPart(self,actor,text):
        self.script.append(ScriptConversationPart(actor,text))

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
            #We just started a script
            self.resetStartFrame()
            self.Game.pause()
        elif self.Game.Renderer.Timer.currentFrame - self.durationFrames == self.startFrame:
            #If the wait is done, go to the next part
            self.script.pop(0)
            self.resetStartFrame()
            if not len(self.script):
                #No more parts. End script
                self.resetScriptValues()
                self.Game.unpause()
            else:
                #Load the part values
                self.loadScriptValues(self.script[0])
        
    def loadScriptValues(self,scriptPart):
        self.currentPartType = self.getCurrentPartType()
        #Determine what kind of part it is:
        if self.currentPartType == 'ScriptConversationPart':
            self.setDurationFrames(len(scriptPart.text))
            self.setColor(scriptPart.actor.getTextColor())
            self.setTextPos(scriptPart.actor.getTextPos())
        elif self.currentPartType == 'ScriptWalkPart':
            #FIXME. Decide how many frames to wait automatically
            self.setDurationFrames(30)
        self.valuesLoaded = True
        
    def runScriptetWalk(self):
        if not self.getActor().walking:
            self.getActor().walkTo(self.getWalkPos())
        
    def resetScriptValues(self):
        self.setDurationFrames(50)
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
        
        #Kept in its own variable so we don't loop over it while scrolling.
        self.pausedCursor = pygame.image.load(os.path.join('data','cursors','cursor_paused.png'))
        
        self.setCursor('DEFAULT')
     
    def setCursor(self,cursorName):
        if cursorName in self.cursors:
            self.cursorName = cursorName
            self.currentCursor = self.cursors[cursorName]
            
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
        if pygame.mouse.get_pos()[1] > 70:        
            for element in self.Game.currentScene.visibleElements:
                #Calculate center for item cursor to avoid pixel hunting.
                #Also set the prefix correctly.
                #TODO: Make this loop smarter. Really.
                if self.Game.Cursor.currentItem is not None:
                    mouse = pygame.mouse.get_pos()
                    pos = (mouse[0]+24,mouse[1]+24)
                else:
                    pos = pygame.mouse.get_pos  ()
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
        else:
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

        self.Game.TitleManager.clearElement()
        self.setCursor('DEFAULT')
        self.currentElement = None;