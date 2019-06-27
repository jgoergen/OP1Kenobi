import os
import pygame
import pygame.freetype

class Video():
    screen = None
    largeFont = None
    smallFont = None

    def __init__(self, width, height, fontFile, largeFontSize, smallFontSize):
        print 'Video:: Starting Init ' + str(width) + ' ' + str(height) 
        Video.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        pygame.mouse.set_visible(0)
        pygame.font.init()
        Video.largeFont = pygame.freetype.Font(fontFile, largeFontSize)
        Video.smallFont = pygame.freetype.Font(fontFile, smallFontSize)

    def Update(self):
        pygame.display.flip()
        # pygame.display.update()
        
    def DrawLargeText(self, color, position, text):
        Video.largeFont.render_to(
            Video.screen, 
            position, 
            text, 
            color)
    
    def DrawSmallText(self, color, position, text):
        Video.smallFont.render_to(
            Video.screen, 
            position, 
            text, 
            color)

    def FillScreen(self, color):
        Video.screen.fill(color)