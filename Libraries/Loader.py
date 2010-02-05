# -*- coding: utf-8 -*-
import os,pygame,time

class Loader:

    def __init__(self,game):
        self.Game = game
        self.data = {}
        self.resourcesDirectory = os.path.join('Resources')
        self.graphicsDirectory = os.path.join('Resources','Graphics')
        self.audioDirectory = os.path.join('Resources','Audio')
        self.numAssets = 0
        
    def buildPath(self,start,path=[]):
        fullPath = start
        for node in path:
            fullPath = os.path.join(fullPath,node)
        return fullPath
        
    def load(self,key,fileObject):
        self.data[key] = fileObject
        self.Game.log("Loaded",key)
        self.numAssets += 1

    def loadResource(self,key,path):
        imagePath = self.resourcesDirectory
        for node in path:
            imagePath = os.path.join(imagePath,node)
        self.load(key,pygame.image.load(imagePath).convert_alpha())

    def loadImage(self,key,path):
        def convertPixels(image):
            if path[-1].endswith('.png'):
                return image.convert_alpha()
            else:
                return image.convert()

        imagePath = self.buildPath(self.graphicsDirectory,path)
                    
        self.load(key,convertPixels(pygame.image.load(imagePath)))
   
    def loadAudio(self,key,path):
        audioPath = self.buildPath(self.audioDirectory,path)
        self.load(key,pygame.mixer.Sound(audioPath))
        
    def loadSequence(self,keyStart,path,length):
        filename = path[-1]
        path.pop()
        for image in range(length):
            tmpPath = path[:]
            tmpPath.append(filename.replace('.',str(image+1)+'.'))
            self.loadImage(keyStart+str(image+1),tmpPath)
        
    def get(self,key):
        if key in self.data:
            return self.data.get(key)
        else:
            print "No such key:",key
            return None
            
    def preload(self):
        start = time.clock()
        
        #Backgrounds
        self.loadImage('BLACKSMITH_BACKGROUND',['Backgrounds','blacksmith.jpg'])
        self.loadImage('BLACKSMITH_FOREGROUND',['Foregrounds','blacksmith.png'])
        self.loadImage('WATERMILL_BACKGROUND',['Backgrounds','watermill.jpg'])
        self.loadImage('WATERMILL_FOREGROUND',['Foregrounds','watermill.png'])
        self.loadImage('CRASHSITE_BACKGROUND',['Backgrounds','crashsite.jpg'])
        
        #Ambience
        self.loadAudio('AMBI_DEFAULT',['Ambience','ambi-noise-default.ogg'])
        self.loadAudio('AMBI_ELECTRICITY',['Ambience','ambi-noise-electricity.ogg'])
        self.loadAudio('AMBI_RIVER',['Ambience','ambi-noise-river.ogg'])
        self.loadAudio('AMBI_DROP',['Ambience','ambi-noise-drop.ogg'])
        self.loadAudio('AMBI_WATER',['Ambience','ambi-water.ogg'])
        #UI Gfx
        self.loadResource('ICON',['Icons','gameicon.png'])
        self.loadImage('LOGO',['Misc','logo.png'])
        self.loadImage('BORDER',['UI','ui-viewport-border.png'])
        self.loadImage('INVENTORY',['UI','ui-inventory.png'])
        self.loadImage('ACTIONMENU_DEFAULT',['UI','ui-actionmenu-default.png'])
        self.loadImage('ACTIONMENU_LOOK',['UI','ui-actionmenu-look.png'])
        self.loadImage('ACTIONMENU_PICKUP',['UI','ui-actionmenu-pickup.png'])
        self.loadImage('ACTIONMENU_TALK',['UI','ui-actionmenu-talk.png'])
        self.loadImage('ACTIONMENU_USE',['UI','ui-actionmenu-use.png'])
        #UI Sfx
        self.loadAudio('MAP_OPEN',['UI','map.ogg']),
        self.loadAudio('SLIDEIN',['UI','slidein.ogg']),
        self.loadAudio('SLIDEOUT',['UI','slideout.ogg']),
        #Speech        
        self.loadAudio('PLAYER001',['Speech','player001.ogg']),
        self.loadAudio('PLAYER002',['Speech','player002.ogg']),
        self.loadAudio('PLAYER003',['Speech','player003.ogg'])
        #Misc
        self.loadAudio('STEP001',['Misc','step001.ogg']),
        self.loadAudio('STEP002',['Misc','step002.ogg'])
        #Elements
        self.loadSequence('FIRE_DEFAULT_',['Elements','Fire','fire-default-.png'],4)
        self.loadImage('TOOLBARREL_DEFAULT',['Elements','Toolbarrel','toolbarrel.png'])
        self.loadImage('MAP_DEFAULT',['Elements','Map','map.png'])
        #Items
        self.loadImage('ITEM_0000',['Items','item-0000.png'])
        self.loadImage('ITEM_0001',['Items','item-0001.png'])
        self.loadImage('ITEM_0002',['Items','item-0002.png'])
        self.loadImage('ITEM_0003',['Items','item-0003.png'])
        self.loadImage('ITEM_0004',['Items','item-0004.png'])
        #Characters
        self.loadSequence('GRIMVALD_STAND_',['Characters','Grimvald','grimvald-stand-.png'],2)
        self.loadSequence('GRIMVALD_TALK_',['Characters','Grimvald','grimvald-talk-.png'],5)
        self.loadSequence('GRIMVALD_SILLY_',['Characters','Grimvald','grimvald-silly-.png'],3)
        #Windows
        self.loadImage('MAP_BACKGROUND',['Windows','map.png'])
        #Widgets
        self.loadImage('MAP_CROSS',['Widgets','Map','map-cross.png'])
        self.loadImage('MAP_ALTAR',['Widgets','Map','map-altar.png'])        
        self.loadImage('MAP_GATES',['Widgets','Map','map-gates.png'])
        self.loadImage('MAP_QUARRY',['Widgets','Map','map-quarry.png'])
        self.loadImage('MAP_CHAMBER',['Widgets','Map','map-chamber.png'])
        self.loadImage('MAP_UNDERFJORD',['Widgets','Map','map-underfjord.png'])
        self.loadImage('MAP_SUNMINE',['Widgets','Map','map-sunmine.png'])
        
        self.loadSequence('PLAYER_STAND_N_',['Characters','Vincent','north-stand-.png'],1)
        self.loadSequence('PLAYER_STAND_E_',['Characters','Vincent','east-stand-.png'],1)
        self.loadSequence('PLAYER_STAND_S_',['Characters','Vincent','south-stand-.png'],1)
        self.loadSequence('PLAYER_STAND_W_',['Characters','Vincent','west-stand-.png'],1)
        self.loadSequence('PLAYER_STAND_NE_',['Characters','Vincent','northeast-stand-.png'],1)
        self.loadSequence('PLAYER_STAND_SE_',['Characters','Vincent','southeast-stand-.png'],1)
        self.loadSequence('PLAYER_STAND_SW_',['Characters','Vincent','southwest-stand-.png'],1)
        self.loadSequence('PLAYER_STAND_NW_',['Characters','Vincent','northwest-stand-.png'],1)
        
        self.loadSequence('PLAYER_WALK_N_',['Characters','Vincent','north-walk-.png'],8)
        self.loadSequence('PLAYER_WALK_S_',['Characters','Vincent','south-walk-.png'],8)
        self.loadSequence('PLAYER_WALK_E_',['Characters','Vincent','east-walk-.png'],8)
        self.loadSequence('PLAYER_WALK_W_',['Characters','Vincent','west-walk-.png'],8)
        self.loadSequence('PLAYER_WALK_NE_',['Characters','Vincent','northeast-walk-.png'],8)
        self.loadSequence('PLAYER_WALK_SE_',['Characters','Vincent','southeast-walk-.png'],8)
        self.loadSequence('PLAYER_WALK_SW_',['Characters','Vincent','southwest-walk-.png'],8)        
        self.loadSequence('PLAYER_WALK_NW_',['Characters','Vincent','northwest-walk-.png'],8)

        self.Game.log("Loaded",str(self.numAssets),"game assets in",str(time.clock()-start),"seconds")