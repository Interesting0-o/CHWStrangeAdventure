import pygame
from Pages.Page import Page
from Elements.MenuButton import MenuButton
from ResourceLoader import ResourceLoader

class PausePage(Page):
    def __init__(self):
        super().__init__()


        #按钮初始化
        self.continue_button_value = False
        self.setting_button_value = False
        self.back_button_value = False
        self.load_button_value = False
        self.button_bg = None
        #黑场专场内容

        self.is_black_end = False
        self.black_surface_list = ResourceLoader.black_surfaces_list
        self.black_surface_index = 0

        # 背景读取
        self.bg = pygame.surface.Surface((360,470))
        pygame.draw.rect(self.bg, "white", (0, 0, 360, 470),border_radius=40)
        self.bg.set_colorkey("black")
        self.bg_copy = self.bg.copy()
        self.bg_h = -60
        self.bg_alpha = 0

        #按钮初始化
        self.button_bg = pygame.surface.Surface((300, 70))
        self.button_bg.fill("green")
        self.button_hover_bg = self.button_bg.copy()
        #按钮设置效果
        pygame.draw.rect(self.button_bg, "white", (0, 0, 300, 70), border_radius=20)
        pygame.draw.rect(self.button_bg, "orange", (0, 0, 300, 70), width=5, border_radius=20)

        pygame.draw.rect(self.button_hover_bg, "#ffd68c", (0, 0, 300, 70), border_radius=20)
        pygame.draw.rect(self.button_hover_bg, "orange", (0, 0, 300, 70), width=5, border_radius=20)

        #继续游戏按钮
        img_text = ResourceLoader.font_dict["MiSansDemibold36"].render("继续游戏", True, "orange")
        img_text_rect = img_text.get_rect(center=(150, 35))
        img_hover_text = ResourceLoader.font_dict["MiSansDemibold36"].render("继续游戏", True, "white")

        img = self.button_bg.copy()
        img.blit(img_text, img_text_rect)
        img.set_colorkey("green")

        img_hover = self.button_hover_bg.copy()
        img_hover.blit(img_hover_text, img_text_rect)
        img_hover.set_colorkey("green")
        self.continue_game_button = MenuButton(img, img_hover, img.get_rect())
        #设置按钮
        img_text = ResourceLoader.font_dict["MiSansDemibold36"].render("设置", True, "orange")
        img_text_rect = img_text.get_rect(center=(150, 35))
        img_hover_text = ResourceLoader.font_dict["MiSansDemibold36"].render("设置", True, "white")

        img = self.button_bg.copy()
        img.blit(img_text, img_text_rect)
        img.set_colorkey("green")

        img_hover = self.button_hover_bg.copy()
        img_hover.blit(img_hover_text, img_text_rect)
        img_hover.set_colorkey("green")
        self.setting_button = MenuButton(img, img_hover, img.get_rect())
        #返回标题按钮
        img_text = ResourceLoader.font_dict["MiSansDemibold36"].render("返回标题", True, "orange")
        img_text_rect = img_text.get_rect(center=(150, 35))
        img_hover_text = ResourceLoader.font_dict["MiSansDemibold36"].render("返回标题", True, "white")

        img = self.button_bg.copy()
        img.blit(img_text, img_text_rect)
        img.set_colorkey("green")

        img_hover = self.button_hover_bg.copy()
        img_hover.blit(img_hover_text, img_text_rect)
        img_hover.set_colorkey("green")
        self.back_button = MenuButton(img, img_hover, img.get_rect())
        #载入存档按钮
        img_text = ResourceLoader.font_dict["MiSansDemibold36"].render("载入存档", True, "orange")
        img_text_rect = img_text.get_rect(center=(150, 35))
        img_hover_text = ResourceLoader.font_dict["MiSansDemibold36"].render("载入存档", True, "white")

        img = self.button_bg.copy()
        img.blit(img_text, img_text_rect)
        img.set_colorkey("green")

        img_hover = self.button_hover_bg.copy()
        img_hover.blit(img_hover_text, img_text_rect)
        img_hover.set_colorkey("green")
        self.load_button = MenuButton(img, img_hover, img.get_rect())

        #按钮框
    def reset(self):
        print("reset")
        self.is_end = False
        #黑场重置
        self.is_black_end = False

        self.black_surface_index = 0

        #背景重置
        self.bg_h = -60
        self.bg_alpha = 0
        self.bg_copy = self.bg.copy()
        self.bg_copy.set_alpha(self.bg_alpha)

        #按钮值重置
        self.continue_button_value = False
        self.setting_button_value = False
        self.back_button_value = False
        self.load_button_value = False



    def init(self):
        #背景初始化
        self.display_surface = pygame.display.get_surface()


        #使用bg_copy作为背景
        self.bg_copy.set_alpha(self.bg_alpha)

        #按钮初始化
        self.continue_game_button.rect.center = (180, 50+35)
        self.setting_button.rect.center = (180, 150+35)
        self.back_button.rect.center = (180, 250+35)
        self.load_button.rect.center = (180, 350+35)


    def is_continue_press(self,event:pygame.event.Event):
        """
        判断是否按下继续按钮
        :return:
        """
        return self.continue_game_button.is_press_down(event,(Page.window_width//2-180, Page.window_height//2-260+self.bg_h))

    def is_setting_press(self,event:pygame.event.Event):
        """
        判断是否按下设置按钮
        :return:
        """
        return self.setting_button.is_press_down(event,(Page.window_width//2-180, Page.window_height//2-260+self.bg_h))

    def is_back_press(self,event:pygame.event.Event):
        """
        判断是否按下返回按钮
        :return:
        """
        return self.back_button.is_press_down(event,(Page.window_width//2-180, Page.window_height//2-260+self.bg_h))

    def is_load_press(self,event:pygame.event.Event):
        """
        判断是否按下载入存档按钮
        :return:
        """
        return self.load_button.is_press_down(event,(Page.window_width//2-180, Page.window_height//2-260+self.bg_h))

    def handle_event(self, event):
        """
        事件处理
        :param event:
        :return:
        """
        if self.is_end:
            return

        #判断继续按钮是否被按下
        if self.is_continue_press(event):
            self.continue_button_value = True


        #判断设置按钮是否被按下
        if self.is_setting_press(event):
            self.setting_button_value = True


        #判断返回按钮是否被按下
        if self.is_back_press(event):
            self.back_button_value = True

        #判断载入存档按钮是否被按下
        if self.is_load_press(event):
            self.load_button_value = True



    def _black_enter_(self):
        """
        黑场进入动画
        :return:
        """
        if not self.continue_button_value:
            if self.black_surface_index < 12:
                self.black_surface_index += 1
                self.bg_h += 5
                self.bg_alpha += 21
                self.bg_copy.set_alpha(self.bg_alpha)
                print(self.bg_alpha)
        else:
            # 设置页面消失动画
            if self.black_surface_index> 0:
                self.black_surface_index -= 1
                self.bg_h -= 5
                self.bg_alpha -= 21
                print(self.bg_alpha)
                self.bg_copy.set_alpha(self.bg_alpha)
                if self.bg_alpha <= 0:
                    self.is_end = True
        self.display_surface.blit(self.black_surface_list[self.black_surface_index], (0, 0))


    def draw(self):
        """
        绘制
        :return:
        """
        #判断是否结束
        if self.is_end:
            return


        #黑场动画
        self._black_enter_()

        #背景渲染
        self.display_surface.blit(self.bg_copy, (Page.window_width//2-180, Page.window_height//2-260+self.bg_h))


        #按钮动画
        self.continue_game_button.hover_animation((Page.window_width//2-180, Page.window_height//2-260+self.bg_h))
        self.setting_button.hover_animation((Page.window_width//2-180, Page.window_height//2-260+self.bg_h))
        self.back_button.hover_animation((Page.window_width//2-180, Page.window_height//2-260+self.bg_h))
        self.load_button.hover_animation((Page.window_width//2-180, Page.window_height//2-260+self.bg_h))

        #按钮渲染
        self.continue_game_button.draw(self.bg_copy)
        self.setting_button.draw(self.bg_copy)
        self.back_button.draw(self.bg_copy)
        self.load_button.draw(self.bg_copy)



def test():
    """
    测试函数
    :return:
    """
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))

    clock = pygame.time.Clock()

    loader = ResourceLoader()
    loader.load_all_resource()
    loader.wait_load_finish()

    pause_page = PausePage()
    pause_page.init()
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            pause_page.handle_event(event)
        screen.fill("green")
        pause_page.draw()
        pygame.display.update()

if __name__ == '__main__':
    test()

