# resources
from Config import *
from Resources.Colors import *

# services
from Services.Audio import *
from Services.Video import *
from Services.Core import *
from Services.Input import *

class MainMenu():
    def __init__(self, core, audio, video, input):
        print 'MainMenu:: Starting Init'
        self.core = core
        self.audio = audio
        self.video = video
        self.input = input
        self.g = 0
        self.currentIndex = 0
        pass

    def Dispose(self):
        pass

    def Update(self):
        self.g = self.g + 1
        if (self.g > 255):
            self.g = 0

    def InputUpdate(self, k1, k2, k3, ku, kd, kl, kr, kp):
        if (ku):
            self.currentIndex = self.currentIndex - 1
        elif (kd):
            self.currentIndex = self.currentIndex + 1

        if (self.currentIndex < 0):
            self.currentIndex = 6
        elif (self.currentIndex > 6):
            self.currentIndex = 0

        if (k1):
            if (self.currentIndex == 0):
                from Scenes.Samples import *
                self.core.ChangeScene(Samples)
            elif (self.currentIndex == 1):
                from Scenes.Synths import *
                self.core.ChangeScene(Synths)
            elif (self.currentIndex == 2):
                from Scenes.Drums import *
                self.core.ChangeScene(Drums)
            elif (self.currentIndex == 3):
                from Scenes.Tapes import *
                self.core.ChangeScene(Tapes)
            elif (self.currentIndex == 4):
                from Scenes.Backups import *
                self.core.ChangeScene(Backups)
            elif (self.currentIndex == 5):
                pass
            elif (self.currentIndex == 6):
                self.core.RunCommand("sudo shutdown -h now")

    def Draw(self):
        indexColor = (100, self.g, 100)

        self.video.DrawLargeText(
            indexColor if self.currentIndex == 0 else Config.PrimaryTextColor, 
            (35, 2), 
            'Samples')

        self.video.DrawLargeText(
            indexColor if self.currentIndex == 1 else Config.PrimaryTextColor, 
            (40, 20), 
            'Synths')

        self.video.DrawLargeText(
            indexColor if self.currentIndex == 2 else Config.PrimaryTextColor, 
            (41, 38), 
            'Drums')

        self.video.DrawLargeText(
            indexColor if self.currentIndex == 3 else Config.PrimaryTextColor, 
            (45, 56), 
            'Tapes')

        self.video.DrawLargeText(
            indexColor if self.currentIndex == 4 else Config.PrimaryTextColor, 
            (38, 74), 
            'Backups')

        self.video.DrawLargeText(
            indexColor if self.currentIndex == 5 else Config.PrimaryTextColor, 
            (50, 92), 
            'Midi')

        self.video.DrawLargeText(
            indexColor if self.currentIndex == 6 else Config.PrimaryTextColor, 
            (49, 110), 
            'Shutdown')
    