import pygame

class MenuButton:
    """
    专为菜单按钮设计的类
    """
    hover:bool = False
    pressed:bool = False
    is_selected:bool = False

    def __init__(self,
                 img:pygame.Surface,       #正常显示时的图片
                 img_hover:pygame.Surface, #鼠标悬停时的图片
                 img_rect,            #图片的位置
                 ):
        #初始化
        self.img_list = [img,img_hover,img]
        self.img = img
        self.rect = img_rect


    def is_hovered(self):
        """
        判断鼠标是否悬停在按钮上
        :return:
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.hover = True
            return True
        else:
            self.hover = False
            return False


    def is_hovered_blit(self,left_top:tuple[int,int]):
        """
        当图层贴至其他图层时，判断鼠标是否悬停在按钮上
        :param left_top:
        :return:
        """
        center_x,center_y =pygame.mouse.get_pos()
        if self.rect.collidepoint((center_x - left_top[0], center_y - left_top[1])):
            self.hover = True
            return True
        else:
            self.hover = False
            return False

    def hover_animation(self):
        """
        鼠标悬停动画
        :return:
        """

        if self.is_hovered():
            self.img = self.img_list[1]
        else:
            self.img = self.img_list[0]

    def hover_animation_blit(self,left_top:tuple[int,int]):
        """
        当图层贴至其他图层时，鼠标悬停动画
        :param left_top:
        :return:
        """
        if self.is_hovered_blit(left_top):
            self.img = self.img_list[1]
        else:
            self.img = self.img_list[0]

    def is_pressed(self):
        """
        判断鼠标是否按下
        :return:
        """
        if self.is_hovered() and pygame.mouse.get_pressed()[0]:
            self.pressed = True
            return True
        else:
            self.pressed = False
            return False

    def is_pressed_blit(self,left_top:tuple[int,int]):
        """
        当图层贴至其他图层时，判断鼠标是否按下
        :param left_top: 上级图层的左上角坐标
        :return:
        """
        if self.is_hovered_blit(left_top) and pygame.mouse.get_pressed()[0]:
            self.pressed = True
            return True
        else:
            self.pressed = False
            return False


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    img = pygame.Surface((100, 50))
    img.fill("white")
    img_hover = pygame.Surface((100, 50))
    img_hover.fill("red")
    button = MenuButton(
        img,
        img_hover,
    )
    button.rect.center = (640, 360)

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.blit(button.img, button.rect)
        button.hover_animation()
        pygame.display.update()
