import pygame
from settings import *
from deletePyFile.player import Player

class Level:

    def __init__(self):
        """
        获取显示表面并初始化
        """
        self.player = None
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.setup()

    def setup(self):
        self.player = Player((640, 360), self.all_sprites)



    def run (self,dt):
        self.display_surface.fill("black")
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)
