from Pages.Page import Page
from Elements.Button import Button
from Pages.framesetting import FrameSetting

import pygame
class SettingsPage(Page):
    """
    游戏设置页面
    """

    def __init__(self,fullscreen_auto_index:int,resolution_auto_index:int):
        super().__init__()

        #黑场专场内容
        self.black_surface = None
        self.black_surface_alpha = 0
        self.is_black_end = False
        # 背景读取
        self.bg_copy = None  # 实际上使用的背景
        self.bg = pygame.image.load(self.path[:-6]+r"/resource/img/bg/SettingsPageBG.png") #作为资源
        self.bg_h = -60
        self.bg_alpha = 0

        #关闭按钮初始化
        self.close_button = Button(
            pygame.image.load(
                self.path[:-6]+r"/resource/img/button/close_button/Close_button.png"))
        for i in range(30):
            self.close_button.animation_list.append(pygame.image.load(
                self.path[:-6] + rf"/resource/img/button/close_button/Close_button_{i:02d}.png"
            ))
        self.close_button_value = False


        #画面设置按钮初始化
        self.frame_button = Button(
            pygame.image.load(
                self.path[:-6] + r"/resource/img/button/frame_setting_button/Frame_setting_button_01.png"
            ))

        for i in range(30):
            self.frame_button.animation_list.append(pygame.image.load(
                self.path[:-6] + rf"/resource/img/button/frame_setting_button/Frame_setting_button_{i:02d}.png"
            ))
        self.isFrameSetting = False

        #画面设置页面
        self.frame_setting = FrameSetting(fullscreen_auto_index,resolution_auto_index)

        #黑场进行设置
        self.black_surface = pygame.Surface((self.window_width, self.window_height))
        self.black_surface.fill((0, 0, 0))
        self.black_surface_alpha = 0

    def init(self):
        """
        重载内容
        :return:
        """
        #黑场初始化
        self.black_surface = pygame.Surface((self.window_width, self.window_height))
        self.black_surface.set_alpha(self.black_surface_alpha)
        #背景初始化
        self.display_surface = pygame.display.get_surface()

        #使用bg_copy作为背景
        self.bg_copy = pygame.transform.scale(self.bg, (self.window_width, self.window_height))
        self.bg_copy.set_alpha(self.bg_alpha)

        #关闭按钮重置

        self.close_button.rect = self.close_button.image.get_rect()
        self.close_button.rect.left = int(self.window_width * 0.86)
        self.close_button.rect.top = int(self.window_height * 0.07)
        self.bg_copy.blit(self.close_button.image, self.close_button.rect)


        #画面设置按钮初始化
        self.frame_button.rect.left = int(self.window_width * 0.15)
        self.frame_button.rect.top = int(self.window_height * 0.2)
        self.bg_copy.blit(self.frame_button.image, self.frame_button.rect)


        #画面设置页面初始化
        self.frame_setting.init((int(0.3125*self.window_width),int(0.2*self.window_height)))
        self.frame_setting.bg_surface_rect.topleft = (int(0.3125*self.window_width),int(0.2*self.window_height))

    def draw(self,
             mouse_down:bool, #鼠标按下状态
             ):

        #黑场进入
        if not self.close_button_value:
            if self.black_surface_alpha <120:
                self.black_surface_alpha += 10
                self.black_surface.set_alpha(self.black_surface_alpha)
                self.bg_h += 5
                self.bg_alpha += 21
                self.bg_copy.set_alpha(self.bg_alpha)
                print(self.bg_alpha)
        else :
            #设置页面消失动画
            if self.black_surface_alpha > 0:
                self.black_surface_alpha -= 10
                self.black_surface.set_alpha(self.black_surface_alpha)
                self.bg_h -= 5
                self.bg_alpha -= 21
                print(self.bg_alpha)
                self.bg_copy.set_alpha(self.bg_alpha)
                if self.bg_alpha <= 0:
                    self.is_end = True

        #按钮渲染
        self.close_button.hover_animation_blit((0,0))
        self.bg_copy.blit(self.close_button.image, self.close_button.rect)


        #画面元素渲染
        self.display_surface.blit(self.black_surface, (0, 0))
        self.display_surface.blit(self.bg_copy, (0, self.bg_h))
        #画面设置页面渲染
        if self.frame_button.setting_mode == 1:
            self.bg_copy.blit(self.frame_setting.bg_surface,
                              (400/1280*self.window_width,150/720*self.window_height))
            self.frame_setting.draw(mouse_down,
                                    (int(0.3125*self.window_width),int(0.2*self.window_height))
                                    )

        #按钮渲染
        self.frame_button.setting_button_animation(mouse_down)
        self.bg_copy.blit(self.frame_button.image, self.frame_button.rect)
        #按钮事件处理
        if self.close_button.is_pressed_blit((0,self.bg_h)):
            self.close_button_value = True


if __name__ == '__main__':

    from Page import Page



    pygame.init()
    settings_page = SettingsPage()
    screen = pygame.display.set_mode((settings_page.window_width, settings_page.window_height))
    screen.fill("white")
    clock = pygame.time.Clock()

    settings_page.init()

    while True:
        mouse_down = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
        screen.fill("white")
        settings_page.draw( mouse_down )

        clock.tick(60)
        pygame.display.update()

