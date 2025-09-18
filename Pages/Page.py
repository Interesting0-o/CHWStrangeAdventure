import pygame

class Page:
    """


    """
    window_width = 1280
    window_height = 720
    window_fps = 60
    display_surface = None
    is_end = False
    path  = __file__[:-8]


    def init(self):
        """
        子类实现初始化方法
        :return:
        """
        pass


    def draw(self):
        """
        子类实现绘制方法
        :return:
        """
        pass

    def rect_show(self,rect:pygame.Rect):
        """
        显示碰撞矩形
        :param rect:
        :return:
        """
        color = pygame.Surface(rect.size)
        color.set_colorkey("black")
        pygame.draw.rect(color,"red", (rect.x+2,rect.y+2,rect.width-4,rect.height-4),2)
        self.display_surface.blit(color, rect)




if __name__ == '__main__':
    page = Page()
    print(page.path)
