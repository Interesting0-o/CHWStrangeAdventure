import pygame
from Elements.Button import Button
from Elements.DropdownMenu import DropdownMenu
from Pages.Page import Page
import settings

class FrameSetting(Page):


    def __init__(self):
        super().__init__()
        #字体导入
        self.font = pygame.font.Font(self.path[:-6] + r"/resource/font/MiSans/MiSans-Demibold.ttf", 24)
        self.text_resolution = self.font.render("分辨率", True, (0, 0, 0))
        self.text_resolution_rect = self.text_resolution.get_rect()
        self.text_fullscreen = self.font.render("全屏", True, (0, 0, 0))
        print(self.path[:-6])
        #分辨率设置列表
        self.resolution_list = [
            "3840x2160",
            "1920x1080",
            "1600x900",
            "1280x720",
            "800x600",
        ]
        #分辨率设置下拉菜单
        self.resolution_menu = DropdownMenu(

        )




    def init(self):
        self.display_surface = pygame.display.get_surface()




    def draw(self):
        #分辨率设置
        self.display_surface.blit(self.text_resolution, self.text_resolution_rect)





if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    frame_setting = FrameSetting()
    frame_setting.init()
    clock = pygame.time.Clock()

    while True:

        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill((255, 255, 255))
        frame_setting.draw()




        pygame.display.update()