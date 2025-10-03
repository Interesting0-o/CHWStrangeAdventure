import pygame
from Pages.Page import Page


class PausePage(Page):
    def __init__(self):
        super().__init__()
        #黑场资源
        self.black_bg_alpha = None
        self.black_bg = None
        #背景资源
        self.quit_window_alpha = 0
        self.quit_window = None
        self.quit_window.set_alpha(0)
        self.quit_window_rect = None
