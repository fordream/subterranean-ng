import os,pygame

class Inventory:
    def __init__(self,game):
        self.Game = game
        self.items = []
        self.visible = False
        self.surface = pygame.Surface((1024,68))
        self.rect = self.surface.get_rect()
        self.surface.fill((25,25,25),self.rect)
        self.surface.set_alpha(145)
        self.animating = False
        self.y = -70
        self.spacing = 10

    def addItem(self,element):
        self.items.append(Item(element))
        self.arrangeItems()
        self.y = 0
        self.hide()
        
    def arrangeItems(self):
        number = 0
        for item in self.items:
            item.pos = number*60+10,10
            number += 1
                                
    def show(self):
        self.visible = True
        self.animating = True

    def hide(self):
        self.visible = False
        self.animating = True
        
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
            
class Item:
    def __init__(self,element):
        self.name = element.name
        self.image = self.loadImage(self.name)
        self.title = element.title
        self.pos = (0,0)
        self.rect = self.image.get_rect()
        
    def loadImage(self,name):
        return pygame.image.load(os.path.join('data','items','%s.png' % (name)))
        
    def getTitle(self,item):
        return 'Foo'
        
    def setY(self,y):
        self.pos = self.pos[0],y
            
class TitleManager:
    def __init__(self,game):
        self.Game = game
        self.prefix = ''
        self.currentElement = None
        
    def setPrefix(self,prefix=None):
        if prefix == 'USE':
            self.prefix = 'Use'
        elif prefix == 'PICKUP':
            self.prefix = 'Pick up'
        elif prefix == 'TALK':
            self.prefix = 'Talk to'
        elif prefix == 'LOOk':
            self.prefix = 'Look at'
        else:
            self.prefix = ''
                    
    def setElement(self,element):
        self.currentElement = element

    def clearElement(self):
        self.currentElement = None
        self.prefix = ''
        
    def getTitle(self):
        if self.currentElement is not None:
            return '%s %s' % (self.prefix,self.currentElement.title)
                            
class Conversation:
    def __init__(self,game):
        self.Game = game
        self.startFrame = None
        self.currentLineLenght = 100
        self.text = []
        
    def isActive(self):
        return len(self.text) > 0
        
    def setText(self,text):
        self.text = text
        
    def resetStartFrame(self):
        self.startFrame = self.Game.Renderer.Timer.currentFrame
        
    def getText(self):
        if self.startFrame is None:
            self.resetStartFrame()
        if len(self.text):
            if self.Game.Renderer.Timer.currentFrame - self.currentLineLenght == self.startFrame:
                self.text.pop()
                if len(self.text) < 1:
                    self.startFrame = None
                    return
                self.resetStartFrame()
            return self.text[0]

            
class Cursor():
    def __init__(self,game):
        self.Game = game
        self.currentElement = None;
        self.cursors = ['DEFAULT','USE','PICKUP','TALK','LOOK']
        self.cursorIndex = None
        self.setCursor(0)
     
    def setCursor(self,cursorIndex):
        if self.cursors[cursorIndex] is not None:
            self.cursorIndex = cursorIndex
            
    def getCursor(self):
        return self.cursors[self.cursorIndex]
        
    def nextCursor(self):
        if self.cursorIndex < len(self.cursors)-1:
            return self.cursorIndex + 1
        else:
            return 0

    def previousCursor(self):
        if self.cursorIndex > 1:
            return self.cursorIndex-1
        else:
            return len(self.cursors)-1
                    
    def scrollCursor(self,direction):
        if direction == 4:
            self.setCursor(self.nextCursor())
        else:
            self.setCursor(self.previousCursor())
            
    def checkCollisions(self):
        if pygame.mouse.get_pos()[1] > 70:        
            for element in self.Game.currentScene.visibleElements:
                if(element.rect.collidepoint(pygame.mouse.get_pos())):
                    self.Game.TitleManager.setElement(element)
                    self.Game.TitleManager.setPrefix(self.getCursor())
                    self.currentElement = element
                    if self.getCursor() == 'DEFAULT':
                        self.setCursor(1)
                    return self.currentElement
        else:
            for item in self.Game.Inventory.items:
                if(item.rect.collidepoint(pygame.mouse.get_pos())):
                    self.Game.TitleManager.setElement(item)
                    self.Game.TitleManager.setPrefix('USE')
                    self.setCursor(1)
                    return item

        self.Game.TitleManager.clearElement()
        self.setCursor(0)
        self.currentElement = None;