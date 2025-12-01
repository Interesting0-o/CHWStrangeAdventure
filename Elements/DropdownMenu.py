import pygame
from Elements.MenuButton import MenuButton


class DropdownMenu:

    def __init__(self,
                 menu_options:list[str],          # 选项列表
                 option_size:tuple[int,int],      # 每个选项的大小
                 num:int,                         # 选项数量
                 menu_font:pygame.font.Font,      # 字体
                 bg_color = "white",              # 背景颜色
                 bg_hover_color = "#FFA500",      # 鼠标悬停颜色
                 font_color = "black",            # 字体颜色
                 font_hover_color = "white",      # 鼠标悬停颜色
                 auto_index:int = 0,               # 初始选中项索引


    ):
        """
        下拉菜单初始化
        :param menu_options:
        :param option_size:
        :param num:
        :param menu_font:
        :param bg_color:
        :param bg_hover_color:
        :param font_color:
        :param font_hover_color:
        """
        #初始化
        self.option_size = option_size
        self.num = num
        self.menu_font = menu_font
        self.bg_color = bg_color
        self.font_color = font_color
        self.current_index = auto_index  #当前选中项索引！！！
        self.menu_options = menu_options
        self.is_open = False
        self.select_index = 0
        self.options = []
        self.tar_location = None
        self.location = None

        #选项列表初始化
        for i in range(num):
            #未选中时图片
            img = pygame.Surface(option_size)
            img.fill(bg_color)
            img_rect = img.get_rect()
            img.blit(menu_font.render(self.menu_options[i], True, font_color),img_rect)
            #选中时图片
            img_hover = pygame.Surface(option_size)
            img_hover.fill(bg_hover_color)
            img_hover_rect = img_hover.get_rect()
            img_hover.blit(menu_font.render(self.menu_options[i], True, font_hover_color),img_hover_rect)
            img_rect.topleft = (0, i*option_size[1])
            self.options.append(MenuButton(
                img,
                img_hover,
                img_rect
            ))

        #收缩时背景rect
        self.current_option_bg = pygame.Surface(option_size) #收缩时背景
        self.current_option_bg_rect = self.current_option_bg.get_rect()
        self.current_option_bg.fill(self.bg_color)
        #收缩时显示的按钮
        self.current_show = MenuButton(
            self.options[auto_index].img_list[0],
            self.options[auto_index].img_list[1],
            self.options[0].rect
        )
        self.current_option_bg.blit(self.current_show.img,(0,0))

        #下拉时背景rect
        self.select_option_bg = pygame.Surface((option_size[0], option_size[1]*self.num))#下拉时背景
        self.select_option_bg_rect = self.select_option_bg.get_rect()
        self.select_option_bg.fill(self.bg_color)
        self.select_index = 0
        for button in self.options:
            self.select_option_bg.blit(button.img, button.rect)
            self.select_index += 1
        self.select_index = auto_index


    def is_hover(self,left_top:tuple[int,int] = (0,0)):
        """
        当图层被贴在其他图层上时，判断鼠标是否悬停在收缩时背景上
        :param left_top:
        :return:
        """
        center_x,center_y =pygame.mouse.get_pos()
        return self.current_option_bg_rect.collidepoint((center_x - left_top[0], center_y - left_top[1]))

    def is_press(self,left_top:tuple[int,int] = (0,0)):
        """
        当图层被贴在其他图层上时，判断鼠标是否按下在收缩时背景上
        :param left_top:
        :return:
        """
        return self.is_hover(left_top) and pygame.mouse.get_pressed()[0]


    def current_visible(self,display:bool = True):
        """
        使得否显示收缩时背景
        :param display:
        :return:
        """

        if display:
            self.current_option_bg.set_alpha(255)
        else:
            self.current_option_bg.set_alpha(0)

    def select_visible(self,display:bool = True):
        """
        使得否显示下拉时背景
        :param display:
        :return:
        """
        if display:
            self.select_option_bg.set_alpha(255)
        else:
            self.select_option_bg.set_alpha(0)


    def select_option_animation_blit(self,left_top:tuple[int,int]):
        for i in range(self.num):
            self.options[i].hover_animation(left_top)
            self.select_option_bg.blit(self.options[i].img, self.options[i].rect)

            if __name__ == "__main__":
                #测试用
                print(i,self.options[i].rect.topleft)

            if self.options[i].is_press(left_top):
                self.current_show = MenuButton(
                    self.options[i].img_list[0],
                    self.options[i].img_list[1],
                    self.current_show.rect
                )
                self.current_index = i
                self.is_open = False


    def handle_event(self,event):
        """
        事件监听
        :param event:
        :return:
        """
        #通过事件监听判断是否打开下拉列表

        if self.location is not None and self.current_show.is_hover((self.tar_location[0]+self.location[0],self.tar_location[1]+self.location[1])):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.is_open:
                    self.is_open = False
                else:
                    self.is_open = True


    def draw(self,
             bg_surface,#背景图层
             location: tuple[int, int]  # bg_surface的左上角坐标
             ):

        self.location = location

        #收缩时表单的选项动画
        self.current_show.hover_animation((
            self.tar_location[0] + self.location[0], self.tar_location[1] + self.location[1]
        ))
        self.current_option_bg.blit(self.current_show.img, (0, 0))
        #下拉列表的选项动画
        if self.is_open:
            bg_surface.blit(self.select_option_bg, self.select_option_bg_rect)
            self.select_option_animation_blit((self.tar_location[0]+self.location[0],
                                               self.tar_location[1]+self.location[1]+self.option_size[1]))
        #绘制收缩时背景
        bg_surface.blit(self.current_option_bg, self.current_option_bg_rect)

    def init(self,
             tar_location: tuple[int, int] =(0,0),  # 图层的左上角坐标
             ):
        self.tar_location = tar_location
        self.current_option_bg_rect.topleft = tar_location
        self.select_option_bg_rect.topleft = (tar_location[0], tar_location[1] + self.option_size[1])
        # 收缩时表单的选项动画
        self.current_option_bg.blit(self.current_show.img, (0, 0))


    def get_index(self):
        return self.current_index

    def set_index(self, index: int):
        self.current_index = index

    def set_open(self, is_open: bool):
        self.is_open = is_open

