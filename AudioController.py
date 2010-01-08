# -*- coding: utf-8 -*-
import os,pygame

class AudioController:

    def __init__(self,game):
        self.Game = game
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
        
        self.musicTracks = {
            'BLACKSMITH_MUSIC':os.path.join('data','audio','music','blacksmith.ogg'),
            'DEFAULT':os.path.join('data','audio','music','default.ogg'),
            'NOTEXPECTED':os.path.join('data','audio','music','notexpected.ogg')
            }

    def playMusic(self,trackName):
        if self.soundEnabled and self.musicEnabled:
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
            self.playSound(self.ambienceChannel,soundName,-1)

    def playSpeechSound(self,soundName):
        if self.soundEnabled:
            self.decreaseMusicVolume()
            self.playSound(self.speechChannel,soundName)

    def playUISound(self,soundName):
        if self.soundEnabled:
            self.playSound(self.UIChannel,soundName)

    def playMiscSound(self,soundName):
        if self.soundEnabled:
            self.playSound(self.miscChannel,soundName)
                
    def playSound(self,channel,soundName,loops=0):
        if self.soundEnabled:
            channel.play(self.Game.get(soundName),loops)

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