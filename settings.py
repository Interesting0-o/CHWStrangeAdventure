import json

import pygame
class Settings:

    screen_size = [
        (3840,2160),
        (1920,1080),
        (1600,900),
        (1280,720),
    ]
    screen_set = [
        0,                                      #窗口模式
        pygame.FULLSCREEN | pygame.HWSURFACE    #全屏模式
    ]
    GAME_VERSION = "0.1.0"
    FPS = 60
    TITLE_SIZE = 24
    FONT_SIZE = 20
    ORANGE = "#FFA500"

    def __init__(self):
        pass

if __name__ == '__main__':
    file = open("settings.json", "r",encoding="utf-8")
    settings = json.load(file)
    print(settings["frame_settings"]["screen_size_index"])