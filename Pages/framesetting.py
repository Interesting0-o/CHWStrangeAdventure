import pygame
from Elements.DropdownMenu import DropdownMenu
from Elements.MenuButton import MenuButton
from Pages.Page import Page
from settings import Settings


class FrameSetting(Page):

    def __init__(self,fullscreen_auto_index:int,resolution_auto_index:int):
        self.isSettingsChange = False #是否修改设置
        super().__init__()
        #背景声明
        self.tar_location = None
        self.bg_surface_rect = None
        self.bg_surface = None
        #字体导入
        self.font = pygame.font.Font(self.path[:-6] + r"/resource/font/MiSans/MiSans-Demibold.ttf", 24)
        self.font2 = pygame.font.Font(self.path[:-6] + r"/resource/font/MiSans/MiSans-Demibold.ttf", 34)
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
        ]

        #全屏设置下拉菜单初始化
        self.fullscreen_menu_current_option = fullscreen_auto_index
        self.fullscreen_menu = DropdownMenu(
            self.fullscreen_list,
            (150, 30),
            2,
            self.font,
            auto_index = self.fullscreen_menu_current_option,
        )


        #分辨率设置下拉菜单初始化
        self.resolution_menu_current_option = resolution_auto_index
        self.resolution_menu = DropdownMenu(
            self.resolution_list,
            (150, 30),
            4,
            self.font,
            auto_index = self.resolution_menu_current_option,
        )
        #设置保存按钮
        self.save_button_bg = pygame.Surface((210,35)) #未选中状态
        self.save_button_bg.fill("white")
        self.save_text = self.font2.render("保存当前设置", True, "#FFA500")
        self.save_button_bg.blit(self.save_text,
                                 self.save_text.get_rect(center = self.save_button_bg.get_rect().center))
        self.save_button_hover_bg = pygame.Surface((210,35)) #鼠标悬停状态
        self.save_button_hover_bg.fill("#FFA500")
        self.save_text_hover = self.font2.render("保存当前设置", True, "white")
        self.save_button_hover_bg.blit(self.save_text_hover,
                                        self.save_text_hover.get_rect(center = self.save_button_hover_bg.get_rect().center))
        self.save_button = MenuButton(#实例化按钮
            self.save_button_bg,
            self.save_button_hover_bg,
            self.save_button_bg.get_rect(center = (self.window_width*0.5*0.6,self.window_height*0.8*0.7))
        )

    def init(self,
             location:tuple[int,int] = (0,0),       #bg_surface位置
             ):

        #背景设置
        self.bg_surface = pygame.surface.Surface((
          self.window_width * 0.6,
            self.window_height * 0.6
        ))
        self.bg_surface_rect = self.bg_surface.get_rect(topleft = location)
        self.tar_location = (int(self.bg_surface_rect.width *0.8),int(self.bg_surface_rect.height *0.1))
        self.bg_surface.fill((255, 255, 255))
        #下拉菜单初始化
        self.resolution_menu.init(self.tar_location)
        self.fullscreen_menu.init((self.tar_location[0],int(self.bg_surface_rect.height *0.18)))
        #保存设置按钮初始化
        self.save_button.rect.center = (self.window_width*0.5*0.6,self.window_height*0.8*0.6)

    def draw(self,
             mouse_down:bool,
             # current_screen:pygame.Surface, #当前屏幕
             location:tuple[int,int] = (0,0),#bg_surface位置
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

        #保存设置按钮
        self.save_button.hover_animation_blit(self.bg_surface_rect.topleft)
        self.bg_surface.blit(self.save_button.img, self.save_button.rect)

        #保存修改
        if self.save_button.is_pressed_blit(self.bg_surface_rect.topleft):
            self.isSettingsChange = True
            # current_screen = pygame.display.set_mode(Settings.screen_size[self.resolution_menu.get_index()],
            #                                  flags =Settings.screen_set[self.fullscreen_menu.get_index()])
            # self.set_window_size(Settings.screen_size[self.resolution_menu.get_index()][0],
            #                       Settings.screen_size[self.resolution_menu.get_index()][1])
            # self.init(location)
        else:
            self.isSettingsChange = False

    def reset(self):
        pass

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    frame_setting = FrameSetting(0,0)
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
        frame_setting.draw(mouse_down,(100,100))




        pygame.display.update()