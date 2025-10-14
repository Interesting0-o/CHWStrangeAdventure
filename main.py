import pygame
import sys

from ResourceLoader import ResourceLoader
from SaveManager import SaveManager
from settings import Settings
from OpenAnimation import OpenAnimation
from Pages import *
from Characters import *
from Chapters import *
import json


class Game:

    def __init__(self):


        self.current_save_name = None
        self.current_save = None

        #d当前游戏是否暂停
        self.is_pause = False

        #存档相关
        self.is_create_save = False
        self.is_load_save = False

        #初始化内容
        self.is_content_load = False
        self.is_content_init = False

        #开始页面相关
        self.start_text_page_start = False
        self.quit_page_start = False
        self.settings_page_start = False
        self.load_page_start = False

        #游戏开始类型
        self.game_start_load = False
        self.game_start_new = False


        self.window_width = 1280
        self.window_height = 720
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
        self.start_text_page = TextPage("是否开始一个新的游戏")


        self.start_page = StartPage()
        self.settings_page = SettingsPage(
            self.setting_date["frame_settings"]["screen_set_index"],
            self.setting_date["frame_settings"]["screen_size_index"]
        )
        self.quit_page = QuitPage()
        self.load_page = LoadGamePage()
        self.pause_page = PausePage()
        

        #初始化页面组
        self.page_group = PagesGroup()
        self.page_group.add_page(self.start_page,
                                 self.settings_page,
                                 self.quit_page,
                                 self.load_page,
                                 self.start_text_page,
                                 self.pause_page
                                 )

        #载入存档数据
        self.load_page.save_load(self.save_manager.save_datas)

        #初始化角色
        self.player = Player()
        self.demo_character = DemoCharacter()
        self.character_group = CharacterGroup()
        self.character_group.add_character( self.demo_character)
        
        #初始化章节
        self.content_chapter = ContentChapter()
        self.start_chapter = StartChapter()




    def init(self):

        self.current_save_name = None
        self.current_save = None

        #d当前游戏是否暂停
        self.is_pause = False

        #存档相关
        self.is_create_save = False
        self.is_load_save = False

        #初始化内容
        self.is_content_load = False
        self.is_content_init = False

        #开始页面相关
        self.start_text_page_start = False
        self.quit_page_start = False
        self.settings_page_start = False
        self.load_page_start = False

        #游戏开始类型
        self.game_start_load = False
        self.game_start_new = False

        self.start_page.is_end = False

    def handle_event(self, event):
        #在起始页面时的事件处理
        if not self.start_page.is_end:
            #开始页面事件
            if self.start_page.start_button.is_pressed_down(event):
                self.start_text_page_start = True
                self.start_page.is_end = True

            #退出页面事件
            elif self.start_page.quit_button.is_pressed_down(event):
                self.quit_page_start = True
                self.start_page.is_end = True

            #设置页面事件
            elif self.start_page.settings_button.is_pressed_down(event):
                self.settings_page_start = True
                self.start_page.is_end = True

            #载入页面事件
            elif self.start_page.load_button.is_pressed_down(event):
                self.load_page_start = True
                self.start_page.is_end = True

            else:
                self.start_page.is_end = False

        else:

            #载入存档界面事件
            if self.load_page_start:
                self.load_page.handle_event(event)

            #开始游戏后事件处理
            if not self.is_pause:
                #通过开始按钮来开始游戏
                if self.game_start_new:
                    if not self.start_chapter.is_end:
                        self.start_chapter.handle_event(event)
                    else:
                        if not self.is_create_save:
                            #创建存档
                            self.current_save = self.save_manager.init_save.copy()
                            self.current_save["player"]["name"] = self.player.name
                            #存档数据保存到硬盘并重置save_manager
                            self.current_save_name = self.save_manager.save_save_data(self.current_save)

                            #初始化载入页面
                            self.load_page.save_load(self.save_manager.save_datas)
                            self.load_page.init()
                            self.is_create_save = True
                    #处理内容章节事件
                    if self.is_content_init and self.is_content_load:
                        self.content_chapter.handle_event(event)
                        #处理存档保存事件
                        if self.content_chapter.save_saves:
                            self.current_save = self.content_chapter.to_dict()
                            self.current_save_name = self.save_manager.save_save_data(self.current_save)

                #通过载入按钮来开始游戏
                if self.game_start_load:
                    #载入存档
                    if not self.is_load_save:
                        self.current_save = self.load_page.current_save_data
                        self.current_save_name = self.load_page.current_save_name
                        self.is_load_save = True

                    #处理内容章节事件
                    if self.is_content_init and self.is_content_load:
                        self.content_chapter.handle_event(event)
                        #处理存档保存事件
                        if self.content_chapter.save_saves:
                            self.current_save = self.content_chapter.to_dict()
                            self.current_save_name = self.save_manager.save_save_data(self.current_save)
            #暂停之后的事件处理
            else:
                #返回按钮事件
                if self.pause_page.back_button_value:
                    print(self.pause_page.back_button_value)
                    self.back_to_start()
                    self.pause_page.back_button_value = False
                    print(self.pause_page.back_button_value)



            #处理暂停事件
            self.pause_page.handle_event(event)


            #处理暂停按钮
            if self.pause_page.continue_button_value:
                self.is_pause = False
            else:
                self.is_pause = True



    def renew_page(self,text_page):
        self.start_page.is_end = False
        text_page.no_button_value = False
        text_page.yes_button_value = False
        text_page.is_end = False

    def renew_close_value_page(self,page):
        self.start_page.is_end = False
        page.close_button_value = False
        page.is_end = False

    def start_page_button_reset(self):
        #开始页面button状态重置
        self.start_page.start_button.img= ResourceLoader.start_button_animation[0]
        self.start_page.start_button.index =0
        self.start_page.quit_button.img= ResourceLoader.quit_button_animation[0]
        self.start_page.quit_button.index =0
        self.start_page.settings_button.img= ResourceLoader.settings_button_animation[0]
        self.start_page.settings_button.index =0
        self.start_page.load_button.img= ResourceLoader.load_button_animation[0]
        self.start_page.load_button.index =0

        #按钮内容重置
        self.start_text_page_start = False
        self.quit_page_start = False
        self.settings_page_start = False
        self.load_page_start = False



    def back_to_start(self):
        #设置开始界面为未结束
        self.start_page.is_end = False

        #游戏开始类型设置为未开始
        self.game_start_load = False
        self.game_start_new = False

        #清除当前存档信息
        self.current_save_name = None
        self.current_save = None

        #开始页面的button状态重置
        self.start_page_button_reset()






    def run(self):
        #初始化开头动画
        self.open_animation.init()
        black_scr = pygame.Surface((3840 ,2160))
        black_scr_alpha = 255

        #初始化页面
        self.page_group.set_window_size(self.window_width, self.window_height)#设置页面大小
        self.page_group.pages_init()#初始化页面

        self.start_page.set_window_size(self.window_width, self.window_height)
        self.start_page.init()
        self.content_chapter.set_window_size(self.window_width, self.window_height)
        self.start_chapter.init()




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

                #重置页面大小并初始化
                self.page_group.set_window_size(Settings.screen_size[temp_screen_size_index][0],
                                                Settings.screen_size[temp_screen_size_index][1])

                self.page_group.pages_init()#初始化页面

                #重置章节大小并初始化
                self.start_chapter.set_window_size(Settings.screen_size[temp_screen_size_index][0],
                                                    Settings.screen_size[temp_screen_size_index][1])
                self.start_chapter.init()
                #重置内容大小并初始化
                self.content_chapter.set_window_size(Settings.screen_size[temp_screen_size_index][0],
                                                    Settings.screen_size[temp_screen_size_index][1])
                if self.is_content_load and self.is_content_init:
                    self.content_chapter.init()


            #开平动画绘制
            self.open_animation.draw()
            if self.open_animation.is_end and not self.game_start_new and not self.game_start_load:
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
                        self.game_start_new = True

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
                    if self.load_page.load_text_page.yes_button_value:
                        self.load_page.load_text_page.no_button_value = True
                        self.game_start_load = True

                    if self.load_page.is_end:
                        #当前页面结束重置内容
                        self.load_page_start = False
                        self.renew_close_value_page(self.load_page)

            #通过创建存档来开始游戏
            if self.game_start_new:
                print(1)
                self.start_page.is_end = True
                self.start_chapter.show(self.player)
                if self.is_create_save:
                    if not self.is_content_load:
                        self.content_chapter.read_config(self.current_save, self.character_group)
                        self.is_content_load = True
                    if not self.is_content_init:
                        self.content_chapter.init()
                        self.is_content_init = True
                    if self.is_content_load and self.is_content_init:
                        self.content_chapter.show()

            #通过载入存档来开始游戏
            if self.game_start_load:
                print(2)
                if self.is_load_save:
                    if not self.is_content_load:
                        self.content_chapter.read_config(self.current_save, self.character_group)
                        self.is_content_load = True
                    if not self.is_content_init:
                        self.content_chapter.init()
                        self.is_content_init = True
                    if self.is_content_load and self.is_content_init:
                        self.content_chapter.show()
            #在游戏中可以显示暂停页面

            if self.game_start_load or self.game_start_new:
                self.pause_page.draw()

            print(self.start_page.is_end ,"and",self.game_start_new,self.game_start_load)

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()

