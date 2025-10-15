import pygame
from Pages.Page import Page
from Elements.MenuButton import MenuButton
from ResourceLoader import ResourceLoader

class PausePage(Page):
    def __init__(self):
        super().__init__()


        #按钮初始化
        self.continue_button_value = True
        self.setting_button_value = False
        self.back_button_value = False
        self.load_button_value = False
        self.button_bg = None
        #黑场专场内容

        self.is_black_end = False
        self.black_surface = pygame.Surface((3840,2160))
        self.black_surface.fill((0, 0, 0))
        self.black_surface_alpha = 0

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
        img_text = ResourceLoader.font_MiSans_Demibold36.render("继续游戏", True, "orange")
        img_text_rect = img_text.get_rect(center=(150, 35))
        img_hover_text = ResourceLoader.font_MiSans_Demibold36.render("继续游戏", True, "white")

        img = self.button_bg.copy()
        img.blit(img_text, img_text_rect)
        img.set_colorkey("green")

        img_hover = self.button_hover_bg.copy()
        img_hover.blit(img_hover_text, img_text_rect)
        img_hover.set_colorkey("green")
        self.continue_game_button = MenuButton(img, img_hover, img.get_rect())
        #设置按钮
        img_text = ResourceLoader.font_MiSans_Demibold36.render("设置", True, "orange")
        img_text_rect = img_text.get_rect(center=(150, 35))
        img_hover_text = ResourceLoader.font_MiSans_Demibold36.render("设置", True, "white")

        img = self.button_bg.copy()
        img.blit(img_text, img_text_rect)
        img.set_colorkey("green")

        img_hover = self.button_hover_bg.copy()
        img_hover.blit(img_hover_text, img_text_rect)
        img_hover.set_colorkey("green")
        self.setting_button = MenuButton(img, img_hover, img.get_rect())
        #返回标题按钮
        img_text = ResourceLoader.font_MiSans_Demibold36.render("返回标题", True, "orange")
        img_text_rect = img_text.get_rect(center=(150, 35))
        img_hover_text = ResourceLoader.font_MiSans_Demibold36.render("返回标题", True, "white")

        img = self.button_bg.copy()
        img.blit(img_text, img_text_rect)
        img.set_colorkey("green")

        img_hover = self.button_hover_bg.copy()
        img_hover.blit(img_hover_text, img_text_rect)
        img_hover.set_colorkey("green")
        self.back_button = MenuButton(img, img_hover, img.get_rect())
        #载入存档按钮
        img_text = ResourceLoader.font_MiSans_Demibold36.render("载入存档", True, "orange")
        img_text_rect = img_text.get_rect(center=(150, 35))
        img_hover_text = ResourceLoader.font_MiSans_Demibold36.render("载入存档", True, "white")

        img = self.button_bg.copy()
        img.blit(img_text, img_text_rect)
        img.set_colorkey("green")

        img_hover = self.button_hover_bg.copy()
        img_hover.blit(img_hover_text, img_text_rect)
        img_hover.set_colorkey("green")
        self.load_button = MenuButton(img, img_hover, img.get_rect())

        #按钮框
    def reset(self):
        self.is_end = False
        #黑场重置
        self.black_surface_alpha = 0
        self.is_black_end = False
        self.black_surface.set_alpha(self.black_surface_alpha)

        #背景重置
        self.bg_h = -60
        self.bg_alpha = 0
        self.bg_copy = self.bg.copy()
        self.bg_copy.set_alpha(self.bg_alpha)

        #按钮值重置
        self.continue_button_value = True
        self.setting_button_value = False
        self.back_button_value = False
        self.load_button_value = False



    def init(self):
        #背景初始化
        self.display_surface = pygame.display.get_surface()

        #黑场初始化
        self.black_surface.set_alpha(self.black_surface_alpha)

        #使用bg_copy作为背景
        self.bg_copy.set_alpha(self.bg_alpha)

        #按钮初始化
        self.continue_game_button.rect.center = (180, 50+35)
        self.setting_button.rect.center = (180, 150+35)
        self.back_button.rect.center = (180, 250+35)
        self.load_button.rect.center = (180, 350+35)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                #按钮按下事件
                #判断继续按钮是否被按下
                if self.continue_game_button.is_pressed_down_blit((self.window_width//2-180, self.window_height//2-260+self.bg_h), True):
                    self.continue_button_value = True


                #判断设置按钮是否被按下
                if self.setting_button.is_pressed_down_blit((self.window_width//2-180, self.window_height//2-260+self.bg_h), True):
                    self.setting_button_value = True


                #判断返回按钮是否被按下
                if self.back_button.is_pressed_down_blit((self.window_width//2-180, self.window_height//2-260+self.bg_h), True):
                    self.back_button_value = True

                #判断载入存档按钮是否被按下
                if self.load_button.is_pressed_down_blit((self.window_width//2-180, self.window_height//2-260+self.bg_h), True):
                    self.load_button_value = True

        if event.type == pygame.KEYDOWN:
            #按下ESC键返回游戏
            if event.key == pygame.K_ESCAPE:
                if self.continue_button_value:
                    self.continue_button_value = False
                else:
                    self.continue_button_value = True



    def draw(self):

        if not self.continue_button_value:
            if self.black_surface_alpha < 120:
                self.black_surface_alpha += 10
                self.black_surface.set_alpha(self.black_surface_alpha)
                self.bg_h += 5
                self.bg_alpha += 21
                self.bg_copy.set_alpha(self.bg_alpha)
                print(self.bg_alpha)
        else:
            # 设置页面消失动画
            if self.black_surface_alpha > 0:
                self.black_surface_alpha -= 10
                self.black_surface.set_alpha(self.black_surface_alpha)
                self.bg_h -= 5
                self.bg_alpha -= 21
                print(self.bg_alpha)
                self.bg_copy.set_alpha(self.bg_alpha)
                if self.bg_alpha <= 0:
                    self.is_end = True
        #画面元素渲染
        self.display_surface.blit(self.black_surface, (0, 0))
        self.display_surface.blit(self.bg_copy, (self.window_width//2-180, self.window_height//2-260+self.bg_h))

        self.bg_copy.blit(self.continue_game_button.img, self.continue_game_button.rect)
        self.bg_copy.blit(self.setting_button.img, self.setting_button.rect)
        self.bg_copy.blit(self.back_button.img, self.back_button.rect)
        self.bg_copy.blit(self.load_button.img, self.load_button.rect)


        #按钮动画
        self.continue_game_button.hover_animation_blit((self.window_width//2-180, self.window_height//2-260+self.bg_h))
        self.setting_button.hover_animation_blit((self.window_width//2-180, self.window_height//2-260+self.bg_h))
        self.back_button.hover_animation_blit((self.window_width//2-180, self.window_height//2-260+self.bg_h))
        self.load_button.hover_animation_blit((self.window_width//2-180, self.window_height//2-260+self.bg_h))




if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))

    clock = pygame.time.Clock()

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


