import pygame
from abc import ABC, abstractmethod
class Page(ABC):
    path  = __file__[:-8]
    window_width = 1280
    window_height = 720
    window_fps = 60


    def __init__(self):
        self.display_surface = None
        self.is_end = False
        self.is_show = False


    @abstractmethod
    def init(self):
        """
        子类实现初始化方法
        :return:
        """
        ...

    @abstractmethod
    def handle_event(self, event):
        """
        子类有选择的实现事件处理方法
        :param event:
        :return:
        """
        ...

    @abstractmethod
    def draw(self):
        """
        子类实现绘制方法
        :return:
        """
        ...

    @abstractmethod
    def reset(self):
        """
        子类实现重置方法
        :return:
        """
        ...

    @staticmethod
    def rect_show(rect:pygame.Rect)->None:
        """
        显示碰撞矩形
        :param rect:
        :return:
        """
        color = pygame.Surface(rect.size)
        color.set_colorkey("black")
        pygame.draw.rect(color,"red", (rect.x+2,rect.y+2,rect.width-4,rect.height-4),2)
        pygame.display.get_surface().blit(color, rect)


    @staticmethod
    def set_window_size(width:int , height:int)->None:
        """
        传入两个参数，或者一个元组参数，设置窗口大小
        :param width:
        :param height:
        :return:
        """
        Page.window_width = width
        Page.window_height = height



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
