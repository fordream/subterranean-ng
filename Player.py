# -*- coding: utf-8 -*-
import os,pygame
import AStar
from time import time
from Elements import Character

class Player(Character):
    def __init__(self,game):
        Character.__init__(self)
        
        
        self.tempVar = False
                
        self.Game = game
        self.rect = None
        self.visible = False
        self.frameKey = 0
        self.startFrame = None
        self.startMillis = 0
        self.frameDuration = 3
        self.callbackMethod = None
        self.callbackArgument = None
        self.rect = pygame.Rect(0,0,60,20)
        self.direction = 's'

        
        #Stand
        self.addSequence('ns',[
            self.Game.get('PLAYER_STAND_N_1')
        ])
        self.addSequence('es',[
            self.Game.get('PLAYER_STAND_E_1')
        ])
        self.addSequence('ss',[
            self.Game.get('PLAYER_STAND_S_1')
        ])
        self.addSequence('ws',[
            self.Game.get('PLAYER_STAND_W_1')
        ])
        self.addSequence('nes',[
            self.Game.get('PLAYER_STAND_NE_1',)
        ])
        self.addSequence('ses',[
            self.Game.get('PLAYER_STAND_SE_1')
        ])
        self.addSequence('sws',[
            self.Game.get('PLAYER_STAND_SW_1')
        ])
        self.addSequence('nws',[
            self.Game.get('PLAYER_STAND_NW_1')
        ])
        
        #Walk
        self.addSequence('nw',[
            self.Game.get('PLAYER_WALK_N_1'),
            self.Game.get('PLAYER_WALK_N_2'),
            self.Game.get('PLAYER_WALK_N_3'),
            self.Game.get('PLAYER_WALK_N_4'),
            self.Game.get('PLAYER_WALK_N_5'),
            self.Game.get('PLAYER_WALK_N_6'),
            self.Game.get('PLAYER_WALK_N_7'),
            self.Game.get('PLAYER_WALK_N_8'),
        ])
        self.addSequence('sw',[
            self.Game.get('PLAYER_WALK_S_1'),
            self.Game.get('PLAYER_WALK_S_2'),
            self.Game.get('PLAYER_WALK_S_3'),
            self.Game.get('PLAYER_WALK_S_4'),
            self.Game.get('PLAYER_WALK_S_5'),
            self.Game.get('PLAYER_WALK_S_6'),
            self.Game.get('PLAYER_WALK_S_7'),
            self.Game.get('PLAYER_WALK_S_8'),
        ])
        self.addSequence('ew',[
            self.Game.get('PLAYER_WALK_E_1'),
            self.Game.get('PLAYER_WALK_E_2'),
            self.Game.get('PLAYER_WALK_E_3'),
            self.Game.get('PLAYER_WALK_E_4'),
            self.Game.get('PLAYER_WALK_E_5'),
            self.Game.get('PLAYER_WALK_E_6'),
            self.Game.get('PLAYER_WALK_E_7'),
            self.Game.get('PLAYER_WALK_E_8'),
        ])
        self.addSequence('ww',[
            self.Game.get('PLAYER_WALK_W_1'),
            self.Game.get('PLAYER_WALK_W_2'),
            self.Game.get('PLAYER_WALK_W_3'),
            self.Game.get('PLAYER_WALK_W_4'),
            self.Game.get('PLAYER_WALK_W_5'),
            self.Game.get('PLAYER_WALK_W_6'),
            self.Game.get('PLAYER_WALK_W_7'),
            self.Game.get('PLAYER_WALK_W_8'),
        ])
        self.addSequence('new',[
            self.Game.get('PLAYER_WALK_NE_1'),
            self.Game.get('PLAYER_WALK_NE_2'),
            self.Game.get('PLAYER_WALK_NE_3'),
            self.Game.get('PLAYER_WALK_NE_4'),
            self.Game.get('PLAYER_WALK_NE_5'),
            self.Game.get('PLAYER_WALK_NE_6'),
            self.Game.get('PLAYER_WALK_NE_7'),
            self.Game.get('PLAYER_WALK_NE_8'),
        ])
        self.addSequence('sew',[
            self.Game.get('PLAYER_WALK_SE_1'),
            self.Game.get('PLAYER_WALK_SE_2'),
            self.Game.get('PLAYER_WALK_SE_3'),
            self.Game.get('PLAYER_WALK_SE_4'),
            self.Game.get('PLAYER_WALK_SE_5'),
            self.Game.get('PLAYER_WALK_SE_6'),
            self.Game.get('PLAYER_WALK_SE_7'),
            self.Game.get('PLAYER_WALK_SE_8'),
        ])
        self.addSequence('sww',[
            self.Game.get('PLAYER_WALK_SW_1'),
            self.Game.get('PLAYER_WALK_SW_2'),
            self.Game.get('PLAYER_WALK_SW_3'),
            self.Game.get('PLAYER_WALK_SW_4'),
            self.Game.get('PLAYER_WALK_SW_5'),
            self.Game.get('PLAYER_WALK_SW_6'),
            self.Game.get('PLAYER_WALK_SW_7'),
            self.Game.get('PLAYER_WALK_SW_8'),
        ])
        self.addSequence('nww',[
            self.Game.get('PLAYER_WALK_NW_1'),
            self.Game.get('PLAYER_WALK_NW_2'),
            self.Game.get('PLAYER_WALK_NW_3'),
            self.Game.get('PLAYER_WALK_NW_4'),
            self.Game.get('PLAYER_WALK_NW_5'),
            self.Game.get('PLAYER_WALK_NW_6'),
            self.Game.get('PLAYER_WALK_NW_7'),
            self.Game.get('PLAYER_WALK_NW_8'),
        ])
        
        self.pos = (0,0)
        self.scale = 1
        self.walking = False
        self.talking = False
        self.standardResponses = {
            'PICKUP':"I can't pick that up",
            'USE':"Um... no.",
            'TALK':"I might as well be talking to myself.",
            'LOOK':"There is nothing noteworthy about it.",
            'GIVE':"I'm not giving that away."
        }
        
        self.textColor = (145,191,232)
        self.name = 'Player'
        self.path = []
        
    def face(self,element):
        self.facePos(element.pos)
        
    def facePos(self,pos):
        self.setDirection(pos)
            
    def findPath(self,x,y):
        startX = self.getX()/16
        startY = self.getY()/16
        endX = x/16
        endY = y/16
        astar = AStar.AStar(AStar.SQ_MapHandler(self.Game.currentScene.mapData,64,48))
        start = AStar.SQ_Location(startX,startY)
        end = AStar.SQ_Location(endX,endY)
        path = astar.findPath(start,end)
        if path is not None:
            self.path = []
            self.path.append((start.x*16,start.y*16))
            for node in path.nodes:
                self.path.append((node.location.x*16,node.location.y*16))
            self.path.append((end.x*16,end.y*16))
            return True
        else:
            return False

    def walk(self):
        if len(self.path):
            self.setPosition(self.path[0])
            self.path.pop(0)
            if len(self.path) > 1:
                self.setDirection(self.path[1])
        else:
            self.walking = False
            if self.callbackMethod is not None:
                self.runCallback()
                
    def runCallback(self):
        self.callbackMethod(self.argument)
        self.callbackMethod = None
        self.callbackArgument = None
        
    def resetStartFrame(self):
        self.startFrame = self.Game.Renderer.Timer.currentFrame

    def resetFrameKey(self):
        self.frameKey = 0
        
    def getFrameKey(self,sequence):
        #Every frame takes twice the time == a nice speed at 12fps
        if self.Game.Renderer.Timer.currentFrame -2 == self.startFrame:
            self.walk()
            self.resetStartFrame()
            if self.frameKey < len(sequence)-1:
                self.frameKey += 1
            else:
                self.resetFrameKey()
        elif self.Game.Renderer.Timer.currentFrame == self.startFrame or self.frameKey is None:
            self.resetFrameKey()
            
        if self.frameKey == 3:
            self.Game.AudioController.playMiscSound("STEP001")
        elif self.frameKey == 7:
            self.Game.AudioController.playMiscSound("STEP002")
            
        return self.frameKey
        
    def getCurrentFrame(self):
        if self.walking:
            state = 'w'
        else:
            state = 's'
            
        sequence = self.sequences.get('%s%s' % (self.getDirection(),state))
        if sequence is not None:
            #FIXME: Bugging
            try:
                currentFrame = sequence[self.getFrameKey(sequence)]
            except IndexError:
                currentFrame = sequence[0]

        self.currentFrame = self.scaleImage(currentFrame)

        #Catch!
        if self.currentFrame is None:
            self.currenFrame = sequence[0]

        return self.currentFrame
        
    def scaleImage(self,image=None):
        #WORK IN PROGRESS    
        pointDiff = self.Game.currentRoom.closestPoint - self.Game.currentRoom.farthestPoint
        scaleDiff = self.Game.currentRoom.closestScale - self.Game.currentRoom.farthestScale
        diff = float(scaleDiff)/float(pointDiff)        
        self.scale = (self.Game.Player.getPosition()[1]*diff)/100
        if image:
            return pygame.transform.rotozoom(image,0,self.scale)

    def getRenderPos(self):
        return (self.rect.left,self.rect.bottom-self.currentFrame.get_height())

    def setPosition(self,pos):
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.pos = pos
                
    def setDirection(self,newPos):
        if self.getPosition()[0] < newPos[0] and self.getPosition()[1] == newPos[1]:
            self.direction = 'e'
        elif self.getPosition()[0] > newPos[0] and self.getPosition()[1] == newPos[1]:
            self.direction = 'w'
        elif self.getPosition()[0] == newPos[0] and self.getPosition()[1] < newPos[1]:
            self.direction = 's'
        elif self.getPosition()[0] == newPos[0] and self.getPosition()[1] > newPos[1]:
            self.direction = 'n'
        elif self.getPosition()[0] < newPos[0] and self.getPosition()[1] < newPos[1]:
            self.direction = 'se'
        elif self.getPosition()[0] > newPos[0] and self.getPosition()[1] > newPos[1]:
            self.direction = 'nw'
        elif self.getPosition()[0] < newPos[0] and self.getPosition()[1] > newPos[1]:
            self.direction = 'ne'
        elif self.getPosition()[0] > newPos[0] and self.getPosition()[1] < newPos[1]:
            self.direction = 'sw'
        return self.direction
        
    def getDirection(self):
        return self.direction
            
    def getPosition(self):
        return self.pos
                        
    def getX(self):
        return self.pos[0]
        
    def getY(self):
        return self.pos[1]
        
    def inRange(self,element):
        #TODO: Refine this? Currently has a range of 100px
        closenessX = self.getPosition()[0] - element.getBasePosition()[0]
        closenessY = self.getPosition()[1] - element.getBasePosition()[1]
        return(closenessX + closenessY < 100 and closenessX + closenessY > -100)
        
    def walkTo(self,(x,y),callbackMethod=None,argument=None):        
        if callbackMethod is not None and argument is not None:
            self.callbackMethod = callbackMethod
            self.argument = argument
        if not self.walking:
            if self.findPath(x,y):
                self.resetStartFrame()
                self.walking = True
                if self.Game.TopicMenu.visible:
                    self.Game.TopicMenu.hide()
            else:
                print "No avalible tiles at",x,y
        
    def pickUp(self,element):
        self.face(element)
        if not self.Game.paused and self.inRange(element) and element.getRetrievable():
            self.Game.Inventory.addItem(element.toItem())
            self.Game.currentScene.visibleElements.remove(element)
            if element.pickupMethod is not None:
                element.pickupMethod()
        else:
            self.scriptSay(self.standardResponses['PICKUP'])
        
    def use(self,element):
        self.face(element)
        print element.useMethod
        if element.useMethod is not None:
            element.useMethod()
        else:
            self.scriptSay(self.standardResponses['USE'])
            
    def look(self,element):
        self.face(element)
        if element.lookMethod is not None:
            element.lookMethod()
        else:
            self.scriptSay(self.standardResponses['LOOK'])

    def talk(self,character):
        if character.isCharacter and character.talkMethod is not None:
            self.face(character)
            self.Game.TopicMenu.loadCharacterTopics(character)
            self.Game.TopicMenu.show()
            character.talkMethod()
        else:
            self.scriptSay(self.standardResponses['TALK'])

    def give(self,element):
        self.face(element)
        if self.Game.Inventory.currentItem is not None and self.inRange(element) and self.Game.Inventory.currentItem.name in element.giveMethods:
            element.runGiveMethod(self.Game.Inventory.currentItem.name)
            self.Game.Inventory.clearCurrentItem()
        else:
            self.scriptSay(self.standardResponses['GIVE'])

    def exit(self,exit):
        if self.inRange(exit):
            self.Game.currentScene.exit(exit.sceneName)

    def randomTalk(self):
        if not self.tempVar:
            self.scriptSay("Hur kom jag hit egentligen? Det vet jag inte, men det är ju väldigt coolt i alla fall.","PLAYER001")
            self.scriptWalk((600,460))
            self.scriptSay("Här kan man vara.","PLAYER002")
            self.tempVar = True
        else:
            self.scriptWalk((334,416))
            self.scriptSay("Hej då!")
                        
    def getTextPos(self):
        return (self.rect.centerx,self.getRenderPos()[1]-30)