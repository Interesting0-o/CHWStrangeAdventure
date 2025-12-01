import pygame
from settings import Settings
import threading

class OpenAnimation:
    display_surface = None
    animation_list = [None for i in range(300)]
    animation_list_index = 0
    is_end = False
    path = __file__[:-17]

    def __init__(self):

        self.window_width = 1280
        self.window_height = 720
        #导入动画图片
        self.current_surface = None
        self.index = 0



    def init(self):
        #缩放动画图片
        self.display_surface = pygame.display.get_surface()

    def draw(self):
        if self.is_end:
            return

        self.current_surface = pygame.image.load(self.path + rf"\resource\video\openVideo\Open_Animation_{self.index:03d}.png" )
        self.current_surface = pygame.transform.scale(self.current_surface, (self.window_width, self.window_height))
        self.index += 1
        self.display_surface.blit(self.current_surface, (0, 0))

        if self.index >= 300:
            self.is_end = True
    def set_window_size(self, width, height):
        self.window_width = width
        self.window_height = height


def test():
    """
    测试函数
    :return:
    """
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    open_animation = OpenAnimation()
    open_animation.init()

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        open_animation.draw()
        pygame.display.update()

        print(clock.get_fps())

def test2():
    print(OpenAnimation.path)

if __name__ == '__main__':
    test()
