import pygame
from settings import Settings
import sys
from OpenAnimation import OpenAnimation
from Pages import *
import json


class Game:

    def __init__(self):
        #初始化内容
        self.window_width = 1280
        self.window_height = 720
        self.quit_page_start = False
        self.settings_page_start = False

        #读取设置文件
        f = open("settings.json" , "r", encoding="utf-8")
        self.setting_date = json.load(f)
        self.window_width = Settings.screen_size[self.setting_date["frame_settings"]["screen_size_index"]][0]
        self.window_height = Settings.screen_size[self.setting_date["frame_settings"]["screen_size_index"]][1]
        self.screen_setting = Settings.screen_set[self.setting_date["frame_settings"]["screen_set_index"]]

        #初始化游戏窗口
        pygame.init()
        pygame.display.set_caption("陈海文の奇妙冒险", "陈海文陈海文の奇妙冒险")
        pygame.display.set_icon(pygame.image.load(r"resource/img/icon/caption.png"))
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()
        #初始化开头动画
        self.open_animation = OpenAnimation()
        self.open_animation.window_width = self.window_width
        self.open_animation.window_height = self.window_height

        #初始化页面
        self.start_page = StartPage()
        self.settings_page = SettingsPage(
            self.setting_date["frame_settings"]["screen_set_index"],
            self.setting_date["frame_settings"]["screen_size_index"]
        )
        self.quit_page = QuitPage()

        #初始化页面组
        self.page_group = PagesGroup()
        self.page_group.add_page(self.start_page, self.settings_page, self.quit_page)






    def run(self):
        #初始化开头动画
        self.open_animation.init()
        black_scr = pygame.Surface((self.window_width ,self.window_height))
        black_scr_alpha = 255

        #初始化页面
        self.page_group.set_window_size(self.window_width, self.window_height)#设置页面大小
        self.page_group.pages_init()#初始化页面




        while True:
            mouse_down = False
            #处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_down = True
            dt = self.clock.tick(60) / 1000
            #检验是否对游戏进行设置并保存
            if self.settings_page.frame_setting.isSettingsChange:
                #获取所修改的设置
                temp_screen_size_index = self.settings_page.frame_setting.resolution_menu.get_index()
                temp_screen_set_index = self.settings_page.frame_setting.fullscreen_menu.get_index()
                #设置游戏窗口大小
                self.screen =pygame.display.set_mode(
                    Settings.screen_size[temp_screen_size_index],
                    flags =Settings.screen_set[temp_screen_set_index])
                #更改设置文件
                self.setting_date["frame_settings"]["screen_size_index"] = temp_screen_size_index
                self.setting_date["frame_settings"]["screen_set_index"] = temp_screen_set_index
                with open("settings.json", "w", encoding="utf-8") as f:
                    json.dump(self.setting_date, f, ensure_ascii=False, indent=4)
                self.settings_page.frame_setting.isSettingsChange = False

                #重置页面大小
                self.page_group.set_window_size(Settings.screen_size[temp_screen_size_index][0],
                                                Settings.screen_size[temp_screen_size_index][1])
                self.page_group.pages_init()#初始化页面


            self.open_animation.draw()
            if self.open_animation.is_end:
                self.start_page.draw()

                if black_scr_alpha !=0:
                    black_scr_alpha -=5

                    self.screen.blit(black_scr, (0, 0))
                    black_scr.set_alpha(black_scr_alpha)


                #设置页面启动
                if self.start_page.settings_button.is_pressed():#判断是否点击设置按钮
                    self.settings_page_start = True#启动设置改为True
                if self.settings_page_start:
                    self.settings_page.draw(mouse_down)#启动设置页面
                if self.settings_page.is_end:#判断是否设置页面关闭
                    self.start_page.is_end = False
                    self.settings_page_start = False
                    self.settings_page.is_end = False
                    self.settings_page.close_button_value = False#重新置关闭按钮状态



                #关闭页面启动
                if self.start_page.quit_button.is_pressed():#判断是否点击退出按钮
                    self.quit_page_start = True#启动退出改为True
                if self.quit_page_start:
                    self.quit_page.draw()#启动退出页面
                if self.quit_page.is_end:#判断是否退出页面关闭
                    self.start_page.is_end = False
                    self.quit_page_start = False
                    self.quit_page.is_end = False
                    self.quit_page.no_button_value = False#重新置退出按钮状态

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()

