import pygame
import sys
from SaveManager import SaveManager
from settings import Settings

from OpenAnimation import OpenAnimation
from Pages import *
from Characters import *
from Chapters import *
from Elements import *
import json


class Game:

    def __init__(self):
        #初始化内容
        self.is_content_load = False
        self.is_content_init = False


        self.start_text_page_start = False
        self.quit_page_start = False
        self.settings_page_start = False
        self.load_page_start = False

        self.window_width = 1280
        self.window_height = 720
        self.game_start_load = False
        self.game_start_new = False

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

        #存档管理初始化
        self.save_manager = SaveManager()
        self.save_manager.init_save_data()

        #初始化页面
        self.start_text_page = TextPage("是否开始新的游戏")


        self.start_page = StartPage()
        self.settings_page = SettingsPage(
            self.setting_date["frame_settings"]["screen_set_index"],
            self.setting_date["frame_settings"]["screen_size_index"]
        )
        self.quit_page = QuitPage()
        self.load_page = LoadGamePage()
        

        #初始化页面组
        self.page_group = PagesGroup()
        self.page_group.add_page(self.start_page,
                                 self.settings_page,
                                 self.quit_page,
                                 self.load_page,
                                 self.start_text_page,
                                 )

        #载入存档数据
        self.load_page.save_load(self.save_manager.save_datas)


        #初始化角色
        self.player = Player()
        self.demo_character = DemoCharacter()
        
        #初始化章节
        self.content_chapter = ContentChapter()
        self.start_chapter = StartChapter()
        self.start_chapter.init()


    def handle_event(self, event):
        #当前
        if not self.start_page.is_end:
            #开始页面事件
            if self.start_page.start_button.is_pressed_down(event):
                # print(self.start_text_page_start,self.start_page.is_end)
                print("开始游戏")
                self.start_text_page_start = True
                self.start_page.is_end = True

            #退出页面事件
            elif self.start_page.quit_button.is_pressed_down(event):
                print("退出游戏")
                self.quit_page_start = True
                self.start_page.is_end = True

            #设置页面事件
            elif self.start_page.settings_button.is_pressed_down(event):
                print("设置页面")
                self.settings_page_start = True
                self.start_page.is_end = True

            #载入页面事件
            elif self.start_page.load_button.is_pressed_down(event):
                print("载入页面")
                self.load_page_start = True
                self.start_page.is_end = True


            else:
                self.start_page.is_end = False
        else:
            if self.load_page_start:
                self.load_page.handle_event(event)




    def renew_page(self,text_page):
        self.start_page.is_end = False
        text_page.no_button_value = False
        text_page.yes_button_value = False
        text_page.is_end = False

    def renew_close_value_page(self,page):
        self.start_page.is_end = False
        page.close_button_value = False
        page.is_end = False


    def run(self):
        #初始化开头动画
        self.open_animation.init()
        black_scr = pygame.Surface((self.window_width ,self.window_height))
        black_scr_alpha = 255

        #初始化页面
        self.page_group.set_window_size(self.window_width, self.window_height)#设置页面大小
        self.page_group.pages_init()#初始化页面




        while True:
            #处理事件
            mouse_down = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_down = True
                self.handle_event(event)



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

            #开平动画绘制
            self.open_animation.draw()
            if self.open_animation.is_end and not self.game_start_load and not self.game_start_new:
                self.start_page.draw()
                #黑场动画结束
                if black_scr_alpha !=0:
                    black_scr_alpha -=5
                    self.screen.blit(black_scr, (0, 0))
                    black_scr.set_alpha(black_scr_alpha)

                #绘制开始页面
                if self.start_text_page_start:
                    self.start_text_page.draw()
                    if self.start_text_page.yes_button_value:
                        self.start_text_page.no_button_value = True

                    if self.start_text_page.is_end:
                        #当前页面结束重置内容
                        self.renew_page(self.start_text_page)
                        self.start_text_page_start = False

                # 绘制退出页面
                if self.quit_page_start:
                    self.quit_page.draw()

                    if self.quit_page.is_end:
                        #当前页面结束重置内容
                        self.renew_page(self.quit_page)
                        self.quit_page_start = False

                # 绘制设置页面
                if self.settings_page_start:
                    self.settings_page.draw(mouse_down)

                    if self.settings_page.is_end:
                        #当前页面结束重置内容
                        self.renew_close_value_page(self.settings_page)
                        self.settings_page_start = False
                # 绘制存档页面
                if self.load_page_start:
                    self.load_page.draw()

                    if self.load_page.is_end:
                        #当前页面结束重置内容
                        self.load_page_start = False
                        self.renew_close_value_page(self.load_page)




            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()

