import pygame
from Elements.Button import Button
from Pages.Page import Page

class QuitPage(Page):
    yes_button_value = False
    no_button_value = False


    def __init__(self):
        super().__init__()

        #黑场资源
        self.black_bg = pygame.Surface((self.window_width, self.window_height))
        self.black_bg.fill((0,0,0))
        self.black_bg_alpha = 0


        #背景资源
        self.quit_window_alpha = 0
        self.quit_window =pygame.image.load(self.path[:-6]+r"/resource/img/title/qiut.png")
        self.quit_window.set_alpha(0)
        self.quit_window_rect = self.quit_window.get_rect(center = (
            int(self.window_width/2),
            int(self.window_height/2)))
        self.quit_window_rect.centery -= 55


        #按钮资源
        self.yes_button = Button(pygame.image.load(
            self.path[:-6]+r"/resource/img/button/yes_button/yes_button_00.png"
        ))
        self.no_button = Button(pygame.image.load(
            self.path[:-6]+r"/resource/img/button/no_button/no_button_00.png"
        ))

        for i in range(0,30):
            self.yes_button.animation_list.append(
                pygame.image.load(
                    self.path[:-6]+rf"/resource/img/button/yes_button/yes_button_{i:02d}.png"
                )
            )
            self.no_button.animation_list.append(
                pygame.image.load(
                    self.path[:-6]+rf"/resource/img/button/no_button/no_button_{i:02d}.png"
                )
            )


        self.buttons_group = pygame.sprite.Group()
        self.buttons_group.add(self.yes_button, self.no_button)


    def init(self):
        self.display_surface =pygame.display.get_surface()


        self.yes_button.rect = self.yes_button.image.get_rect(center =(200,200))
        self.no_button.rect = self.no_button.image.get_rect(center =(400,200))



    def draw(self):
        #黑场动画
        if not self.no_button_value: #取消按钮未按下时
            if self.black_bg_alpha < 120:
                self.black_bg_alpha += 10
                self.quit_window_alpha += 21
                self.black_bg.set_alpha(self.black_bg_alpha)
                self.quit_window.set_alpha(self.quit_window_alpha)
                self.quit_window_rect.centery += 5
                if __name__ == '__main__':
                    print("y的值", self.quit_window_rect.centery,end = "")
                    print("退出窗口的透明度", self.quit_window_alpha,end = "")
                    print("黑场的透明度", self.black_bg_alpha,end = "")
                    print()
        else :
            if self.black_bg_alpha > 0 :
                self.black_bg_alpha -= 10
                self.quit_window_alpha -= 21
                self.black_bg.set_alpha(self.black_bg_alpha)
                self.quit_window.set_alpha(self.quit_window_alpha)
                self.quit_window_rect.centery -= 5
                if __name__ == '__main__':
                    print("y的值", self.quit_window_rect.centery,end = "")
                    print("退出窗口的透明度", self.quit_window_alpha,end = "")
                    print("黑场的透明度", self.black_bg_alpha,end = "")
                    print()

                if self.black_bg_alpha <= 0:
                    self.is_end = True





        #渲染黑场背景和退出窗口
        self.display_surface.blit(self.black_bg, (0,0))
        self.display_surface.blit(self.quit_window, self.quit_window_rect)



        #按钮渲染
        self.buttons_group.draw(self.quit_window)
        self.yes_button.hover_animation_blit(self.quit_window_rect.topleft)
        self.no_button.hover_animation_blit(self.quit_window_rect.topleft)


        #按钮按下事件处理
        if self.yes_button.is_pressed_blit(self.quit_window_rect.topleft):
            pygame.quit()
            exit()

        if self.no_button.is_pressed_blit(self.quit_window_rect.topleft):
            self.no_button_value = True









if __name__ == "__main__":
    pygame.init()
    quit_page = QuitPage()
    screen = pygame.display.set_mode((quit_page.window_width, quit_page.window_height))
    clock = pygame.time.Clock()


    quit_page.init()

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill("white")
        quit_page.draw()
        pygame.display.update()