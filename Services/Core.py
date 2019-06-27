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
        print 'Core:: Starting Init'
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
        print 'Core:: Changing scene'
        
        if (Core.currentScene):
            Core.currentScene.Dispose()

        Core.currentScene = scene(self, self.audio, self.video, self.input)

    def GetTime(self):
        return time.get_ticks()

    def RunCommand(self, cmd):
    	p = Popen(
            cmd, 
            shell = True, 
            stdout = PIPE)
        return p.communicate()[0]

    def IsUSBDeviceConnected(self, vendor, product):
      return usb.core.find(
          idVendor = vendor, 
          idProduct = product) is not None

    def GetUSBMountPath(self, usbId):
        o = os.popen('readlink -f /dev/disk/by-id/' + usbId).read()

        if usbId in o:
            raise RuntimeError("Error getting OP-1 mount path: {}".format(o))
        else:
            return o.rstrip()

    def MountDevice(self, source, target):
        ret = os.system('mount {} {}'.format(source, target))
        
        if ret not in (0, 8192):
            raise RuntimeError("Error mounting {} on {}: {}".format(source, target, ret))

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
            #if filename.endswith(".atm") or filename.endswith(".py"): 
            
        tapeList.sort()

    def SplitFilePathParts(self, filePath):
        head, tail = os.path.split(filePath)
        return head, tail

    def CopyFile(self, sourcePath, destinationPath):
        sh.copy(sourcePath, destinationPath)

    def DeleteFile(self, sourcePath):
        os.remove(sourcePath)

    def CopyFolder(self, sourcePath, destinationPath, symlinks=False, ignore=None):
        ct=0
        # print str(len(os.listdir(src))) + " files to move"

        try:
            for item in os.listdir(sourcePath):
                s = os.path.join(sourcePath, item)
                d = os.path.join(destinationPath, item)

                if os.path.isdir(destinationPath) == 0:
                    os.mkdir(destinationPath)
                if os.path.isdir(s):
                    sh.copytree(s, d, symlinks, ignore)
                else:
                    sh.copy(s, d)
                    ct += 1
                    print "Core:: File " + str(ct) + " moved"
        except:
            print "Core:: Must be an error. file full or smt"

    def GetDataInDirectory(self, path):
        print 'Core:: Loading directory information for ' + path

        files = []
        directories = []

        for (dirpath, dirnames, filenames) in walk(path):
            for name in dirnames:
                directories.append(os.path.join(dirpath, name))
            del dirnames[:]
            for name in filenames:
                files.append(os.path.join(dirpath, name))
        
        print 'Core:: Returning ' + str(len(files)) + ' files and ' + str(len(directories)) + ' directories'

        return (files, directories)
