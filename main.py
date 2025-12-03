import pygame
import json
import threading

from Pages import *
from ResourceLoader import ResourceLoader
from SaveManager import SaveManager
from settings import Settings


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
        self.is_thread_start = False
        self.is_thread_finish = False
        self.thread_init = threading.Thread(target=self._threading_start_)

    def get_size_by_set(self):
        return Settings.screen_size[self.config["frame_settings"]["resolution_size_index"]]



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
        self.load_game_page:LoadGamePage = LoadGamePage()
        self.pause_page:PausePage = PausePage()
        try:
            self.settings_page:SettingsPage = SettingsPage(self.config["frame_settings"]["fullscreen_setting_index"],
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
                                   self.load_game_page,
                                   self.pause_page,
                                   self.settings_page,
                                   self.quit_page,
                                   self.start_chapter
                                  )

    def _page_init_(self):
        self.pages_group.pages_init()

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
        #页面组初始化
        self._page_define_()
        self.load_game_page.save_load(self.save_manager)
        self._page_init_()
        self.pages_group.change_page_end()

        self.is_thread_finish = True
        print("_threading_start_ 线程启动完成")



    def _handle_event_(self,event:pygame.event.Event):
        """
        处理事件
        :param event:
        :return:
        """
        #在资源加载完成后才处理事件
        if self.is_load_finish() and self.is_thread_finish:
            self.open_animation.handle_event(event)

            if self.open_animation.is_black:
                self.start_page.is_end = False
                self._start_menu_event_(event)

    def _is_other_show_(self):
        """
        判断开始菜单界面是否有其他页面显示
        :return:
        """
        return self.load_game_page.is_show or self.settings_page.is_show or self.quit_page.is_show




    def _start_menu_event_(self,event:pygame.event.Event):
        """
        处理开始菜单的按钮事件
        :param event:
        :return:
        """
        # 处理开始按钮事件
        if self.start_page.is_start_down(event) and not self._is_other_show_():
            pass

        # 处理载入游戏按钮事件
        elif self.start_page.is_load_down(event) and not self._is_other_show_():
            print("载入游戏")
            self.load_game_page.reset()

        # 处理设置按钮事件
        elif self.start_page.is_settings_down(event) and not self._is_other_show_():
            print("设置")
            self.settings_page.reset()

        # 处理退出按钮事件
        elif self.start_page.is_quit_down(event) and not self._is_other_show_():
            print("退出游戏")
            self.quit_page.reset()

        # 处理退出，设置，载入游戏页面事件
        self.quit_page.handle_event(event)
        self.settings_page.handle_event(event)
        self.load_game_page.handle_event(event)

    def _draw_start_menu_(self):
        self.start_page.draw()

        self.load_game_page.draw()
        self.settings_page.draw()
        self.quit_page.draw()

    def _game_init_(self):
        """
        初始化游戏
        :return:
        """
        pygame.init()
        pygame.display.set_caption("陈海文の奇妙冒险", "陈海文陈海文の奇妙冒险")
        pygame.display.set_icon(pygame.image.load(r"resource/img/icon/caption.png"))
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()

        #开屏动画
        self.open_animation = OpenAnimation()
        self.open_animation.init()

    def _load_(self):
        """
        加载资源
        :return:
        """
        print("_load_ 加载资源")
        self.loader.load_all_resource()
        self.save_manager.init_save_data()

    def _draw_(self):
        #开屏动画


        self.open_animation.draw()

        #当开屏动画结束后才绘制页面
        if self.open_animation.is_black:
            self._draw_start_menu_()

            #开平动画结束之后的缓入效果
            if self.black_scr_alpha != 0:
                self.black_scr_alpha -= 5
                self.screen.blit(self.black_scr, (0, 0))
                self.black_scr.set_alpha(self.black_scr_alpha)


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

            self._draw_()
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()