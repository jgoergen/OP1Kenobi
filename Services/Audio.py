# system imports
import os
import pygame
from pygame import time

# resources
from Config import *

class Audio():
    def __init__(self, core):
        print('Audio:: Starting Init')
        # max out system volume
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        print(core.RunCommand('amixer  sset Speaker,0 90%'))

    def Update(self):
        pass

    def PlaySound(self, pathToSound):
        if ".mp3" in pathToSound.lower():
            pygame.mixer.music.load(pathToSound)
            pygame.mixer.music.set_volume(Config.SoundVolume)
            pygame.mixer.music.play()
        
        if ".wav" in pathToSound.lower():
            sound = pygame.mixer.Sound(pathToSound)
            sound.set_volume(Config.SoundVolume)
            pygame.mixer.Sound.play(sound)

    def StopAllSounds(self):
        pygame.mixer.stop()
        pygame.mixer.music.stop()

    def GetBusy(self):
        return pygame.mixer.get_busy()

    def GetVolume(self):
        return Config.SoundVolume

    def RaiseVolume(self, amount):
        Config.SoundVolume += amount

        if Config.SoundVolume > 1:
            Config.SoundVolume = 1
        
        return Config.SoundVolume

    def LowerVolume(self, amount):
        Config.SoundVolume -= amount

        if Config.SoundVolume < 0:
            Config.SoundVolume = 0
        
        return Config.SoundVolume