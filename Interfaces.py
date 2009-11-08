import os,pygame

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

    def addItem(self,element):
        self.items.append(Item(element))
        self.arrangeItems()
        self.y = 0
        self.hide()
        
    def arrangeItems(self):
        number = 0
        for item in self.items:
            if item.current is False:
                item.setX(number*60+10)
                number += 1
                                
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
            
class Item:
    def __init__(self,element):
        self.name = element.name
        self.current = False
        self.image = self.loadImage(self.name)
        self.title = element.title
        self.rect = pygame.Rect(10,10,48,48)
        
    def loadImage(self,name):
        return pygame.image.load(os.path.join('data','items','%s.png' % (name)))
        
    def getTitle(self,item):
        return 'Foo'
        
    def setPos(self,pos):
        self.rect.move(pos)
        
    def setX(self,x):
        self.rect.left = x
        
    def setY(self,y):
        self.rect.top = y

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
        if self.currentElement is not None:
            if self.prefix == 'Combine' or self.prefix == 'Give':
                return '%s %s %s %s' % (self.prefix,self.Game.Inventory.currentItem.title,self.suffix,self.currentElement.title)
            else:
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
        self.setCursor('DEFAULT')
     
    def setCursor(self,cursorName):
        if cursorName in self.cursors:
            self.cursorName = cursorName
            self.currentCursor = self.cursors[cursorName]
            
    def getCursor(self):
        if self.Game.Inventory.currentItem is not None:
            return self.Game.Inventory.currentItem.image
        else:
            return self.currentCursor
            
    def getCursorName(self):
        return self.cursorName
        
    def nextCursor(self):
        keys = self.cursors.keys()
        cursorIndex = keys.index(self.cursorName)
        print cursorIndex
        if cursorIndex < len(self.cursors)-1:
            self.setCursor(keys[cursorIndex + 1])
        else:
            self.setCursor("USE")

    def previousCursor(self):
        keys = self.cursors.keys()
        cursorIndex = keys.index(self.cursorName)
        print cursorIndex
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
                if(element.rect.collidepoint(pygame.mouse.get_pos())):
                    self.Game.TitleManager.setElement(element)
                    self.Game.TitleManager.setPrefix(self.getCursorName())
                    self.currentElement = element
                    if self.getCursorName() == 'DEFAULT':
                        self.setCursor('USE')
                    return self.currentElement
        else:
            for item in self.Game.Inventory.items:
                print item.rect
                if(item.rect.collidepoint(pygame.mouse.get_pos())):
                    if self.Game.Inventory.currentItem is not None and item.current is False:
                        print item.name
                        self.Game.TitleManager.setElement(item)
                        self.Game.TitleManager.setPrefix('COMBINE')
                        self.Game.TitleManager.setSuffix('WITH')
                        self.currentItem = item
                        return item
                
                    elif(item.rect.collidepoint(pygame.mouse.get_pos())):
                        self.Game.TitleManager.setElement(item)
                        self.Game.TitleManager.setPrefix('USE')
                        self.setCursor('USE')
                        self.currentItem = item
                        return item

        self.Game.TitleManager.clearElement()
        self.setCursor('DEFAULT')
        self.currentElement = None;