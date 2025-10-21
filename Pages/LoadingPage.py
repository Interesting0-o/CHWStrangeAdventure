from Pages.Page import Page
import pygame
import threading
import main

class LoadingPage(Page):
    def __init__(self):
        super().__init__()
        self.loading_ball =None
        self.loading_ball_rect =[]

        #黑场初始化
        self.black_surface = pygame.surface.Surface((3840, 2160))
        self.black_surface.fill((0, 0, 0))
        self.black_surface_alpha = 0

    def init(self):
        """
        初始化
        :return:
        """
        self.display_surface = pygame.display.set_mode((self.window_width, self.window_height))

        #初始化加载动画主体
        self.loading_ball = pygame.surface.Surface((self.window_height*0.1, self.window_height*0.1))
        pygame.draw.circle(self.loading_ball,
                           "white",
                           (self.loading_ball.get_width() // 2,self.loading_ball.get_height() // 2),
                           self.loading_ball.get_width() // 2,
                           )
        #初始化加载动画位置
        for i in range(5):
            rect = self.loading_ball.get_rect(center = (self.window_width*0.2+self.window_width*0.1*(i+1), self.window_height//2))
            self.loading_ball_rect.append(rect)





    def reset(self):
        pass

    def draw(self):


        #渲染加载动画
        for rect in self.loading_ball_rect:

            self.display_surface.blit(self.loading_ball,rect)

    def handle_event(self, event):
        pass


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    screen.fill((255, 255, 255))

    loading_page = LoadingPage()
    loading_page.init()
    clock = pygame.time.Clock()

    while True:
        dt = clock.tick() / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            loading_page.handle_event(event)
        screen.fill("black")
        loading_page.draw()
        pygame.display.update()
