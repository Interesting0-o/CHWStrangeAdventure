import pygame

class Page:
    path  = __file__[:-8]

    def __init__(self):
        self.window_width = 1280
        self.window_height = 720
        self.window_fps = 60
        self.display_surface = None
        self.is_end = False

    def init(self):
        """
        子类实现初始化方法
        :return:
        """
        pass


    def draw(self,*agrs):
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
    def set_window_size(self, width:int, height:int):
        """
        设置窗口大小
        :param width:
        :param height:
        :return:
        """
        self.window_width = width
        self.window_height = height



if __name__ == '__main__':
    page = Page()
    print(page.path)
