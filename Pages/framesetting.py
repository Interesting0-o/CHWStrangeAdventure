import pygame
from Elements.DropdownMenu import DropdownMenu
from Pages.Page import Page


class FrameSetting(Page):


    def __init__(self):
        super().__init__()
        #背景声明
        self.fullscreen_menu = None
        self.tar_location = None
        self.bg_surface_rect = None
        self.bg_surface = None
        #字体导入
        self.font = pygame.font.Font(self.path[:-6] + r"/resource/font/MiSans/MiSans-Demibold.ttf", 24)
        self.text_resolution = self.font.render("分辨率:", True, (0, 0, 0))
        self.text_resolution_rect = self.text_resolution.get_rect(topleft =(30,self.window_height * 0.07))
        self.text_fullscreen = self.font.render("全屏选项:", True, (0, 0, 0))
        self.text_fullscreen_rect = self.text_fullscreen.get_rect(topleft =(30,self.window_height * 0.13))
        #全屏设置列表
        self.fullscreen_list = [
            "窗口化",
            "全屏",
        ]
        #分辨率设置列表
        self.resolution_list = [
            "3840x2160",
            "1920x1080",
            "1600x900",
            "1280x720",
            "800x600",
        ]

        #全屏设置下拉菜单初始化
        self.fullscreen_menu = DropdownMenu(
            self.fullscreen_list,
            (150, 30),
            2,
            self.font,
            auto_index = 0,
        )


        #分辨率设置下拉菜单初始化
        self.resolution_menu = DropdownMenu(
            self.resolution_list,
            (150, 30),
            5,
            self.font,
            auto_index = 3,
        )









    def init(self,
             location:tuple[int,int] = (0,0),
             ):

        #背景设置
        self.bg_surface = pygame.surface.Surface((
          self.window_width * 0.6,
            self.window_height * 0.7
        ))
        self.bg_surface_rect = self.bg_surface.get_rect(topleft = location)
        self.tar_location = (int(self.bg_surface_rect.width *0.8),int(self.bg_surface_rect.height *0.1))
        self.bg_surface.fill((255, 255, 255))
        #下拉菜单初始化
        self.resolution_menu.init(self.tar_location)
        self.fullscreen_menu.init((self.tar_location[0],int(self.bg_surface_rect.height *0.18)))







    def draw(self,
             mouse_down:bool,
             location:tuple[int,int] = (0,0),
             # screen: pygame.Surface, #当前屏幕
             ):
        self.bg_surface.fill((255, 255, 255))


        #全屏设置
        self.bg_surface.blit(self.text_fullscreen, self.text_fullscreen_rect)
        self.fullscreen_menu.draw(
            self.bg_surface,
            location,
            mouse_down,
            (self.tar_location[0],int(self.bg_surface_rect.height *0.18))
        )

        #分辨率设置
        self.bg_surface.blit(self.text_resolution, self.text_resolution_rect)
        self.resolution_menu.draw(
            self.bg_surface,
            location,
            mouse_down,
            self.tar_location
        )







if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    frame_setting = FrameSetting()
    frame_setting.init((100,100))
    clock = pygame.time.Clock()

    while True:
        mouse_down = False
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
        screen.fill("black")
        screen.blit(frame_setting.bg_surface, frame_setting.bg_surface_rect)
        frame_setting.draw(mouse_down, (100,100))




        pygame.display.update()