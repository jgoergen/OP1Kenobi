# resources
from Config import *
from Resources.Colors import *

# services
from Services.Audio import *
from Services.Video import *
from Services.Core import *
from Services.Input import *

class Albums():
    def loadDirectoryData(self, path):
        files, directories = self.core.GetDataInDirectory(path)
        self.currentDirectories = directories
        self.currentFiles = []
        self.currentIndex = 0
    
        for file in files:
            if ".aif" in file.lower():
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
        print 'Albums:: Starting Init'
        self.core = core
        self.audio = audio
        self.video = video
        self.input = input
        self.local = False
        self.menu = 0
        self.cursorPosition = 0
        self.currentFileName = ""
        self.g = 0
        self.currentIndex = 0
        self.lastDirectories = [Config.OP1USBMountDir + "/album"]
        self.volume = self.audio.GetVolume()

        self.op1Present = self.core.IsUSBDeviceConnected(Config.OP1USBVendor, Config.OP1USBProduct)
        
        if self.op1Present:
            # create mount directory if it doesn't exist
            self.core.ForceDirectory(Config.OP1USBMountDir)
            # get usb drive mount path
            self.mountpath = self.core.GetUSBMountPath(Config.OP1USBId)
            print(" > OP-1 device path: %s" % self.mountpath)
            # mount it!
            self.core.MountDevice(self.mountpath, Config.OP1USBMountDir)
            # load contents
            self.loadDirectoryData(self.lastDirectories[0]);

    def Dispose(self):
        pass

    def Update(self):
        self.g = self.g + 1
        if (self.g > 255):
            self.g = 0

    def InputUpdate(self, k1, k2, k3, ku, kd, kl, kr, kp):

        if self.op1Present:

            if self.menu == 1:
                if ku:
                    phraseList = list(self.currentFileName)
                    char = phraseList[self.cursorPosition]
                    charIndex = Config.ValidFilenameCharacters.index(char)
                    charIndex += 1;
                    if charIndex >= len(Config.ValidFilenameCharacters):
                        charIndex = 0
                    phraseList[self.cursorPosition] = Config.ValidFilenameCharacters[charIndex]
                    self.currentFileName = "".join(phraseList)

                elif kd:
                    phraseList = list(self.currentFileName)
                    char = phraseList[self.cursorPosition]
                    charIndex = Config.ValidFilenameCharacters.index(char)
                    charIndex -= 1;
                    if charIndex < 0:
                        charIndex = len(Config.ValidFilenameCharacters) - 1
                    phraseList[self.cursorPosition] = Config.ValidFilenameCharacters[charIndex]
                    self.currentFileName = "".join(phraseList)

                elif kl:
                    self.cursorPosition -= 1

                elif kr:
                    self.cursorPosition += 1

                # cursor wrapping
                if (self.cursorPosition < 0):
                    self.cursorPosition = Config.MaxFilenameLength

                elif (self.cursorPosition > Config.MaxFilenameLength):
                    self.cursorPosition = 0
                    
                if k1:
                    # copy album local
                    self.menu = 2

                    self.video.DrawLargeText(
                        Config.PrimaryTextColor, 
                        (10, 10), 
                        "Copying!")

                    # ensure the target directory exists
                    currentObject = self.getObject(self.currentIndex)
                    path, file = self.core.SplitFilePathParts(currentObject)

                    if self.local:
                        targetDirectory = Config.OP1USBMountDir + "/album/"
                        path = path.replace(Config.MediaDirectory + "/albums/", "")
                    else:
                        targetDirectory = Config.MediaDirectory + "/albums/"
                        path = path.replace(Config.OP1USBMountDir + "/album/", "")

                    self.core.ForceDirectory(targetDirectory + path)

                    # copy
                    print("Albums:: Copying file " + currentObject)
                    print("Albums:: To " + targetDirectory + path + "/" + self.currentFileName)
                    self.core.CopyFile(
                        currentObject,
                        targetDirectory + path + "/" + self.currentFileName)

                    self.menu = 0

                if k2:
                    self.menu = 3
                    pass

                if k3:
                    # cancel action
                    self.menu = 0

            elif self.menu == 3:
                if k1:
                    currentObject = self.getObject(self.currentIndex)
                    self.core.DeleteFile(currentObject)
                    self.loadDirectoryData(self.lastDirectories[-1]);
                    self.menu = 0

                if k3:
                    self.menu = 0

            elif self.menu == 0:
                if ku:
                    self.currentIndex -= 1

                elif kd:
                    self.currentIndex += 1

                elif kl:
                    pass

                elif kr:
                    pass

                # cursor wrapping
                if (self.currentIndex < 0):
                    self.currentIndex = (len(self.currentDirectories) + len(self.currentFiles)) - 1

                elif (self.currentIndex > (len(self.currentDirectories) + len(self.currentFiles))):
                    self.currentIndex = 0

                if k1:
                    objectType = self.getObjectType(self.currentIndex)
                    currentObject = self.getObject(self.currentIndex)
                    
                    if objectType == "Directory":
                        self.lastDirectories.append(currentObject)
                        self.loadDirectoryData(currentObject);

                    elif objectType == "File":
                        path, file = self.core.SplitFilePathParts(currentObject)
                        self.currentFileName = file
                        self.cursorPosition = 0
                        self.menu = 1

                if k2:
                    if self.local:
                        self.local = False
                        self.lastDirectories = [Config.OP1USBMountDir + "/album"]
                    
                    else:
                        self.local = True
                        self.lastDirectories = [Config.MediaDirectory + "/albums"]
                    
                    self.loadDirectoryData(self.lastDirectories[0]);

                if k3:
                    if len(self.lastDirectories) == 1:
                        self.core.UnmountDevice(Config.OP1USBMountDir)
                        from Scenes.MainMenu import *
                        self.core.ChangeScene(MainMenu)
                        
                    else:
                        self.lastDirectories.pop()
                        self.loadDirectoryData(self.lastDirectories[-1])

        elif self.op1Present == False:
            if k1 or k2 or k3:
                from Scenes.MainMenu import *
                self.core.ChangeScene(MainMenu)

    def Draw(self):
        indexColor = (100, self.g, 100)
        line = 0

        if self.op1Present:

            if self.menu == 0:
                # draw entries
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

                # draw volume
                volumeBar = ""

                for i in range(0, int(self.volume * 10)):
                    volumeBar += "|"
                
                self.video.DrawSmallText(
                    Config.PrimaryTextColor, 
                    (10, 115), 
                    str(len(self.currentDirectories)) + "," + str(len(self.currentFiles)) + " : " + volumeBar)

            elif self.menu == 1:

                if self.local:
                    self.video.DrawSmallText(
                        indexColor, 
                        (10, 10), 
                        "Copy to OP1")
                else:
                    self.video.DrawSmallText(
                        indexColor, 
                        (10, 10), 
                        "Copy Local")

                self.video.DrawSmallText(
                    indexColor, 
                    (10, 22), 
                    "Delete")

                self.video.DrawSmallText(
                    indexColor, 
                    (10, 34), 
                    "Cancel")

                phraseList = list(self.currentFileName)
                newPhraseList = []
                
                for index, char in enumerate(phraseList):
                    if (index == self.cursorPosition):
                        newPhraseList.append("[")
                        newPhraseList.append(phraseList[index])
                        newPhraseList.append("]")
                    else:
                        newPhraseList.append(phraseList[index])

                self.video.DrawLargeText(
                    Config.PrimaryTextColor, 
                    (10, 100), 
                    "".join(newPhraseList))

            elif self.menu == 2:
    
                self.video.DrawLargeText(
                    indexColor, 
                    (10, 10), 
                    "Copying!")

            elif self.menu == 3:
        
                self.video.DrawLargeText(
                    indexColor, 
                    (10, 10), 
                    "Delete?")

        else:
            self.video.DrawLargeText(
                indexColor, 
                (10, 10), 
                "OP1 Drive")

            self.video.DrawLargeText(
                indexColor, 
                (10, 25), 
                "Not Present!")

            self.video.DrawSmallText(
                Config.PrimaryTextColor, 
                (10, 40), 
                "Return to the menu,")

            self.video.DrawSmallText(
                Config.PrimaryTextColor, 
                (10, 48), 
                "plug in the OP1")

            self.video.DrawSmallText(
                Config.PrimaryTextColor, 
                (10, 56), 
                "and try again.")
