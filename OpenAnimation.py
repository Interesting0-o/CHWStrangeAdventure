import pygame
from settings import Settings
import threading
from Save_Load import SaveLoad

class OpenAnimation:
    display_surface = None
    animation_list = [None for i in range(300)]
    animation_list_index = 0
    is_end = False


    def __init__(self):
        self.window_width = 1280
        self.window_height = 720
        #导入动画图片
        self.current_surface = None
        SaveLoad().LoadImage_fileDir(rf"resource/video/openVideo", self.animation_list)


    def init(self):
        #缩放动画图片
        try:
            for i in range(0,300):
                self.animation_list[i] = pygame.transform.scale(self.animation_list[i],
                                                                (
                                                                    self.window_width,
                                                                    self.window_height
                                                                ))
        except Exception as e:
            print("Animation init error:", e)
            exit()
        self.current_surface = self.animation_list[0]
        self.display_surface = pygame.display.get_surface()

    def draw(self):
        if not self.is_end:
            if self.animation_list_index < 299:
                self.current_surface = self.animation_list[self.animation_list_index]
                self.animation_list_index += int(60/Settings.FPS)
                if self.animation_list_index == 299:
                    self.is_end = True

            self.display_surface.blit(self.current_surface, (0, 0))
    def set_window_size(self, width, height):
        self.window_width = width
        self.window_height = height


if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    open_animation = OpenAnimation()
    open_animation.init()

    while True:
        clock.tick(Settings.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        open_animation.draw()
        pygame.display.update()