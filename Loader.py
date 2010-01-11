# -*- coding: utf-8 -*-
import os,pygame,time

class Loader:

    def __init__(self,game):
        self.Game = game
        self.data = {}
        self.imageDirectory = './data'
        self.audioDirectory = os.path.join('data','audio')
        self.numAssets = 0
        
    def load(self,key,fileObject):
        self.data[key] = fileObject
        self.Game.log("Loaded",key)
        self.numAssets += 1
        
    def loadImage(self,key,category,filename):
        def convertPixels(image):
            if filename.endswith('.png'):
                return image.convert_alpha()
            else:
                return image.convert()
        self.load(key,convertPixels(pygame.image.load(os.path.join(self.imageDirectory,category,filename))))
   
    def loadAudio(self,key,category,filename):
        self.load(key,pygame.mixer.Sound((os.path.join(self.audioDirectory,category,filename))))
        
    def loadSequence(self,keyStart,category,filename,length):
        for image in range(length):
            self.loadImage(keyStart+str(image+1),category,filename.replace('.',str(image+1)+'.'))
        
    def get(self,key):
        if key in self.data:
            return self.data.get(key)
        else:
            print "No such key:",key
            return None
            
    def preload(self):
        start = time.clock()
        
        #Backgrounds
        self.loadImage('BLACKSMITH_BACKGROUND','backgrounds','blacksmith.jpg')
        self.loadImage('BLACKSMITH_FOREGROUND','foregrounds','blacksmith.png')
        self.loadImage('WATERMILL_BACKGROUND','backgrounds','watermill.jpg')
        self.loadImage('WATERMILL_FOREGROUND','foregrounds','watermill.png')
        self.loadImage('CRASHSITE_BACKGROUND','backgrounds','crashsite.jpg')
        
        #Ambience
        self.loadAudio('AMBI001','ambience','ambience001.ogg')
        self.loadAudio('WATER001','ambience','water001.ogg')
        #UI Gfx
        self.loadImage('ICON','icons','gameicon.png')
        self.loadImage('LOGO','ui','inventory.png')
        self.loadImage('INVENTORY','ui','inventory.png')
        self.loadImage('ACTIONMENU_DEFAULT','ui','actionmenu-default.png')
        self.loadImage('ACTIONMENU_LOOK','ui','actionmenu-look.png')
        self.loadImage('ACTIONMENU_PICKUP','ui','actionmenu-pickup.png')
        self.loadImage('ACTIONMENU_TALK','ui','actionmenu-talk.png')
        self.loadImage('ACTIONMENU_USE','ui','actionmenu-use.png')
        #UI Sfx
        self.loadAudio('MAP_OPEN','ui','map.ogg'),
        self.loadAudio('SLIDEIN','ui','slidein.ogg'),
        self.loadAudio('SLIDEOUT','ui','slideout.ogg'),
        #Speech        
        self.loadAudio('PLAYER001','speech','player001.ogg'),
        self.loadAudio('PLAYER002','speech','player002.ogg'),
        self.loadAudio('PLAYER003','speech','player003.ogg')
        #Misc
        self.loadAudio('STEP001','misc','step001.ogg'),
        self.loadAudio('STEP002','misc','step002.ogg')
        #Elements
        self.loadSequence('FIRE_DEFAULT_','elements','fire-default-.png',4)
        self.loadImage('TOOLBARREL_DEFAULT','elements','toolbarrel.png')
        self.loadImage('MAP_DEFAULT','elements','map.png')
        #Items
        #Characters
        self.loadSequence('GRIMVALD_STAND_','characters','grimvald-stand-.png',2)
        self.loadSequence('GRIMVALD_TALK_','characters','grimvald-talk-.png',5)
        self.loadSequence('GRIMVALD_SILLY_','characters','grimvald-silly-.png',3)
        #Windows
        self.loadImage('MAP_BACKGROUND','windows','map.png')
        #Widgets
        self.loadImage('MAP_CROSS','widgets','map-cross.png')
        self.loadImage('MAP_ALTAR','widgets','map-altar.png')        
        self.loadImage('MAP_GATES','widgets','map-gates.png')
        self.loadImage('MAP_QUARRY','widgets','map-quarry.png')
        self.loadImage('MAP_CHAMBER','widgets','map-chamber.png')
        self.loadImage('MAP_UNDERFJORD','widgets','map-underfjord.png')
        self.loadImage('MAP_SUNMINE','widgets','map-sunmine.png')
        
        self.loadSequence('PLAYER_STAND_N_','maincharacter','north-stand-.png',1)
        self.loadSequence('PLAYER_STAND_E_','maincharacter','east-stand-.png',1)
        self.loadSequence('PLAYER_STAND_S_','maincharacter','south-stand-.png',1)
        self.loadSequence('PLAYER_STAND_W_','maincharacter','west-stand-.png',1)
        self.loadSequence('PLAYER_STAND_NE_','maincharacter','northeast-stand-.png',1)
        self.loadSequence('PLAYER_STAND_SE_','maincharacter','southeast-stand-.png',1)
        self.loadSequence('PLAYER_STAND_SW_','maincharacter','southwest-stand-.png',1)
        self.loadSequence('PLAYER_STAND_NW_','maincharacter','northwest-stand-.png',1)
        
        self.loadSequence('PLAYER_WALK_N_','maincharacter','north-walk-.png',8)
        self.loadSequence('PLAYER_WALK_S_','maincharacter','south-walk-.png',8)
        self.loadSequence('PLAYER_WALK_E_','maincharacter','east-walk-.png',8)
        self.loadSequence('PLAYER_WALK_W_','maincharacter','west-walk-.png',8)
        self.loadSequence('PLAYER_WALK_NE_','maincharacter','northeast-walk-.png',8)
        self.loadSequence('PLAYER_WALK_SE_','maincharacter','southeast-walk-.png',8)
        self.loadSequence('PLAYER_WALK_SW_','maincharacter','southwest-walk-.png',8)        
        self.loadSequence('PLAYER_WALK_NW_','maincharacter','northwest-walk-.png',8)



        self.Game.log("Loaded",str(self.numAssets),"game assets in",str(time.clock()-start),"seconds")