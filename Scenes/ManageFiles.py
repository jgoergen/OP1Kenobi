# resources
from Config import *
from Resources.Colors import *

# services
from Services.Audio import *
from Services.Video import *
from Services.Core import *
from Services.Input import *
from Services.PhraseInput import *

# scenes
from Scenes.MainMenu import *
from Scenes.MainMenu import *


class ManageFiles():
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
        print('ManageFiles:: Starting Init')
        self.core = core
        self.audio = audio
        self.video = video
        self.input = input
        self.local = False
        self.menu = 0
        self.g = 0
        self.currentIndex = 0
        self.lastDirectories = [Config.OP1USBMountDir + "/"]
        self.volume = self.audio.GetVolume()
        self.phraseInput = PhraseInput()

        self.op1Present = self.core.IsUSBDeviceConnected(
            Config.OP1USBVendor, Config.OP1USBProduct)

        if self.op1Present:
            # create mount directory if it doesn't exist
            self.core.ForceDirectory(Config.OP1USBMountDir)
            # get usb drive mount path
            self.mountpath = self.core.GetUSBMountPath(Config.OP1USBId)
            print(' > OP-1 device path: %s' % self.mountpath)
            # mount it!
            self.core.MountDevice(self.mountpath, Config.OP1USBMountDir)
            # load contents
            self.loadDirectoryData(self.lastDirectories[0])

    def Dispose(self):
        pass

    def Update(self):
        self.g = self.g + 1
        if (self.g > 255):
            self.g = 0

    def CopyFiles(self):
        self.menu = 2

        self.video.DrawLargeText(
            Config.PrimaryTextColor,
            (10, 10),
            "Copying!")

        # ensure the target directory exists
        currentObject = self.getObject(self.currentIndex)
        path, file = self.core.SplitFilePathParts(currentObject)

        if self.local:
            targetDirectory = Config.OP1USBMountDir + "/"
            path = path.replace(Config.MediaDirectory + "/", "")
        else:
            targetDirectory = Config.MediaDirectory + "/"
            path = path.replace(Config.OP1USBMountDir + "/", "")

        self.core.ForceDirectory(targetDirectory + path)

        # copy
        print("ManageFiles:: Copying file " + currentObject)
        print("ManageFiles:: To " + targetDirectory +
              path + "/" + self.phraseInput.phrase)
        self.core.CopyFile(
            currentObject,
            targetDirectory + path + "/" + self.phraseInput.phrase)

        self.menu = 0

    def ChangeMenuIndex(self, delta):
        self.currentIndex += delta

        # cursor wrapping
        if (self.currentIndex < 0):
            self.currentIndex = (
                len(self.currentDirectories) + len(self.currentFiles)) - 1

        elif (self.currentIndex > (len(self.currentDirectories) + len(self.currentFiles))):
            self.currentIndex = 0

    def GoBack(self):
        if len(self.lastDirectories) == 1:
            self.core.UnmountDevice(Config.OP1USBMountDir)
            self.core.ChangeScene(MainMenu)

        else:
            self.lastDirectories.pop()
            self.loadDirectoryData(self.lastDirectories[-1])

    def SwitchContext(self):
        # changes between local and the OP1
        if self.local:
            self.local = False
            self.lastDirectories = [Config.OP1USBMountDir + "/"]

        else:
            self.local = True
            self.lastDirectories = [Config.MediaDirectory + "/"]

        self.loadDirectoryData(self.lastDirectories[0])

    def SelectItem(self):
        objectType = self.getObjectType(self.currentIndex)
        currentObject = self.getObject(self.currentIndex)
        path, file = self.core.SplitFilePathParts(currentObject)

        if objectType == "Directory":
            self.lastDirectories.append(currentObject)
            self.loadDirectoryData(currentObject)

        elif objectType == "File":
            self.phraseInput.phrase = file
            self.phraseInput.cursorPosition = 0
            self.menu = 1

    def DeleteItem(self):
        currentObject = self.getObject(self.currentIndex)
        self.core.DeleteFile(currentObject)
        self.loadDirectoryData(self.lastDirectories[-1])
        self.menu = 0

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

        if self.op1Present:

            if self.menu == 1:
                if ku:
                    self.phraseInput.ChangePhraseCharacter(1)

                elif kd:
                    self.phraseInput.ChangePhraseCharacter(-1)

                elif kl:
                    self.phraseInput.ChangePhraseCursorPosition(-1)

                elif kr:
                    self.phraseInput.ChangePhraseCursorPosition(1)

                if k1:
                    self.CopyFiles()

                if k2:
                    self.menu = 3
                    pass

                if k3:
                    # cancel action
                    self.menu = 0

            elif self.menu == 3:
                if k1:
                    self.DeleteItem()

                if k3:
                    self.menu = 0

            elif self.menu == 0:
                if ku:
                    self.ChangeMenuIndex(-1)

                elif kd:
                    self.ChangeMenuIndex(1)

                if k1:
                    self.SelectItem()

                if k2:
                    self.SwitchContext()

                if k3:
                    self.GoBack()

        elif self.op1Present == False:
            if k1 or k2 or k3:
                self.core.ChangeScene(MainMenu)

    def Draw(self):
        indexColor = (100, self.g, 100)
        line = 0

        if self.op1Present:
            if self.menu == 0:
                self.DrawEntries(indexColor)
                self.DrawVolume()

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

                self.video.DrawLargeText(
                    Config.PrimaryTextColor,
                    (10, 100),
                    self.phraseInput.GetPhrase())

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
