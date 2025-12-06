import pygame
pygame.mixer.init()


class Voice:

    char_channel = pygame.mixer.Channel(0)

    effect_channel = pygame.mixer.Channel(1)


    def __init__(self)->None:
        pass
