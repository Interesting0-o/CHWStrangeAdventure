import pygame
from Elements.Button import Button
from Elements.ButtonGroup import ButtonGroup
from Pages.Page import Page
from ResourceLoader import ResourceLoader

class QuitPage(Page):
    yes_button_value = False
    no_button_value = False

    def __init__(self):
        super().__init__()
        #黑场资源
        self.black_bg_alpha = None
        self.black_bg = None
        #背景资源
        self.quit_window_alpha = 0
        self.quit_window =ResourceLoader.title_dict["quit"]
        self.quit_window.set_alpha(0)
        self.quit_window_rect = None

        #按钮资源
        self.yes_button = Button(ResourceLoader.button_dict["yes_button"])
        self.no_button = Button(ResourceLoader.button_dict["no_button"])


        self.buttons_group = ButtonGroup()
        self.buttons_group.add_button(self.yes_button, self.no_button)


    def init(self):
        """
        初始化页面
        :return:
        """

        self.display_surface =pygame.display.get_surface()
        #黑场资源
        self.black_bg = pygame.Surface((3840,2160))
        self.black_bg.fill((0,0,0))
        self.black_bg_alpha = 0
        #背景资源
        self.quit_window_rect = self.quit_window.get_rect(center = (
            int(Page.window_width/2),
            int(Page.window_height/2)))
        self.quit_window_rect.centery -= 55

        self.yes_button.rect = self.yes_button.image.get_rect(center =(200,200))
        self.no_button.rect = self.no_button.image.get_rect(center =(400,200))

    def reset(self):
        """
        重置页面
        :return:
        """
        self.is_end = False
        # 黑场重置
        self.black_bg_alpha = 0
        self.black_bg.set_alpha(self.black_bg_alpha)
        #背景重置
        self.quit_window_alpha = 0
        self.quit_window.set_alpha(self.quit_window_alpha)
        self.quit_window_rect = self.quit_window.get_rect(center = (
            int(Page.window_width/2),int(Page.window_height/2)-55)
        )
        #按钮值重置
        self.yes_button_value = False
        self.no_button_value = False
        #按钮动画重置
        self.yes_button.img = ResourceLoader.button_dict["yes_button"][0]
        self.yes_button.animation_index = 0
        self.no_button.img = ResourceLoader.button_dict["no_button"][0]
        self.no_button.animation_index = 0

    def handle_event(self, event):

        """
        事件处理
        :param event:
        :return:
        """
        self.yes_button.hover_animation(self.quit_window_rect.topleft)
        self.no_button.hover_animation(self.quit_window_rect.topleft)
        #按钮按下事件处理
        if self.yes_button.is_press_down(event, self.quit_window_rect.topleft):
            pygame.quit()
            exit()

        if self.no_button.is_press_down(event, self.quit_window_rect.topleft):
            self.no_button_value = True

    def _black_enter_(self):
        """
        黑场进入动画
        :return:
        """
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


    def draw(self):
        if self.is_end:
            return

        #黑场动画绘制
        self._black_enter_()

        #渲染黑场背景和退出窗口
        self.display_surface.blit(self.black_bg, (0,0))
        self.display_surface.blit(self.quit_window, self.quit_window_rect)

        #按钮渲染
        self.buttons_group.draw(self.quit_window)


def test():
    """
    测试函数
    :return:
    """
    loader = ResourceLoader()
    loader.load_all_resource()
    loader.wait_load_finish()

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
            quit_page.handle_event(event)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            quit_page.reset()
        screen.fill("white")
        quit_page.draw()
        pygame.display.update()


if __name__ == "__main__":
    test()