import pygame
import json
import threading

from Pages import *
from ResourceLoader import ResourceLoader
from SaveManager import SaveManager
from settings import Settings
from Characters import *
from Voice import Voice

pygame.font.init()
pygame.mixer.init()

class Game:
    path = __file__[:-8]
    def __init__(self):
        self.FPS = 60

        #开屏黑场专场内容
        self.black_scr = pygame.Surface((3840, 2160))
        self.black_scr.fill((0, 0, 0))
        self.black_scr_alpha = 255

        #资源加载器初始化
        self.loader:ResourceLoader = ResourceLoader()
        #存档管理器初始化
        self.save_manager:SaveManager = SaveManager()
        #读取配置文件
        self._read_config_()

        #设置窗口大小
        self.window_width = self.get_size_by_set()[0]
        self.window_height = self.get_size_by_set()[1]

        Page.window_width = self.window_width
        Page.window_height = self.window_height

        #页面组
        self.pages_group:PagesGroup = PagesGroup()

        #开平动画时后台初始化的资源
        self.is_thread_start = False
        self.is_thread_finish = False
        self.thread_init = threading.Thread(target=self._threading_start_)

        #两种开始游戏的方式
        self._game_begin_new_ = False
        self._game_begin_load_ = False

        self._on_game_begin_ = True

        #存档是否被创建
        self.is_save_create = False

    def _character_define_(self):
        """
        定义角色
        :return:
        """
        #初始化主角
        self.player = Player()
        #初始化角色组
        self.character_group = CharacterGroup()

        #初始化其他角色
        self.demo_character = DemoCharacter()

        self.character_group.add_character(self.demo_character)

    def get_size_by_set(self):
        return Settings.screen_size[self.config["frame_settings"]["resolution_size_index"]]

    def _save_config_(self):
        """
        保存配置文件
        :return:
        """
        self.config["frame_settings"]["fullscreen_setting_index"] = self.settings_scene.get_fullscreen_set()
        self.config["frame_settings"]["resolution_size_index"] = self.settings_scene.get_resolution_set()
        with open(Game.path + r"\config.json", 'w') as f:
            json.dump(self.config, f,indent=4)

    def _set_screen_(self):
        """
        根据设置页面来设置屏幕
        :return:
        """
        #设置屏幕大小
        self.window_width = Settings.screen_size[self.settings_scene.get_resolution_set()][0]
        self.window_height = Settings.screen_size[self.settings_scene.get_resolution_set()][1]
        Page.window_width = self.window_width
        Page.window_height = self.window_height
        #设置屏幕模式
        self.screen = pygame.display.set_mode(size=Settings.screen_size[self.settings_scene.get_resolution_set()],
                                              flags=Settings.screen_set[self.settings_scene.get_fullscreen_set()])

    def _read_config_(self):
        """
        读取配置文件
        :return:
        """
        with  open(Game.path + r"\config.json", 'r') as f:
            self.config = json.load(f)

    def _page_define_(self):
        """
        定义所有的页面
        :return:
        """
        #页面组初始化

        self.start_page:StartPage = StartPage()
        self.load_game_scene:LoadGameScene = LoadGameScene()
        self.pause_page:PausePage = PausePage()
        try:
            self.settings_scene:SettingsScene = SettingsScene(self.config["frame_settings"]["fullscreen_setting_index"],
                                              self.config["frame_settings"]["resolution_size_index"]
                                               )
        except KeyError:
            print("配置文件有误，请检查配置文件")

        self.quit_page:QuitPage = QuitPage()
        self.game_scene:GameScene = GameScene()
        self.start_chapter:StartChapter = StartChapter()

        #text_page；类型
        self.tp_is_start:TextPage = TextPage("是否开始一个新的游戏？")


        self.pages_group.add_page(self.start_page,
                                   self.load_game_scene,
                                   self.pause_page,
                                   self.settings_scene,
                                   self.quit_page,
                                   self.start_chapter,
                                  self.tp_is_start
                                  )

    def _page_init_(self):
        self.pages_group.pages_init()

        self.start_chapter.set_player(self.player)

    def is_load_finish(self):
        """
        判断资源是否加载完成
        :return:
        """
        return self.loader.check_load_finish() and self.save_manager.check_load_finish()

    def _threading_start_(self):
        """
        启动页面线程
        :return:
        """
        self.is_thread_start = True

        #角色初始化
        self._character_define_()
        #页面组初始化
        self._page_define_()
        self.load_game_scene.save_load(self.save_manager)
        self._page_init_()
        self.pages_group.change_page_end()
        self.game_scene.is_end = True

        self.is_thread_finish = True
        print("_threading_start_ 线程启动完成")

    def _game_scene_event_(self,event:pygame.event.Event) -> None:
        """
        _game_scene_event_ 的 Docstring
        
        :param self: 说明
        :param event: 说明
        :type event: pygame.event.Event
        """
        #照常处理事件
        self.game_scene.handle_event(event)

        #当保存按钮被按下时
        if self.game_scene.is_save_press(event):
            #保存存档数据
            self.save_manager.cover_save_data(self.player.name,self.game_scene.to_dict())


    def _handle_event_(self,event:pygame.event.Event):
        """
        处理事件
        :param event:
        :return:
        """
        #在资源加载完成后才处理事件
        print(self.is_load_finish(),self.is_thread_finish)
        if self.is_load_finish() and self.is_thread_finish:
            print("资源加载完成，开始处理事件")
            self.open_animation.handle_event(event)

            #处理开始菜单页面事件
            if self.open_animation.is_black and self._on_game_begin_:
                print("开始菜单界面  事件")
                self.start_page.is_end = False
                self._start_menu_event_(event)

            elif self._game_begin_new_:
                print("开始新游戏  事件")
                self._game_new_event_(event)
            
            elif self._game_begin_load_:
                print("开始载入游戏  事件")
                self._game_load_event_(event)

    def _is_other_show_start_(self):
        """
        判断开始菜单界面是否有其他页面显示
        :return:
        """
        return self.load_game_scene.is_show or self.settings_scene.is_show or self.quit_page.is_show or self.tp_is_start.is_show

    def _back_to_start_menu_(self):
        """
        返回开始菜单界面
        :return:
        """
        #将所有设置改为在开始菜单界面时的值
        self._game_begin_new_ = False
        self._game_begin_load_ = False
        self._on_game_begin_ = True

        self.is_save_create = False
        #重置所有页面
        self.pages_group.reset()
        self.pages_group.change_page_end()

        #设置开始菜单界面为未结束
        self.start_page.is_end = False

        self.game_scene.is_end = True

        #停止所有声音
        Voice.char_channel.stop()
        Voice.effect_channel.stop()



    def _settings_event_(self):
        """
        处理设置页面的按钮事件
        :return:
        """
        # 设置保存
        # #保存设置到config文件
        self._save_config_()
        # #设置屏幕
        self._set_screen_()
        #设置页面全部初始化
        self._page_init_()
        self.settings_scene.reset_set()

        self.settings_scene.set_settings_change(False)

    def _start_menu_event_(self,event:pygame.event.Event):
        """
        处理开始菜单的按钮事件
        :param event:
        :return:
        """
        # 处理开始按钮事件
        if self.start_page.is_start_down(event) and not self._is_other_show_start_():
            if not self.tp_is_start.is_reset:
                self.tp_is_start.reset()
                self.tp_is_start.is_show = True

        # 处理载入游戏按钮事件
        elif self.start_page.is_load_down(event) and not self._is_other_show_start_():
            print("载入游戏")
            self.load_game_scene.reset()

        # 处理设置按钮事件
        elif self.start_page.is_settings_down(event) and not self._is_other_show_start_():
            print("设置")
            self.settings_scene.reset()

        # 处理退出按钮事件
        elif self.start_page.is_quit_down(event) and not self._is_other_show_start_():
            print("退出游戏")
            self.quit_page.reset()

        # 处理退出，设置，载入游戏页面事件
        self.quit_page.handle_event(event)
        self.settings_scene.handle_event(event)
        self._load_game_event_(event)


        self._start_new_event_tp_(event)

        #设置界面内的保存按钮是否按下
        if self.settings_scene.is_settings_change():
            self._settings_event_()

    def _load_game_event_(self,event:pygame.event.Event):
        """
        _load_game_event_ 的 Docstring
        
        :param self: 说明
        :param event: 说明
        :type event: pygame.event.Event
        """
        self.load_game_scene.handle_event(event)        

        if self.load_game_scene.tp_is_load.is_yes_button_down(event):

            #更改游戏状态为以载入存档的方式开始游戏
            self._game_begin_load_ = True
            self._on_game_begin_ = False
            self._game_begin_new_ = False

            #读取存档数据
            self.game_scene.read_save(self.save_manager.current_save,self.character_group)
            self.game_scene.init()
            self.game_scene.is_end = False


            #重置在游戏过程中的所有页面
            self.settings_scene.reset()
            self.settings_scene.is_end = True
            self.load_game_scene.reset()
            self.load_game_scene.is_end = True
            self.pause_page.reset()
            self.pause_page.is_end = True
    def _start_new_event_tp_(self,event:pygame.event.Event):
        """
        处理是否开始新游戏的按钮事件
        :param event:
        :return:
        """
        if self.tp_is_start.is_no_button_down(event):
            self.tp_is_start.no_button_value = True
        elif self.tp_is_start.is_yes_button_down(event):
            print("通过创建新存档来新游戏,开始游戏，开始界面结束")
            self.start_page.is_end = True

            self._on_game_begin_ = False
            self._game_begin_new_ = True
            self._game_begin_load_ = False

            #开启输入框开始游戏界面
            self.start_chapter.is_end = False

            #重置在游戏过程中的所有页面
            self.settings_scene.reset()
            self.settings_scene.is_end = True
            self.load_game_scene.reset()
            self.load_game_scene.is_end = True
            self.pause_page.reset()
            self.pause_page.is_end = True

    def _draw_start_menu_(self):
        self.start_page.draw()

        self.load_game_scene.draw()
        self.settings_scene.draw()
        self.quit_page.draw()
        self.tp_is_start.draw()

    def _game_init_(self):
        """
        初始化游戏
        :return:
        """
        pygame.init()
        pygame.display.set_caption("李好香の奇妙冒险", "陈海文陈海文の奇妙冒险")
        pygame.display.set_icon(pygame.image.load(r"resource/img/icon/caption.png"))
        self.screen = pygame.display.set_mode(size = (self.window_width, self.window_height),flags = Settings.screen_set[self.config["frame_settings"]["fullscreen_setting_index"]])
        self.clock = pygame.time.Clock()

        #开屏动画
        self.open_animation = OpenAnimation()
        self.open_animation.init()

    def _new_save_(self):
        """
        创建新存档
        :return:
        """
        #创建一个初始的存档
        SaveManager.current_save = SaveManager.init_save.copy()
        SaveManager.current_save_name = self.player.name
        #设置存档名称
        SaveManager.set_current_save_name(self.player.name)
        #保存存档数据
        self.save_manager.save_save_data(SaveManager.current_save)
        #添加存档数据到载入游戏界面
        self.load_game_scene.add_save_view(self.save_manager.current_save,self.player.name)

    def _load_(self):
        """
        加载资源
        :return:
        """
        print("_load_ 加载资源")
        self.loader.load_all_resource()
        self.save_manager.init_save_data()

    def draw_current_fps(self):
        """
        绘制当前帧率
        :return:
        """
        fps_text = "FPS: " + str(int(self.clock.get_fps()))
        fps_text_surface = ResourceLoader.font_dict["MiSansDemibold24"].render(fps_text, True, (255, 255, 255))
        self.screen.blit(fps_text_surface, (0, 0))

    def _draw_black_scr_(self):
        """
        绘制黑场
        :return:
        """
        if self.black_scr_alpha != 0:
            self.black_scr_alpha -= 5
            self.screen.blit(self.black_scr, (0, 0))
            self.black_scr.set_alpha(self.black_scr_alpha)

    def _draw_game_new_(self):
        """
        绘制游戏界面
        :return:
        """
        if self.start_chapter.is_end:
            self.game_scene.draw()

        self.start_chapter.draw()
        #绘制暂停界面
        self.pause_page.draw()

        #绘制载入游戏界面
        self.load_game_scene.draw()

        #绘制设置界面
        self.settings_scene.draw()

    def _is_other_end_pause_(self):
        """
        判断是否有其他页面显示
        :return:
        """
        return self.load_game_scene.is_end and  self.settings_scene.is_end

    def _pause_event_(self,event:pygame.event.Event):
        """
        处理暂停页面的事件
        :return:
        """
        #当按下ESC时，显示暂停界面
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and self._is_other_end_pause_():
            #判断是否已经显示过暂停界面
            if self.pause_page.is_end:
                self.pause_page.reset()
            else:
                self.pause_page.continue_button_value = True

        #当按下继续游戏按钮时，显示游戏界面
        if self.pause_page.is_continue_press(event) and not self.pause_page.is_end and self._is_other_end_pause_():
            self.pause_page.continue_button_value = True

        #当按下返回按钮时，返回开始菜单界面
        if self.pause_page.is_back_press(event) and not self.pause_page.is_end and self._is_other_end_pause_():
            self._back_to_start_menu_()

        #当按下载入游戏按钮时，显示载入游戏界面
        if self.pause_page.is_load_press(event) and not self.pause_page.is_end and self._is_other_end_pause_():
            self.load_game_scene.is_end = False

        if self.pause_page.is_setting_press(event) and not self.pause_page.is_end and self._is_other_end_pause_():
            self.settings_scene.is_end = False

    def _game_new_event_(self,event:pygame.event.Event):
        """
        处理新建游戏的事件
        :param event:
        :return:
        """
        #在暂停页面未显示时，处理开始章节的事件
        if  self.pause_page.is_end:
            #只有将玩家名重置之后,即StartChapter.is_end为True,才能开始游戏
            if self.start_chapter.is_end:
                self._game_scene_event_(event)

            self.start_chapter.handle_event(event)

        self._pause_event_(event)
        #处理由暂停页面引起的页面切换事件
        self._load_game_event_(event)
        self.settings_scene.handle_event(event)

        #设置界面内的保存按钮是否按下
        if self.settings_scene.is_settings_change():
            self._settings_event_()


        #当开始章节结束，且没有创建存档时，开始创建存档
        if self.start_chapter.is_end and not self.is_save_create and self.player.name is not None:
            self._new_save_()
            #游戏场景读取存档数据并初始化
            self.game_scene.read_save(SaveManager.current_save, self.character_group)
            self.game_scene.init()
            self.game_scene.is_end = False

            self.is_save_create = True

    def _draw_game_load_(self):
        self.game_scene.draw()

        #绘制暂停界面
        self.pause_page.draw()


        #绘制载入游戏界面
        self.load_game_scene.draw()

        #绘制设置界面
        self.settings_scene.draw()

    def _game_load_event_(self,event:pygame.event.Event):
        """
        _game_load_event_ 的 Docstring
        
        :param self: 说明
        :param event: 说明
        :type event: pygame.event.Event
        """

        self._pause_event_(event)

        #处理由暂停页面引起的页面切换事件
        self._load_game_event_(event)
        self._game_scene_event_(event)

        #设置界面内的保存按钮是否按下
        if self.settings_scene.is_settings_change():
            self._settings_event_()

        if self.load_game_scene.is_end and self.pause_page.is_end and self.settings_scene.is_end:
            self.game_scene.handle_event(event)

    def _draw_(self):
        """
        绘制
        :return:
        """
        #开屏动画
        self.open_animation.draw()

        #当开屏动画结束后才绘制页面
        if self.open_animation.is_black and self._on_game_begin_:
            #绘制开始菜单的界面
            self._draw_start_menu_()

            #开平动画结束之后的缓入效果
            self._draw_black_scr_()

        elif self._game_begin_new_:
            self._draw_game_new_()

        elif self._game_begin_load_:
            self._draw_game_load_()

    def run(self):
        self._game_init_()

        # 加载资源
        self._load_()
        while True:
            # 判断资源是否加载完成,如果加载完成则启动线程
            if self.is_load_finish():

                if not self.pages_group.is_pages_init() and not self.is_thread_start:
                    self.thread_init.start()

            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                self._handle_event_(event)
                print("事件处理完成")

            self._draw_()
            self.draw_current_fps()
            pygame.display.update()




if __name__ == '__main__':
    import os
    print("PID:",os.getpid())
    game = Game()
    game.run()