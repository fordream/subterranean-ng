# -*- coding: utf-8 -*-
import os,pygame

class AudioController:

    def __init__(self,game):
        try:
            pygame.mixer.init(44100)
        except:
            self.soundEnabled = False
            self.musicEnabled = False
            return
        self.soundEnabled = True
        self.musicEnabled = True
        self.musicState = None
        self.musicVolume= None
        self.currentMusicTrack = None
        self.currentSound = None
        self.ambienceChannel = pygame.mixer.Channel(1)
        self.speechChannel = pygame.mixer.Channel(2)
        self.UIChannel = pygame.mixer.Channel(3)
        self.miscChannel = pygame.mixer.Channel(4)
        try:
            self.musicTracks = {
                'DEFAULT':os.path.join('data','music','default.ogg'),
                'THEME':os.path.join('data','music','theme.ogg'),
                'NOTEXPECTED':os.path.join('data','music','notexpected.ogg')
            }
        except:
            self.musicTracks = {}

        self.ambienceSounds = {
            'AMBI001':os.path.join('data','sound','ambience','ambience001.ogg'),
            'WATER001':os.path.join('data','sound','ambience','water001.ogg')
        }
        
        self.UISounds = {
            'SLIDEIN':os.path.join('data','sound','ui','slidein.ogg'),
            'SLIDEOUT':os.path.join('data','sound','ui','slideout.ogg'),
            'MAP':os.path.join('data','sound','ui','map.ogg'),
        }        
        
        self.speechSounds = {
            'PLAYER001':os.path.join('data','sound','speech','player001.ogg'),
            'PLAYER002':os.path.join('data','sound','speech','player002.ogg'),
            'PLAYER003':os.path.join('data','sound','speech','player003.ogg')
        }

        self.miscSounds = {
            'STEP001':os.path.join('data','sound','misc','step001.ogg'),
            'STEP002':os.path.join('data','sound','misc','step002.ogg')
        }

    def playMusic(self,trackName):
        if self.soundEnabled and self.musicEnabled and trackName in self.musicTracks:
            if self.currentMusicTrack is not None and self.currentMusicTrack != trackName:
                pygame.mixer.music.fadeout(0)
            self.currentMusicTrack = trackName
            pygame.mixer.music.load(self.musicTracks.get(trackName))
            pygame.mixer.music.play(-1)
            self.musicState = 'unpaused'
            self.musicVolume= 'normal'

    def stopMusic(self):
        pygame.mixer.music.stop()
        
    def toggleMusicVolume(self):
        if self.musicVolume == 'normal':
            self.decreaseMusicVolume()
        else:
            self.restoreMusicVolume()    
        
    def decreaseMusicVolume(self):
        pygame.mixer.music.set_volume(0.5)
        self.musicVolume = 'decreased'
        
    def restoreMusicVolume(self):
        pygame.mixer.music.set_volume(1.0)
        self.musicVolume = 'normal'
        
    def toggleMusicPause(self):
        if self.musicState == 'unpaused':
            self.pauseMusic()
        else:
            self.unpauseMusic()
        
    def pauseMusic(self):
        pygame.mixer.music.pause()
        self.musicState = 'paused'
        
    def unpauseMusic(self):
        pygame.mixer.music.unpause()
        self.musicState = 'unpaused'
    
    def playAmbienceSound(self,soundName):
        if self.soundEnabled:
            self.playSound(self.ambienceChannel,self.ambienceSounds,soundName,-1)

    def playSpeechSound(self,soundName):
        if self.soundEnabled:
            self.decreaseMusicVolume()
            self.playSound(self.speechChannel,self.speechSounds,soundName)

    def playUISound(self,soundName):
        if self.soundEnabled:
            self.playSound(self.UIChannel,self.UISounds,soundName)

    def playMiscSound(self,soundName):
        if self.soundEnabled:
            self.playSound(self.miscChannel,self.miscSounds,soundName)
                
    def playSound(self,channel,soundList,soundName,loops=0):
        if self.soundEnabled and soundName in soundList:
            channel.play(pygame.mixer.Sound(soundList.get(soundName)),loops)
        else:
            print "Cound not find sound!:",soundName

    def stopSpeech(self):
        self.stopSound(self.speechChannel)

    def stopAmbience(self):
        self.stopSound(self.ambienceChannel)
        
    def stopSound(self,channel):
        if channel.get_busy():
            channel.stop()
        
    def enableMusic(self):
        self.musicEnabled = True

    def disableMusic(self):
        self.stopMusic()
        self.musicEnabled = False
        
    def enableSound(self):
        self.soundEnabled = True

    def disableSound(self):
        pygame.mixer.stop()
        pygame.mixer.music.stop()
        self.soundEnabled = False
        self.musicEnabled = False