def test():
    from ResourceLoader import ResourceLoader


    loader = ResourceLoader()
    loader.load_all_resource()
    loader.wait_load_finish()

    def show_pos(bg_surface):
        text = "鼠标位置：{}".format(pygame.mouse.get_pos())
        font1 = ResourceLoader().font_dict["MiSansDemibold24"]
        text_surface = font1.render(text, True, (0, 0, 0))
        bg_surface.blit(text_surface, (100, 100))


    """
    测试函数
    :return:
    """
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    font = ResourceLoader().font_dict["MiSansDemibold24"]
    options = ["选项1", "选项2", "选项3", "选项4"]
    options2 = ["选项1", "选项2", "选项3", "选项4", "选项5"]

    dropdown_menu = DropdownMenu(options, (100, 30), 4,  menu_font=font)
    dropdown_menu2 = DropdownMenu(options2, (100, 30), 5, menu_font=font)
    color = pygame.surface.Surface((500, 500))
    color.fill("blue")
    dropdown_menu.init(
        tar_location=(100, 100),
    )
    dropdown_menu2.init(
        tar_location=(100, 300),
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            dropdown_menu.handle_event(event)
            dropdown_menu2.handle_event(event)



        screen.fill((255, 255, 255))
        screen.blit(color, (100, 100))
        color.fill("blue")
        dropdown_menu.draw(color,location=(100, 100))
        dropdown_menu2.draw(color, location=(100, 100))
        show_pos(screen)
        pygame.display.update()


if __name__ == '__main__':
   test()