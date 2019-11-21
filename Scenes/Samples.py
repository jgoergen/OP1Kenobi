# resources
from Config import *
from Resources.Colors import *

# services
from Services.Audio import *
from Services.Video import *
from Services.Core import *
from Services.Input import *

class Samples():
    def loadDirectoryData(self, path):
        files, directories = self.core.GetDataInDirectory(path)
        self.currentDirectories = directories
        self.currentFiles = []
        self.currentIndex = 0
    
        for file in files:
            if ".wav" in file.lower() or ".mp3" in file.lower():
                self.currentFiles.append(file)

    def getObjectType(self, index):
        if index < len(self.currentDirectories):
            return "Directory"
        elif (index - len(self.currentDirectories)) < len(self.currentFiles):
            return "File"
        else:
            return None

    def getObject(self, index):
        if index < len(self.currentDirectories):
            return self.currentDirectories[index]
        elif (index - len(self.currentDirectories)) < len(self.currentFiles):
            return self.currentFiles[(index - len(self.currentDirectories))]
        else:
            return None

    def __init__(self, core, audio, video, input):
        print 'Samples:: Starting Init'
        self.core = core
        self.audio = audio
        self.video = video
        self.input = input
        self.g = 0
        self.currentIndex = 0
        self.lastDirectories = [Config.MediaDirectory + "/samples"]
        self.volume = self.audio.GetVolume()
        
        # load base directory
        self.loadDirectoryData(self.lastDirectories[0]);

    def Dispose(self):
        pass

    def Update(self):
        self.g = self.g + 1
        if (self.g > 255):
            self.g = 0

    def ChangeMenuIndex(self, delta):
        self.currentIndex += delta

        # cursor wrapping
        if (self.currentIndex < 0):
            self.currentIndex = (len(self.currentDirectories) + len(self.currentFiles)) - 1

        elif (self.currentIndex > (len(self.currentDirectories) + len(self.currentFiles))):
            self.currentIndex = 0

    def SelectItem(self):
        objectType = self.getObjectType(self.currentIndex)
        currentObject = self.getObject(self.currentIndex)
        
        if objectType == "Directory":
            self.lastDirectories.append(currentObject)
            self.loadDirectoryData(currentObject);

        elif objectType == "File":
            self.audio.StopAllSounds()
            self.audio.PlaySound(currentObject)

    def GoBack(self):
        if len(self.lastDirectories) == 1:
            from Scenes.MainMenu import *
            self.core.ChangeScene(MainMenu)
        else:
            self.lastDirectories.pop()
            self.loadDirectoryData(self.lastDirectories[-1])

    def PlayAll(self):
        quit = False
        for file in self.currentFiles:
            if quit:
                break

            self.audio.StopAllSounds()
            self.audio.PlaySound(file)

            while self.audio.GetBusy():
                if self.input.KeyDown(Config.Key1Pin) or self.input.KeyDown(Config.Key2Pin) or self.input.KeyDown(Config.Key3Pin):
                    self.audio.StopAllSounds()
                    quit = True

    def DrawEntries(self, indexColor):
        line = 0
        for index in range(self.currentIndex, self.currentIndex + 10):
            currentObject = self.getObject(index)
            objectType = self.getObjectType(index)
                
            if objectType is not None:
                self.video.DrawSmallText(
                    indexColor if self.currentIndex == index else Config.PrimaryTextColor, 
                    (10, line * 11), 
                    currentObject[-18:])
            else:
                pass

            line += 1

    def DrawVolume(self):
        volumeBar = ""

        for i in range(0, int(self.volume * 10)):
            volumeBar += "|"
        
        self.video.DrawSmallText(
            Config.PrimaryTextColor, 
            (10, 115), 
            str(len(self.currentDirectories)) + "," + str(len(self.currentFiles)) + " : " + volumeBar)

    def InputUpdate(self, k1, k2, k3, ku, kd, kl, kr, kp):
        if ku:
            self.ChangeMenuIndex(-1)

        elif kd:
            self.ChangeMenuIndex(1)

        elif kl:
            self.volume = self.audio.LowerVolume(0.1)
            
        elif kr:
            self.volume = self.audio.RaiseVolume(0.1)

        if k1:
            self.SelectItem()

        if k2:
            self.PlayAll()

        if k3:
            self.GoBack()
            
    def Draw(self):
        indexColor = (100, self.g, 100)
        self.DrawEntries(indexColor)
        self.DrawVolume()