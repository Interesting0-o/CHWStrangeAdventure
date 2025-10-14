import pygame
from Elements.Button import Button
from Pages.Page import Page
from ResourceLoader import ResourceLoader

class TextPage(Page):
    yes_button_value = False
    no_button_value = False

    def __init__(self,
                 string:str
                 ):
        super().__init__()
        #黑场资源
        self.black_bg_alpha = None
        self.black_bg = None
        #背景资源
        text = ResourceLoader.font_MiSans_Demibold36.render(string, True, "black")
        text_rect = text.get_rect(center = (300,120))

        self.text_window_alpha = 0
        self.text_window =pygame.image.load(self.path[:-6]+r"/resource/img/title/text.png")
        self.text_window.blit(text, text_rect)
        self.text_window.set_alpha(0)
        self.text_window_rect = None

        #按钮资源
        self.yes_button = Button(ResourceLoader.yes_button_animation[0])
        self.no_button = Button(ResourceLoader.no_button_animation[0])
        #按钮动画添加
        self.yes_button.animation_list = ResourceLoader.yes_button_animation
        self.no_button.animation_list = ResourceLoader.no_button_animation

        self.buttons_group = pygame.sprite.Group()
        self.buttons_group.add(self.yes_button, self.no_button)

    def renew(self):
        #按钮动画重置
        self.yes_button_value = False
        self.no_button_value = False
        #
        self.is_end = False
        #文本窗口重置
        self.text_window_alpha = 0

    def init(self):

        self.display_surface =pygame.display.get_surface()
        #黑场资源
        self.black_bg = pygame.Surface((3840, 2160))
        self.black_bg.fill((0,0,0))
        self.black_bg_alpha = 0
        #背景资源
        self.text_window_rect = self.text_window.get_rect(center = (
            int(self.window_width/2),
            int(self.window_height/2)))
        self.text_window_rect.centery -= 55

        self.yes_button.rect = self.yes_button.image.get_rect(center =(200,200))
        self.no_button.rect = self.no_button.image.get_rect(center =(400,200))

    def reset(self):
        self.is_end = False
        # 黑场重置
        self.black_bg_alpha = 0
        self.black_bg.set_alpha(self.black_bg_alpha)
        #背景重置
        self.text_window_alpha = 0
        self.text_window.set_alpha(self.text_window_alpha)
        self.text_window_rect = self.text_window.get_rect(center = (
            int(self.window_width/2),int(self.window_height/2)-55)
        )
        #按钮值重置
        self.yes_button_value = False
        self.no_button_value = False
        #按钮动画重置
        self.yes_button.img = ResourceLoader.yes_button_animation[0]
        self.yes_button.animation_index = 0
        self.no_button.img = ResourceLoader.no_button_animation[0]
        self.no_button.animation_index = 0

    def draw(self):
        #黑场动画
        if not self.no_button_value: #取消按钮未按下时
            if self.black_bg_alpha < 120:
                self.black_bg_alpha += 10
                self.text_window_alpha += 21
                self.black_bg.set_alpha(self.black_bg_alpha)
                self.text_window.set_alpha(self.text_window_alpha)
                self.text_window_rect.centery += 5
                if __name__ == '__main__':
                    print("y的值", self.text_window_rect.centery,end = "")
                    print("退出窗口的透明度", self.text_window_alpha,end = "")
                    print("黑场的透明度", self.black_bg_alpha,end = "")
                    print()
        else :
            if self.black_bg_alpha > 0 :
                self.black_bg_alpha -= 10
                self.text_window_alpha -= 21
                self.black_bg.set_alpha(self.black_bg_alpha)
                self.text_window.set_alpha(self.text_window_alpha)
                self.text_window_rect.centery -= 5
                if __name__ == '__main__':
                    print("y的值", self.text_window_rect.centery,end = "")
                    print("退出窗口的透明度", self.text_window_alpha,end = "")
                    print("黑场的透明度", self.black_bg_alpha,end = "")
                    print()

                if self.black_bg_alpha <= 0:
                    self.is_end = True

        #渲染黑场背景和退出窗口
        self.display_surface.blit(self.black_bg, (0,0))
        self.display_surface.blit(self.text_window, self.text_window_rect)

        #按钮渲染
        self.buttons_group.draw(self.text_window)
        self.yes_button.hover_animation_blit(self.text_window_rect.topleft)
        self.no_button.hover_animation_blit(self.text_window_rect.topleft)

        #按钮按下事件处理
        if self.yes_button.is_pressed_blit(self.text_window_rect.topleft):
            self.yes_button_value = True

        if self.no_button.is_pressed_blit(self.text_window_rect.topleft):
            self.no_button_value = True

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    game = TextPage("niuhao")
    game.init()


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game.reset()
        screen.fill((255, 255, 255))
        game.draw()
        if game.is_end:
            game.renew()
        pygame.display.update()
        clock.tick(60)