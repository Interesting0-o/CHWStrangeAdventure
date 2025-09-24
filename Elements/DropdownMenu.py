import pygame
from Elements.MenuButton import MenuButton


class DropdownMenu:
    is_open =False
    hover = False
    pressed = False
    select_index = 0
    options = []
    options_rect =[]
    def __init__(self,
                 menu_options:list[str],          # 选项列表
                 option_size:tuple[int,int],      # 每个选项的大小
                 num:int,                         # 选项数量
                 menu_font:pygame.font.Font,      # 字体
                 bg_color = "white",              # 背景颜色
                 bg_hover_color = "#FFA500",      # 鼠标悬停颜色
                 font_color = "black",            # 字体颜色
                 font_hover_color = "white",      # 鼠标悬停颜色
                 auto_index:int = 0               # 初始选中项索引
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

        #选项列表初始化
        for i in range(num):
            #未选中时图片
            img = pygame.Surface(option_size)
            img.fill(bg_color)
            img_rect = img.get_rect()
            img.blit(menu_font.render(menu_options[i], True, font_color),img_rect)
            #选中时图片
            img_hover = pygame.Surface(option_size)
            img_hover.fill(bg_hover_color)
            img_hover_rect = img_hover.get_rect()
            img_hover.blit(menu_font.render(menu_options[i], True, font_hover_color),img_hover_rect)
            self.options.append(MenuButton(
                img,
                img_hover
            ))
            img_rect.lefttop = (0, i*option_size[1]+i*2)
            self.select_index += 1
            self.options_rect.append(img_rect)

        #收缩时背景rect
        self.current_option_bg = pygame.Surface(option_size) #收缩时背景
        self.current_option_bg_rect = self.current_option_bg.get_rect()
        self.current_option_bg.fill(self.bg_color)
        self.current_show = self.options[auto_index]
        self.current_option_bg.blit(self.current_show.img,(0,0))

        #下拉时背景rect
        self.select_option_bg = pygame.Surface((option_size[0]+10, option_size[1]*self.num+self.num*2))#下拉时背景
        self.select_option_bg_rect = self.select_option_bg.get_rect()
        self.select_option_bg.fill(self.bg_color)
        self.select_index = 0
        for button in self.options:
            self.select_option_bg.blit(button.img, self.options_rect[self.select_index])
            self.select_index += 1
        self.select_index = auto_index



    def is_hovered(self):
        """
        判断鼠标是否悬停在收缩时背景上
        :return:
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.current_option_bg_rect.collidepoint(mouse_pos):
            self.hover = True
            return True
        else:
            self.hover = False
            return False

    def is_hovered_blite(self,left_top:tuple[int,int]):
        """
        当图层被贴在其他图层上时，判断鼠标是否悬停在收缩时背景上
        :param left_top:
        :return:
        """
        center_x,center_y =pygame.mouse.get_pos()
        if self.current_option_bg_rect.collidepoint((center_x - left_top[0], center_y - left_top[1])):
            self.hover = True
            return True
        else:
            self.hover = False
            return False
    def is_pressed(self):
        """
        判断鼠标是否按下在收缩时背景上
        :return:
        """
        if self.is_hovered() and pygame.mouse.get_pressed()[0]:
            self.pressed = True
            return True
        else:
            self.pressed = False
            return False
    def is_pressed_blite(self,left_top:tuple[int,int]):
        """
        当图层被贴在其他图层上时，判断鼠标是否按下在收缩时背景上
        :param left_top:
        :return:
        """
        if self.is_hovered_blite(left_top) and pygame.mouse.get_pressed()[0]:
            self.pressed = True
            return True
        else:
            self.pressed = False
            return False

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


    def draw(self,bg_surface,
             location:tuple[int,int]#bg_surface的左上角坐标
             ):
        #对下拉列表进行重新定位
        self.current_option_bg_rect.lefttop = location
        self.select_option_bg_rect.lefttop = (location[0],location[1] + self.option_size[1])



        self.current_show.hover_animation_blit(location)
        if self.is_pressed():
            self.select_visible(True)
            self.current_visible(False)




        bg_surface.blit(self.current_option_bg, self.current_option_bg_rect)
        bg_surface.blit(self.select_option_bg, self.select_option_bg_rect)




if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    font = pygame.font.Font(r"E:\code\GameDemo\resource\font\MiSans\MiSans-Demibold.ttf",20 )
    options = ["选项1", "选项2", "选项3", "选项4"]

    dropdown_menu = DropdownMenu(options, (100, 30), 4, font, (255, 255, 255))

    # font = pygame.font.Font("../resource/font/萝莉体 第二版.ttf",20)
    # img = pygame.Surface((100,50))
    # img.fill("white")
    # img.blit(font.render("nihao", True, "black"), (0,0))



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


        screen.fill((255, 255, 255))
        dropdown_menu.draw(screen, (0,0))
        pygame.display.update()
