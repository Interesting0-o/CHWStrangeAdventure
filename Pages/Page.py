import pygame
from abc import ABC, abstractmethod
class Page(ABC):
    path  = __file__[:-8]

    @abstractmethod
    def __init__(self):
        self.window_width = 1280
        self.window_height = 720
        self.window_fps = 60
        self.display_surface = None
        self.is_end = False

    @abstractmethod
    def init(self):
        """
        子类实现初始化方法
        :return:
        """
        pass


    def handle_event(self, event):
        """
        子类有选择的实现事件处理方法
        :param event:
        :return:
        """
        pass

    @abstractmethod
    def draw(self):
        """
        子类实现绘制方法
        :return:
        """
        pass

    @abstractmethod
    def reset(self):
        """
        子类实现重置方法
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

    def set_window_size(self, width:int = -1, height:int = -1 ,
                        size:tuple[int,int] = (-1,-1)
                        ):
        """
        传入两个参数，或者一个元组参数，设置窗口大小
        :param size:
        :param width:
        :param height:
        :return:
        """
        if width != -1 and height != -1 :
            self.window_width = width
            self.window_height = height
        else:
            self.window_width, self.window_height = size



if __name__ == '__main__':

    class MyPage(Page):
        def __init__(self):
            super().__init__()
        def init(self):
            print("init")
        def handle_event(self, event):
            print("handle_event")
        def draw(self):
            print("draw")
        def reset(self):
            print("reset")
    a = MyPage()
    print(a.path)
