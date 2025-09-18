import pygame
from settings import Settings
import threading
class OpenAnimation:
    window_width =Settings.M_WIDTH
    window_height =Settings.M_HEIGHT
    display_surface = None
    animation_list = [None for i in range(300)]
    animation_list_index = 0
    is_end = False

    def thread_read_func(self,tuple_data:tuple[int,int]):
        for i in range(tuple_data[0],tuple_data[1]):
            self.animation_list[i] = pygame.image.load(
                rf"resource/video/openVideo/Open_Animation_{i:03d}.png"
            )

    def __init__(self):
        #导入动画图片
        self.current_surface = None
        threading_list = []
        for i in range(1,11):
            threading_list.append(threading.Thread(target=self.thread_read_func,args=(((i-1)*30,i*30),)))
            threading_list[i-1].start()
        for i in range(1,11):
            threading_list[i-1].join()





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


if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode((Settings.M_WIDTH, Settings.M_HEIGHT))
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