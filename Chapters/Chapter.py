import pygame

class Chapter:

    def __init__(self):

        self.window_width = 1280
        self.window_height = 720
        self.display_surface = None
        self.is_end = False
        self.path = __file__[:-11]


    def set_window_size(self, width: int, height: int):
        """
        设置窗口大小
        :param width:
        :param height:
        :return:
        """
        self.window_width = width
        self.window_height = height

    def init(self):
        pass

    def handle_event(self, event):
        pass

    def show(self):
        pass
