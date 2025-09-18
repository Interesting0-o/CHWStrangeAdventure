import pygame
from settings import Settings
import sys
from OpenAnimation import OpenAnimation
from Pages import *


class Game:
    window_width = Settings.M_WIDTH
    window_height = Settings.M_HEIGHT
    quit_page_start = False
    settings_page_start = False


    def __init__(self):

        self.open_animation = OpenAnimation()
        pygame.init()
        pygame.display.set_caption("陈海文の奇妙冒险", "陈海文陈海文の奇妙冒险")
        pygame.display.set_icon(pygame.image.load(r"resource/img/icon/caption.png"))
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()



    def run(self):
        start_page = StartPage()
        start_page.init()
        self.open_animation.init()
        black_scr = pygame.Surface((Settings.M_WIDTH, Settings.M_HEIGHT))
        black_scr_alpha = 255
        quit_page = QuitPage()
        quit_page.init()
        settings_page = SettingsPage()
        settings_page.init()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            dt = self.clock.tick(60) / 1000



            self.open_animation.draw()
            if self.open_animation.is_end:
                start_page.draw()

                if black_scr_alpha !=0:
                    black_scr_alpha -=5

                    self.screen.blit(black_scr, (0, 0))
                    black_scr.set_alpha(black_scr_alpha)


                #设置页面启动
                if start_page.settings_button.is_pressed():
                    self.settings_page_start = True
                if self.settings_page_start:
                    settings_page.draw()
                if settings_page.is_end:
                    start_page.is_end = False
                    self.settings_page_start = False
                    settings_page.is_end = False
                    settings_page.close_button_value = False



                #关闭页面启动
                if start_page.quit_button.is_pressed():
                    self.quit_page_start = True
                if self.quit_page_start:
                    quit_page.draw()
                if quit_page.is_end:
                    start_page.is_end = False
                    self.quit_page_start = False
                    quit_page.is_end = False
                    quit_page.no_button_value = False

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()

