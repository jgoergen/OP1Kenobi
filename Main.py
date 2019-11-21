# system imports
import sys
import time,os,datetime
import shutil as sh

# resources
from Config import *
from Resources.Colors import *

# services
from Services.Audio import *
from Services.Video import *
from Services.Core import *
from Services.Input import *

# scenes
from Scenes.MainMenu import *

# initialize
print 'Main:: Starting Init'
core = Core()

video = Video(
    Config.DisplayWidth,
    Config.DisplayHeight,
    Config.FontFile,
    Config.LargeFontSize,
    Config.SmallFontSize)

audio = Audio(core)

input = Input(
    Config.Key1Pin,
    Config.Key2Pin,
    Config.Key3Pin,
    Config.KeyUpPin,
    Config.KeyDownPin,
    Config.KeyLeftPin,
    Config.KeyRightPin,
    Config.KeyPressPin)

def Main():
    print 'Main:: Starting Main'
    global core
    global video
    global audio
    global input

    core.RegisterServices(video, audio, input)
    core.ChangeScene(MainMenu)
    lastDisplayUpdateTime = 0
    lastInputUpdateTime = 0
    core.running = True

    while core.running:
        core.Update()
        core.currentScene.Update()

        if (core.GetTime() - lastDisplayUpdateTime > Config.DisplayUpdateSpeed):
            lastDisplayUpdateTime = core.GetTime()
            video.FillScreen(Colors.Black)
            core.currentScene.Draw()            

        if (core.GetTime() - lastInputUpdateTime > Config.InputUpdateSpeed):
            lastInputUpdateTime = core.GetTime()
            core.currentScene.InputUpdate(
                input.KeyDown(Config.Key1Pin),
                input.KeyDown(Config.Key2Pin),
                input.KeyDown(Config.Key3Pin),
                input.KeyDown(Config.KeyUpPin),
                input.KeyDown(Config.KeyDownPin),
                input.KeyDown(Config.KeyLeftPin),
                input.KeyDown(Config.KeyRightPin),
                input.KeyDown(Config.KeyPressPin))

        video.Update()
        audio.Update()
        
def Intro():
    print 'Main:: Starting Intro'
    global core
    global video
    global audio

    video.FillScreen(Colors.Black)

    video.DrawLargeText(
        Config.PrimaryTextColor, 
        (10, 10), 
        'Intro!')

    video.Update()
        
    # TODO: Intro screen

if __name__ == '__main__':
    Intro()
    Main()
    pygame.quit()
    sys.exit()