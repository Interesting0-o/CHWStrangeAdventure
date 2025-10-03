import pygame
from Characters.Character import Character
from ResourceLoader import ResourceLoader

class DemoCharacter(Character):



    def __init__(self):
        super().__init__()
        self.name = "DemoCharacter"
        self.emotions = {
            "neutral":ResourceLoader.demo_character_neutral,
        }
        self.Id = "DC"

    def __str__(self):
        return self.name



