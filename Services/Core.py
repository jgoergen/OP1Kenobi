# system imports
import os
import usb.core
import pygame
from pygame import time
from os import walk
from subprocess import Popen, PIPE, STDOUT
import shutil as sh


class Core():

    currentScene = None
    audio = None
    video = None
    input = None

    def __init__(self):
        print('Core:: Starting Init')
        self.running = False
        pygame.init()

    def RegisterServices(self, video, audio, input):
        self.audio = audio
        self.video = video
        self.input = input

    def Update(self):
        pygame.event.poll()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def Quit(self):
        self.running = false

    def ChangeScene(self, scene):
        print('Core:: Changing scene')

        if (Core.currentScene):
            Core.currentScene.Dispose()

        Core.currentScene = scene(self, self.audio, self.video, self.input)

    def GetTime(self):
        return time.get_ticks()

    def RunCommand(self, cmd):
        p = Popen(
            cmd,
            shell=True,
            stdout=PIPE)
        return p.communicate()[0]

    def Shutdown(self):
        self.RunCommand('sudo shutdown -h now')

    def Reboot(self):
        self.RunCommand('sudo reboot')

    def IsUSBDeviceConnected(self, vendor, product):
        return usb.core.find(
            idVendor=vendor,
            idProduct=product) is not None

    def GetUSBMountPath(self, usbId):
        o = os.popen('readlink -f /dev/disk/by-id/' + usbId).read()

        if usbId in o:
            raise RuntimeError('Error getting OP-1 mount path: {}'.format(o))
        else:
            return o.rstrip()

    def MountDevice(self, source, target):
        ret = os.system('mount {} {}'.format(source, target))

        if ret not in (0, 8192):
            raise RuntimeError(
                "Error mounting {} on {}: {}".format(source, target, ret))

    def UnmountDevice(self, target):
        ret = os.system('umount {}'.format(target))

        if ret != 0:
            raise RuntimeError("Error unmounting {}: {}".format(target, ret))

    def ForceDirectory(self, path):
        if not os.path.isdir(path):
            os.makedirs(path)

    def GetFilesInDirectory(self, path):
        for filename in os.listdir(path):
            fullPath = path + filename
            tapeList.append([filename, fullPath])
            # if filename.endswith(".atm") or filename.endswith(".py"):

        tapeList.sort()

    def SplitFilePathParts(self, filePath):
        head, tail = os.path.split(filePath)
        return head, tail

    def CopyFile(self, sourcePath, destinationPath):
        sh.copy(sourcePath, destinationPath)

    def DeleteFile(self, sourcePath):
        os.remove(sourcePath)

    def DeleteFolder(self, sourcePath):
        print("Core:: Deleting directory")
        print(sourcePath)
        if os.path.exists(sourcePath):
            sh.rmtree(sourcePath)
        else:
            print("Core:: Directory doesnt exist, ignoring.")

    def getNormPath(self, path):
        return os.path.basename(os.path.normpath(path))

    def CopyFolder(self, src, dst, symlinks=False, ignore=None):
        print("Core:: Copying " + src + " to " + dst)

        if not os.path.exists(dst):
            print("Core:: Creating destination directory.")
            os.makedirs(dst)
            sh.copystat(src, dst)

        lst = os.listdir(src)

        if ignore:
            excl = ignore(src, lst)
            lst = [x for x in lst if x not in excl]

        for item in lst:
            s = os.path.join(src, item)
            d = os.path.join(dst, item)

            if symlinks and os.path.islink(s):
                if os.path.lexists(d):
                    os.remove(d)

                print('Core:: Creating Symlink')
                os.symlink(os.readlink(s), d)

                try:
                    st = os.lstat(s)
                    mode = stat.S_IMODE(st.st_mode)
                    os.lchmod(d, mode)

                except:
                    print('Core:: lchmod not available')
                    pass

            elif os.path.isdir(s):
                self.CopyFolder(s, d, symlinks, ignore)

            else:
                print('Core:: Copying file ' + d)
                sh.copy2(s, d)

    def GetDataInDirectory(self, path):
        print('Core:: Loading directory information for ' + path)

        files = []
        directories = []

        for (dirpath, dirnames, filenames) in walk(path):
            for name in dirnames:
                directories.append(os.path.join(dirpath, name))
            del dirnames[:]
            for name in filenames:
                files.append(os.path.join(dirpath, name))

        print('Core:: Returning ' + str(len(files)) +
              ' files and ' + str(len(directories)) + ' directories')

        return (files, directories)
