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

    def SelectMenuEntry(self):
        if (self.currentIndex == 0):
            from Scenes.Samples import *
            self.core.ChangeScene(Samples)
        elif (self.currentIndex == 1):
            from Scenes.Backups import *
            self.core.ChangeScene(Backups)
        elif (self.currentIndex == 2):
            from Scenes.ManageFiles import *
            self.core.ChangeScene(ManageFiles)
        elif (self.currentIndex == 3):
            self.core.Shutdown()
        elif (self.currentIndex == 4):
            pass
        elif (self.currentIndex == 5):
            pass
        elif (self.currentIndex == 6):
            pass

    def ChangeMenuIndex(self, delta):
        self.currentIndex += delta

        if (self.currentIndex < 0):
            self.currentIndex = 6
        elif (self.currentIndex > 6):
            self.currentIndex = 0

    def InputUpdate(self, k1, k2, k3, ku, kd, kl, kr, kp):
        if (ku):
            self.ChangeMenuIndex(-1)
        elif (kd):
            self.ChangeMenuIndex(1)
        if (k1):
            self.SelectMenuEntry()

    def Draw(self):
        indexColor = (100, self.g, 100)

        self.video.DrawLargeText(
            indexColor if self.currentIndex == 0 else Config.PrimaryTextColor, 
            (2, 2), 
            'Browse Sounds')

        self.video.DrawLargeText(
            indexColor if self.currentIndex == 1 else Config.PrimaryTextColor, 
            (30, 20), 
            'Backups')

        self.video.DrawLargeText(
            indexColor if self.currentIndex == 2 else Config.PrimaryTextColor, 
            (12, 38), 
            'Manage Files')

        self.video.DrawLargeText(
            indexColor if self.currentIndex == 3 else Config.PrimaryTextColor, 
            (22, 56), 
            'Shutdown')

        self.video.DrawLargeText(
            indexColor if self.currentIndex == 4 else Config.PrimaryTextColor, 
            (12, 74), 
            '')

        self.video.DrawLargeText(
            indexColor if self.currentIndex == 5 else Config.PrimaryTextColor, 
            (22, 92), 
            '')

        self.video.DrawLargeText(
            indexColor if self.currentIndex == 6 else Config.PrimaryTextColor, 
            (26, 110), 
            '')
    