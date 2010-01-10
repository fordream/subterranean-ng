# -*- coding: utf-8 -*-
import os,pygame                      
    
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
    def __init__(self,actor,sequenceName,duration=None):
        self.actor = actor
        self.sequenceName = sequenceName
        if duration is not None:
            self.duration = duration
        else:
            self.duration = len(self.actor.sequences.get(self.sequenceName))

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
        self.speaker = None
        
    def skip(self):
        self.skipped = True
        
    def setColor(self,color):
        self.currentColor = color
        
    def setDurationFrames(self,part):
        if part.getType() == 'ScriptConversationPart':
            if part.speech is not None:
                #If there is a sound, calculate the frames from it
                tmpSound = self.Game.get(part.speech)
                self.durationFrames = int(tmpSound.get_length()*32)
            else:
                #If not, calculate from the text.
                #TODO: Calibrate
                self.durationFrames = int(round(len(part.text) * 1.9))
        elif part.getType == 'ScriptWalkPart':
            #Calculate frames from path length
            #TODO: Calculate this
            self.durationFrames = 100
        elif part.getType() == 'ScriptSequencePart':
            self.durationFrames = part.duration
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

    def getSequenceName(self):
        return self.script[0].sequenceName

    def addConversationPart(self,actor,text,speech):
        self.script.append(ScriptConversationPart(actor,text,speech))

    def addWalkPart(self,actor,endPos):
        self.script.append(ScriptWalkPart(actor,endPos))

    def addSequencePart(self,actor,sequenceName,duration=None):
        self.script.append(ScriptSequencePart(actor,sequenceName,duration))

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
            self.getActor().setSequence('default')
            self.Game.AudioController.stopSpeech()
            self.skipped = False
            self.script.pop(0)
            self.resetStartFrame()
            if not len(self.script):
                #End
                self.Game.AudioController.restoreMusicVolume()
                self.resetScriptValues()
                self.Game.unpause()

        if self.Game.Renderer.Timer.currentFrame == self.startFrame:
            #Every part
            self.loadScriptValues(self.script[0])
            
            if self.script[0].__class__.__name__ == 'ScriptConversationPart':
                self.getActor().setSequence('talk')
                if self.script[0].speech is not None:
                    self.Game.AudioController.decreaseMusicVolume()
                    self.Game.AudioController.playSpeechSound(self.script[0].speech)
            elif self.script[0].__class__.__name__ == 'ScriptSequencePart':
                self.getActor().setSequence(self.getSequenceName())

                        
    def loadScriptValues(self,scriptPart):
        self.currentPartType = self.getCurrentPartType()
        #Determine what kind of part it is:
        if self.currentPartType == 'ScriptConversationPart':
            self.setColor(scriptPart.actor.getTextColor())
            self.setTextPos(scriptPart.actor.getTextPos())
        self.setDurationFrames(scriptPart)
        self.valuesLoaded = True
        
    def runScriptedWalk(self):        
        if len(self.getActor().path) == 0:
            self.skip()
            
        if not self.getActor().walking:
            self.getActor().walkTo(self.getWalkPos())
        
    def resetScriptValues(self):
        self.durationFrames = 50
        self.setColor((255,255,255))
        self.setTextPos((0,0))
        self.valuesLoaded = False
        self.startFrame = None