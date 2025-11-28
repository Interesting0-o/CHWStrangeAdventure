import pygame

class MenuButton:
    """
    专为菜单按钮设计的类
    """
    def __init__(self,
                 img:pygame.Surface,       #正常显示时的图片
                 img_hover:pygame.Surface, #鼠标悬停时的图片
                 img_rect,            #图片的位置
                 ):
        #初始化
        self.img_list = [img,img_hover,img]
        self.img = img
        self.rect = img_rect


    def is_hover(self,left_top:tuple[int,int] = (0,0)):
        """
        判断鼠标是否悬停在按钮上
        :return:
        """
        center_x,center_y =pygame.mouse.get_pos()
        return True if self.rect.collidepoint((center_x - left_top[0], center_y - left_top[1])) else False

    def hover_animation(self,left_top:tuple[int,int] = (0,0)):
        """
        鼠标悬停动画
        :return:
        """
        self.img = self.img_list[0] if self.is_hover(left_top) else self.img_list[1]


    def is_press(self,left_top:tuple[int,int] = (0,0)):
        """
        判断鼠标是否按下,长按会一直触发该事件
        :param left_top:
        :return:
        """
        return True if self.is_hover(left_top) and pygame.mouse.get_pressed()[0] else False


    def is_pressed_down(self,event:pygame.event.Event,left_top:tuple[int,int] = (0,0)):
        """
        判断鼠标是否按下返回事件
        :param left_top:
        :param event:
        :return:
        """
        return True if self.is_hover(left_top) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1  else False

    def draw(self,
             bg_surface:pygame.Surface,#背景Surface
             left_top:tuple[int,int] = (0,0),#b背景Surface的左上角坐标
             ):

        self.hover_animation(left_top)
        bg_surface.blit(self.img,self.rect)





def test():
    """
    测试函数
    :return:
    """
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
        img.get_rect()
    )

    button.rect.center = (640, 360)

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if button.is_pressed_down(event):
                print("按下")


        button.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    test()
