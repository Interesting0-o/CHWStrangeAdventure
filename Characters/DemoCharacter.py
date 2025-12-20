import pygame
from Characters.Character import Character
from ResourceLoader import ResourceLoader

class DemoCharacter(Character):



    def __init__(self):
        super().__init__()
        self.name = "DemoCharacter"
        self.emotions = {
            "neutral":ResourceLoader.demo_character_dict["neutral"],
            "happy":ResourceLoader.demo_character_dict["happy"],
            "mad":ResourceLoader.demo_character_dict["mad"]
        }
        self.Id = "DC"
        self.name_surface = ResourceLoader.font_dict["MiSansDemibold36"].render(self.name+":", True, (255, 255, 255))

    def __str__(self):
        return self.name



