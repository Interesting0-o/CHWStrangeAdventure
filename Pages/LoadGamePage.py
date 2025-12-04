import pygame

from Pages.PagesGroup import PagesGroup
from ResourceLoader import ResourceLoader
from Elements.Button import Button
from Elements.MenuButton import MenuButton
from Pages.Page import Page
from Pages.TextPage import TextPage
from SaveManager import SaveManager


class LoadGameScene(Page):
    def __init__(self):
        super().__init__()

        self.save_manager:SaveManager = None #声明存档管理器

        self.close_button_value = False

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
        self.save_view_list:list[LoadGameScene.SaveView] = []


        #当前存档的页数
        self.page_num = 1
        self.page_text = []
        self.page_text_rect = []

        self.is_save_load = False #声明是否开始载入存档

        #textPage类型
        self.tp_group = PagesGroup()

        self.tp_is_load:TextPage = TextPage("是否载入存档?")
        self.tp_is_delete:TextPage = TextPage("是否删除存档?")
        self.tp_group.add_page(self.tp_is_load,self.tp_is_delete)

        self.to_empty_index:int = -1 #声明需要删除存档的索引
        self.to_load_index:int = -1 #声明需要载入存档的索引

    def _text_page_init_(self):
        """
        TextPage初始化
        :return:
        """
        self.tp_is_load.init()
        self.tp_is_delete.init()

        self.tp_is_load.is_end = True
        self.tp_is_delete.is_end = True

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

    def _button_init_(self):
        """
        按钮初始化
        :return:
        """
        #关闭按钮位置
        self.close_button.rect.left = int(Page.window_width * 0.86)
        self.close_button.rect.top = int(Page.window_height * 0.07)

        #设置按钮位置
        self.next_button.rect.center = (int(Page.window_width * 0.88), int(Page.window_height * 0.5))
        self.last_button.rect.center = (int(Page.window_width * 0.12), int(Page.window_height * 0.5))

    def _draw_button_(self):
        """
        绘制按钮
        :return:
        """
        #绘制关闭按钮
        self.close_button.draw(self.bg_scale)

        #绘制翻页按钮
        self.next_button.draw(self.bg_scale)
        self.last_button.draw(self.bg_scale)

    def _button_event_(self,event:pygame.event.Event):
        """
        按钮事件处理
        :param event:
        :return:
        """
        #添加按钮动画
        self.close_button.hover_animation()
        self.next_button.hover_animation()
        self.last_button.hover_animation()

        # 处理关闭按钮事件
        if self.close_button.is_press_down(event):
            self.close_button_value = True

        # 处理翻页按钮事件
        if self.next_button.is_press_down(event) and self.page_num < len(self.save_view_list)//6:
            self.page_num += 1
            if self.page_num > len(self.save_view_list)//6+1:
                self.page_num = 1
        if self.last_button.is_press_down(event) and self.page_num > 1:
            self.page_num -= 1
            if self.page_num < 1:
                self.page_num = len(self.save_view_list)//6+1

    def _sort_save_view_(self,is_init:bool = False):
        """
        快速排序存档视图列表，将不是空拍和错误的存档放在前面
        :return:
        """
        # 快速排序
        size = (int(Page.window_width * 0.2), int(Page.window_height * 0.3))

        self.save_view_list.sort(key=lambda x: x.ID,reverse=True)

        #设置存档视图位置
        for i in range(len(self.save_view_list)):
            if is_init:
                self.save_view_list[i].init(size[0], size[1])
            #设置存档视图位置
            self.save_view_list[i].set_location(int(Page.window_width*0.20+(i%6)%3*Page.window_width*0.21),
                                                 int(Page.window_height*0.20 +(i%6)//3*Page.window_height*0.32))




    class SaveView:

        empty_bg = None #声明空白背景
        error_bg = None #声明错误背景

        def __init__(self,
                     save_data:dict|None,
                     delete_button:MenuButton|None,
                     name:str|None,
                     is_empty:bool = False
                     ):
            # 存档数据
            self.is_empty = is_empty

            self.name = name
            self.save_data = save_data
            self.delete_button = delete_button

            self.bg = None #声明背景Surface
            self.bg_rect = None #声明背景Rect

            self.is_delete_press = False #声明是否按下删除按钮
            self.is_load_press = False #声明是否按下载入按钮

            self.ID:int = 0 #声明存档序数



        def _bg_init_(self,window_width:int,window_height:int):
            """
            正常背景初始化背景
            :return:
            """
            text = ResourceLoader.font_dict["MiSansDemibold24"].render(self.name, True, "white")
            self.bg = pygame.transform.scale(ResourceLoader.chapter_bg_dict[self.save_data["bg"]],
                                             (window_width, window_height)
                                             )
            self.bg.blit(text, text.get_rect(center=(window_width/2, window_height/2)))

        @staticmethod
        def error_bg_init(window_width:int,window_height:int):
            """
            错误背景初始化
            :return:
            """
            # 错误背景初始化
            LoadGameScene.SaveView.error_bg = pygame.Surface((window_width, window_height))
            LoadGameScene.SaveView.error_bg.fill("#aaaaaa")
            # 错误文字渲染
            text = ResourceLoader.font_dict["MiSansDemibold24"].render("Error", True, "white")

            LoadGameScene.SaveView.error_bg.blit(text, text.get_rect(center=(window_width/2, window_height/2)))

            print("error load")

        @staticmethod
        def empty_bg_init(window_width:int,window_height:int):
            """
            空白背景初始化
            :return:
            """
            LoadGameScene.SaveView.empty_bg = pygame.Surface((window_width, window_height))
            LoadGameScene.SaveView.empty_bg.fill("#aaaaaa")

            text = ResourceLoader.font_dict["MiSansDemibold24"].render("Empty", True, "white")

            LoadGameScene.SaveView.empty_bg.blit(text, text.get_rect(center=(window_width/2, window_height/2)))

            print("empty load")

        def init(self,window_width:int,window_height:int):
            #如果存档数据为空，则显示empty_bg
            if self.is_empty:
                self.bg = LoadGameScene.SaveView.empty_bg
                self.ID = 0


            #如果存档数据为Error，则显示error_bg
            elif self.save_data == "Error":
                self.bg = LoadGameScene.SaveView.error_bg
                self.ID = 1

            #否则显示正常背景
            else:
                self._bg_init_(window_width,window_height)
                self.ID = 3

        def set_location(self,x:int,y:int):
            """
            设置存档视图位置
            :param x:
            :param y:
            :return:
            """
            #设置存档视图位置
            self.bg_rect = self.bg.get_rect(topleft=(x,y))
            #设置删除按钮位置,只有在非空存档才显示
            if self.is_empty:
                return
            self.delete_button.rect.topleft = (x+self.bg_rect.width-self.delete_button.rect.width,y)

        def is_hover(self, left_top: tuple[int, int] = (0, 0)):
            """
            判断鼠标是否悬停在存档视图上
            :return:
            """
            center_x, center_y = pygame.mouse.get_pos()
            return self.bg_rect.collidepoint((center_x - left_top[0], center_y - left_top[1]))

        def is_press_down(self,event:pygame.event.Event,left_top:tuple[int,int] = (0,0)):
            """
            判断鼠标是否按下
            :param event:
            :param left_top:
            :return:
            """
            return True if self.is_hover(left_top) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 else False

        def tarns_to_empty(self):
            """
            转换为空白存档
            :return:
            """
            self.is_empty = True
            self.init(self.bg.get_width(),self.bg.get_height())

        def handle_event(self, event:pygame.event.Event):
            """
            处理事件
            :param event:
            :return:
            """
            # 当存档数据为空时，不处理事件
            if self.is_empty:
                return
            #添加按钮动画
            self.delete_button.hover_animation()

            #当错误存档时，只处理删除按钮事件
            if self.save_data == "Error" and self.delete_button.is_press_down(event):
                self.is_delete_press = True


            #当正常存档时，处理删除按钮和存档视图事件
            elif self.save_data != "Error":
                if not self.delete_button.is_hover() and self.is_press_down(event) :
                    self.is_load_press = True
                    print("存档视图被点击")

                #删除按钮按下时
                elif self.delete_button.is_press_down(event):
                    self.is_delete_press = True

        def draw(self,bg_surface:pygame.Surface):
            """
            绘制存档视图
            :param bg_surface:
            :return:
            """
            # 绘制背景
            bg_surface.blit(self.bg,self.bg_rect)
            # 绘制删除按钮，只有在非空存档才显示
            if not self.is_empty:
                self.delete_button.draw(bg_surface)

        def get_name(self):
            return self.name

    def _save_view_init_(self):
        """
        初始化存档视图列表的位置
        :return:
        """
        num = len(self.save_view_list)//6 * 6 + 6 - len(self.save_view_list)
        # 补充空白存档
        for i in range(num):
            self.save_view_list.append(self.SaveView(None,None,None,True))
        size = (int(Page.window_width*0.2),int(Page.window_height*0.3))

        self.SaveView.empty_bg_init(size[0],size[1])
        self.SaveView.error_bg_init(size[0],size[1])

        #排序并初始化存档视图
        self._sort_save_view_(True)

    def _draw_save_view_(self):
        """
        绘制存档视图
        :return:
        """
        for i in range(self.page_num*6-6,self.page_num*6):
            self.save_view_list[i].draw(self.bg_scale)

    def _save_view_event_(self,event:pygame.event.Event):
        """
        处理存档视图事件
        :param event:
        :return:
        """
        flag_empty = True
        flag_load = True

        if not self.tp_is_load.is_show and not self.tp_is_delete.is_show:
            for i in range(self.page_num*6-6,self.page_num*6):
                self.save_view_list[i].handle_event(event)

                #获取需要删除的存档索引
                if self.save_view_list[i].is_delete_press:
                    self.to_empty_index = i
                    flag_empty = False

                if self.save_view_list[i].is_load_press:
                    self.to_load_index = i
                    flag_load = False

        if flag_empty:
            self.to_empty_index = -1

        if flag_load:
            self.to_load_index = -1

    def save_load(self,save_manger:SaveManager):
        """
        读取存档数据
        :param save_manger:
        :return:
        """
        self.save_manager = save_manger
        self.save_data.clear()
        self.save_data = save_manger.save_datas

        # 清空存档视图列表
        self.save_view_list.clear()
        self.save_view_list = [self.SaveView(save,
                                             MenuButton(self.delete_button.img_list[0],self.delete_button.img_list[1],self.delete_button.rect.copy()),
                                             name[:-4]
                                             )
            for name,save in self.save_data.items()
        ]
        self.is_save_load = True

    def reset(self):
        self.is_end = False
        self.is_show = False

        #黑场资源重置
        self.black_surface_alpha = 0
        self.bg_h = -55
        self.bg_alpha = 0
        self.close_button_value = False

        #重置提示框
        self.tp_is_delete.reset()
        self.tp_is_delete.is_end = True
        self.tp_is_load.reset()
        self.tp_is_load.is_end = True

        #重置存档页数
        self.to_empty_index = -1


    def _page_num_init_(self):

        text_surface = [ResourceLoader.font_dict["loli36"].render(f"Page {i}", True, "black") for i in range(len(self.save_view_list)//6+1)]


        for surface in text_surface:
            #为所有的文字添加白色背景
            white = pygame.Surface((surface.get_size()[0]+5, surface.get_size()[1]+5))
            white.fill("white")
            white.blit(surface, (0, 0))
            self.page_text.append(white)

        #获取文字的位置
        self.page_text_rect =[ surface.get_rect(center=(Page.window_width/2, Page.window_height*0.85)) for surface in self.page_text]


    def _draw_page_(self):
        self.bg_scale.blit(self.page_text[self.page_num-1],self.page_text_rect[self.page_num-1])

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

    def _delete_event_(self,event:pygame.event.Event):
        """
        处理存档删除事件
        :param event:
        :return:
        """

        if self.to_empty_index !=-1:
            # 判断删除提示框是否未重载
            if not self.tp_is_delete.is_reset:
                self.tp_is_delete.reset()
                self.tp_is_delete.is_reset = True

            print("删除存档")
            self.tp_is_delete.is_end = False

            #处理是否载入提示框事件
            if self.tp_is_delete.is_no_button_down(event):
                # 重置提示框改为初始状态
                self.tp_is_delete.is_reset = False
                self.tp_is_delete.no_button_value = True
                print("no按钮被点击")

                #将存档视图恢复正常
                self.save_view_list[self.to_empty_index].is_delete_press = False
                self.to_empty_index = -1

            elif self.tp_is_delete.is_yes_button_down(event):
                print("yes按钮被点击")
                #删除存档
                self.save_view_list[self.to_empty_index].tarns_to_empty()

                #删除存档文件
                self.save_manager.delete_save_data(self.save_view_list[self.to_empty_index].name)

                # 删除提示框关闭,重置检测改为未重置
                self.tp_is_delete.is_reset = False
                self.tp_is_delete.no_button_value = True

                #将存档视图恢复正常
                self.save_view_list[self.to_empty_index].is_delete_press = False
                self.to_empty_index = -1

                #重新排序存档视图列表
                self._sort_save_view_()

    def _load_event_(self,event:pygame.event.Event):
        """
        处理存档加载事件
        :param event:
        :return:
        """
        if self.to_load_index !=-1:
            # 判断载入提示框是否未重载
            if not self.tp_is_load.is_reset:
                self.tp_is_load.reset()
                self.tp_is_load.is_reset = True

                print("载入存档")
                self.tp_is_load.is_end = False

            #处理是否载入提示框事件
            if self.tp_is_load.is_no_button_down(event):
                # 重置提示框改为初始状态
                self.tp_is_load.is_reset = False
                self.tp_is_load.no_button_value = True
                print("no按钮被点击")

                #将存档视图恢复正常
                self.save_view_list[self.to_load_index].is_load_press = False
                self.to_load_index = -1

            elif self.tp_is_load.is_yes_button_down(event):
                print("yes按钮被点击")
                #载入存档
                SaveManager.current_save = self.save_view_list[self.to_load_index].save_data

                # 载入提示框关闭,重置检测改为未重置
                self.tp_is_load.is_reset = False
                self.tp_is_load.no_button_value = True

                #将存档视图恢复正常
                self.save_view_list[self.to_load_index].is_load_press = False
                self.to_load_index = -1




    def init(self):
        self.display_surface = pygame.display.get_surface()

        #tp初始化
        self._text_page_init_()

        #缩放背景
        self.bg_scale = pygame.transform.scale(self.bg, (Page.window_width, Page.window_height))

        #初始化存档视图列表
        for save_view in self.save_view_list:
            save_view.init(Page.window_width,Page.window_height)

        #初始化页数
        self._page_num_init_()

        #初始化存档页
        self._save_view_init_()

        #初始化按钮
        self._button_init_()

    def is_other_show(self):
        """
        判断是否有其他提示框显示
        :return:
        """
        return self.tp_is_load.is_show or self.tp_is_delete.is_show

    def handle_event(self, event: pygame.event.Event):
        """
        处理事件
        :param event:
        :return:
        """
        # 判断是否关闭按钮被点击
        if self.is_end:
            self.is_show = False
            return
        if not self.is_other_show():
            #处理按钮事件
            self._button_event_(event)

            #处理存档视图事件
            self._save_view_event_(event)


        #存档删除事件
        self._delete_event_(event)

        #存档载入事件
        self._load_event_(event)

    def draw(self):
        if self.is_end:
            return

        self.is_show = True

        #黑场动画
        self.black_enter()

        #渲染存档页数
        self._draw_page_()

        #渲染按钮
        self._draw_button_()

        #渲染存档视图
        self._draw_save_view_()

        #渲染是否载入提示框
        self.tp_is_load.draw()

        #渲染是否删除提示框
        self.tp_is_delete.draw()


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
    save_manager.wait_load_finish()

    page = LoadGameScene()
    page.save_load(save_manager)
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