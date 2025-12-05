from Pages.Page import Page
from Elements.Button import Button
from Pages.framesetting import FrameSetting
from ResourceLoader import ResourceLoader
import pygame

class SettingsScene(Page):
    """
    游戏设置页面
    """

    def __init__(self,fullscreen_auto_index:int,resolution_auto_index:int):
        super().__init__()

        self.close_button_value = False  # 关闭按钮状态

        #黑场专场内容
        self.black_surface_list = [pygame.surface.Surface((3840, 2160)) for _ in range(13)]
        for i in range(13):
            self.black_surface_list[i].fill((0, 0, 0))
            self.black_surface_list[i].set_alpha(10 * i)

        self.black_surface_index = 0

        # 背景读取
        self.bg_copy = None  # 实际上使用的背景
        self.bg = ResourceLoader.bg_dict["SettingsPageBG"]#作为资源
        self.bg_h = -60
        self.bg_alpha = 0

        #按钮定义
        self._button_define_()

        #画面设置页面
        self.frame_setting = FrameSetting(fullscreen_auto_index,resolution_auto_index)

    def _button_define_(self):

        #关闭按钮初始化
        self.close_button = Button(ResourceLoader.button_dict["close_button"])
        self.close_button_value = False


        #画面设置按钮初始化
        self.frame_button = Button(ResourceLoader.button_dict["frame_setting_button"])
        self.isFrameSetting = False


    def reset_set(self):
        """
        重置设置
        :return:
        """
        #按钮值重置
        self.close_button_value = False


        self.frame_button.image = self.frame_button.animation_list[0]
        self.frame_button.setting_mode = 0
        self.frame_button.index = 0

        #下拉菜单重置
        self.frame_setting.reset()


    def is_settings_change(self)->bool:
        """
        判断是否有设置变更
        :return:
        """
        return self.frame_setting.is_settings_change()

    def set_settings_change(self,setting:bool)->None:
        """
        设置设置变更
        :return:
        """
        self.frame_setting.isSettingsChange = setting

    def init(self):
        """
        重载内容
        :return:
        """
        #背景初始化
        self.display_surface = pygame.display.get_surface()

        #使用bg_copy作为背景
        self.bg_copy = pygame.transform.scale(self.bg, (self.window_width, self.window_height))
        self.bg_copy.set_alpha(self.bg_alpha)

        #关闭按钮重置

        self.close_button.rect = self.close_button.image.get_rect()
        self.close_button.rect.left = int(self.window_width * 0.86)
        self.close_button.rect.top = int(self.window_height * 0.07)
        self.bg_copy.blit(self.close_button.image, self.close_button.rect)


        #画面设置按钮初始化
        self.frame_button.rect.left = int(self.window_width * 0.15)
        self.frame_button.rect.top = int(self.window_height * 0.2)
        self.bg_copy.blit(self.frame_button.image, self.frame_button.rect)


        #画面设置页面初始化
        self.frame_setting.init((int(0.3125*self.window_width),int(0.2*self.window_height)))
        self.frame_setting.bg_surface_rect.topleft = (int(0.3125*self.window_width),int(0.2*self.window_height))
        self.frame_setting.is_end = True

    def reset(self):
        self.is_end = False
        self.is_show = False
        #黑场重置
        self.black_surface_index = 0

        #背景重置
        self.bg_h = -60
        self.bg_alpha = 0
        self.bg_copy = pygame.transform.scale(self.bg, (self.window_width, self.window_height))

        #按钮值重置
        self.close_button_value = False


        self.frame_button.image = self.frame_button.animation_list[0]
        self.frame_button.setting_mode = 0
        self.frame_button.index = 0

        #下拉菜单重置
        self.frame_setting.reset()

    def get_fullscreen_set(self)->int:
        """
        获取当前全屏设置的索引
        :return:
        """
        return self.frame_setting.get_fullscreen_set()

    def get_resolution_set(self)->int:
        """
        获取当前分辨率设置的索引
        :return:
        """
        return self.frame_setting.get_resolution_set()

    def handle_event(self, event):
        """
        事件处理
        :param event:
        :return:
        """
        if self.is_end:
            self.is_show = False
            return

        self.close_button.hover_animation()

        #处理关闭按钮事件
        if self.close_button.is_press_down(event,(0,self.bg_h)):
            self.close_button_value = True

        #处理页面设置按钮
        if self.frame_button.is_press_down(event,(0,self.bg_h)):
                print("click")
                self.frame_button.set_mode()
                self.frame_setting.is_end = not self.frame_setting.is_end

        #处理界面设置页面事件
        self.frame_setting.handle_event(event)

    def _black_enter_(self):
        """
        黑场进入动画
        :return:
        """
        #黑场进入
        if not self.close_button_value:
            if self.black_surface_index <12:
                self.black_surface_index += 1
                self.bg_h += 5
                self.bg_alpha += 21
                self.bg_copy.set_alpha(self.bg_alpha)
                print(self.black_surface_index)
        else :
            #设置页面消失动画
            if self.black_surface_index > 0:
                self.black_surface_index -= 1
                self.bg_h -= 5
                self.bg_alpha -= 21
                print(self.black_surface_index)
                self.bg_copy.set_alpha(self.bg_alpha)

                if self.bg_alpha <= 0:
                    self.is_end = True

        #画面元素渲染
        self.display_surface.blit(self.black_surface_list[self.black_surface_index], (0, 0))
        self.display_surface.blit(self.bg_copy, (0, self.bg_h))

    def _draw_button_(self):
        self.bg_copy.blit(self.close_button.image, self.close_button.rect)

    def draw(self):
        """
        绘制
        :return:
        """

        if self.is_end:
            self.is_show = False
            return

        self.is_show = True
        #黑场动画
        self._black_enter_()

        #按钮渲染
        self._draw_button_()

        #画面设置页面渲染
        self.bg_copy.blit(self.frame_setting.bg_surface, self.frame_setting.bg_surface_rect)
        self.frame_setting.draw((int(0.3125*self.window_width),int(0.2*self.window_height)))

        #按钮渲染
        self.frame_button.setting_button_animation(False)
        self.bg_copy.blit(self.frame_button.image, self.frame_button.rect)

def test():
    """
    测试函数
    :return:
    """
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    clock = pygame.time.Clock()

    loader = ResourceLoader()
    loader.load_all_resource()
    loader.wait_load_finish()

    settings_page = SettingsScene(0,0)
    settings_page.init()

    while True:
        screen.fill("white")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            settings_page.handle_event(event)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            print("esc")
            settings_page.reset()

        screen.fill("white")
        settings_page.draw()

        clock.tick(60)
        pygame.display.update()

if __name__ == '__main__':
    test()

