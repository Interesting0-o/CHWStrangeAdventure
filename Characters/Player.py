from ResourceLoader import ResourceLoader
import pygame

class Player:
    def __init__(self):
        self.name = None
        # 使用与存档和 ResourceLoader 一致的字段名
        self.honor_value = 0
        self.name_surface = None

    def init_name_surface(self):
        # ResourceLoader 将字体保存在 font_dict，键为 "MiSansDemibold24"
        font = ResourceLoader.font_dict.get("MiSansDemibold24")
        if font:
            self.name_surface = font.render(self.name+":" ,True, (255, 255, 255))
        else:
            # 回退到默认字体
            self.name_surface = pygame.font.SysFont(None, 24).render(self.name+":", True, (255,255,255))

