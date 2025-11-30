import pygame
from ResourceLoader import ResourceLoader
from Elements.Button import Button
from Elements.MenuButton import MenuButton
from Pages.Page import Page
from SaveManager import SaveManager


class LoadGamePage(Page):
    def __init__(self):
        super().__init__()

        #黑场资源载入
        self.black_surface = pygame.Surface((3840, 2160))
        self.black_surface_alpha = 0

        #背景资源载入
        self.bg = ResourceLoader.bg_dict["SettingsPageBG"]
        self.bg_scale = None #声明背景缩放后的Surface
        self.bg_h = -55 #声明背景高度
        self.bg_alpha = 0 #声明背景透明度

        #定义按钮
        self._button_define_()

        #存档数据
        self.save_data = {}
        self.save_view_list = []


    def _button_define_(self):
        #关闭按钮初始化
        self.close_button = Button(ResourceLoader.button_dict["close_button"])
        self.close_button.animation_list = ResourceLoader.button_dict["close_button"]
        self.close_button_value = False

        #翻页按钮初始化
        next_img = pygame.transform.scale(ResourceLoader.icon_dict["next"], (70, 70))
        next_img_hover = pygame.transform.scale(ResourceLoader.icon_dict["next_hover"], (70, 70))
        self.next_button =MenuButton(
            next_img,
            next_img_hover,
            next_img.get_rect()
        )
        last_img = pygame.transform.scale(ResourceLoader.icon_dict["last"], (70, 70))
        last_img_hover = pygame.transform.scale(ResourceLoader.icon_dict["last_hover"], (70, 70))
        self.last_button = MenuButton(
            last_img,
            last_img_hover,
            last_img.get_rect()
        )

        #删除按钮初始化
        delete = pygame.transform.scale(ResourceLoader.icon_dict["delete"], (48, 64))
        delete_hover = pygame.transform.scale(ResourceLoader.icon_dict["delete_hover"], (48, 64))
        self.delete_button = MenuButton(
            delete,
            delete_hover,
            delete.get_rect()
        )


    class SaveView:

        def __init__(self,
                     save_data:dict,
                     delete_button:MenuButton,
                     ):
            self.save_data = save_data
            self.delete_button = delete_button

            self.bg = None #声明背景Surface

        def init(self,window_width:int,window_height:int):

            try:
                bg = self.save_data["bg"]
                self.bg = pygame.transform.scale(ResourceLoader.chapter_bg_dict[bg],(window_width,window_height))
            except KeyError:
                print("背景不存在,未来实现")

        def handle_event(self,event:pygame.event.Event):
            pass




    def save_load(self,save_data:dict):
        """
        读取存档数据
        :param save_data:
        :return:
        """
        self.save_data.clear()
        self.save_data = save_data

        # 清空存档视图列表
        self.save_view_list.clear()
        self.save_view_list = [self.SaveView(save,MenuButton(
                self.delete_button.img_list[0],
                self.delete_button.img_list[1],
                self.delete_button.rect.copy()
            ))
            for name,save in self.save_data.items()
        ]


    def reset(self):
        super().reset()

        #黑场资源重置
        self.black_surface_alpha = 0
        self.bg_h = -55
        self.bg_alpha = 0



    def init(self):
        self.display_surface = pygame.display.get_surface()

        #缩放背景
        self.bg_scale = pygame.transform.scale(self.bg, (self.window_width, self.window_height))

        #初始化存档视图列表
        for save_view in self.save_view_list:
            save_view.init(self.window_width,self.window_height)


    def handle_event(self, event):
        """
        处理事件
        :param event:
        :return:
        """
        pass

    def black_enter(self):
        """
        黑场进入动画
        :return:
        """
        # 黑场进入
        if not self.close_button_value:
            if self.black_surface_alpha < 120:
                self.black_surface_alpha += 10
                self.black_surface.set_alpha(self.black_surface_alpha)
                self.bg_h += 5
                self.bg_alpha += 21
                self.bg_scale.set_alpha(self.bg_alpha)

        else:
            # 设置页面消失动画
            if self.black_surface_alpha > 0:
                self.black_surface_alpha -= 10
                self.black_surface.set_alpha(self.black_surface_alpha)
                self.bg_h -= 5
                self.bg_alpha -= 21
                self.bg_scale.set_alpha(self.bg_alpha)
                if self.bg_alpha <= 0:
                    self.is_end = True
                    print("退出设置页面")
        self.display_surface.blit(self.black_surface, (0, 0))
        self.display_surface.blit(self.bg_scale, (0, self.bg_h))

    def draw(self):
        if self.is_end:
            return

        self.black_enter()


def test():
    """
    测试函数
    :return:
    """
    loader = ResourceLoader()
    loader.load_all_resource()
    loader.wait_load_finish()


    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    save_manager = SaveManager()
    save_manager.init_save_data()

    page = LoadGamePage()
    page.init()

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            page.handle_event(event)
        keys =   pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            page.reset()
        screen.fill("white")
        page.draw()
        pygame.display.update()


if __name__ == '__main__':
    test()