from ResourceLoader import ResourceLoader
import pygame

class Player:
    def __init__(self):
        self.name = None
        self.honer_value = 0
        self.name_surface = None

    def init_name_surface(self):
        self.name_surface = ResourceLoader.font_MiSans_Demibold24.render(self.name+":" ,True, (255, 255, 255))

