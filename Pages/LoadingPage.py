import sys

import pygame
import math
from Pages.Page import Page
from ResourceLoader import ResourceLoader


class LoadingPage(Page):
    def __init__(self):
        super().__init__()
        #黑场资源初始化
        self.bg = pygame.Surface((3840, 2160))
        self.bg.fill("#ffcd72")

        #加载动画的小球
        self.loading_ball = pygame.surface.Surface((100, 100))
        pygame.draw.circle(self.loading_ball, "white", (50, 50), 50)
        self.loading_ball.set_colorkey("black")

        #小球状态
        self.ball_state = []

        for i in range(5):
            rect = self.loading_ball.get_rect()
            rect.center = (int(self.window_width*(0.2+(i+1)*0.1)), self.window_height//2)
            self.ball_state.append({
                "rect": rect,
                "start":False,
                "end":False,
                "run_time":0,
                "is_highest":False
            })

        #加载文字显示
        self.loading_text = []

        self.text_show_index = 0
        self.total_time = 0
        for i in range(6):
            text = ResourceLoader.font_loliti48.render("Loading"+i*".",True,(255,255,255))
            rect = text.get_rect()
            self.loading_text.append({
                "text":text,
                "rect":rect
            })


    def ball_reset(self):
        for i in range(5):
            self.ball_state[i]["start"] = False
            self.ball_state[i]["end"] = False
            self.ball_state[i]["run_time"] = 0
            self.ball_state[i]["is_highest"] = False
            self.ball_state[i]["rect"].centery = self.window_height//2


    def ball_move(self,d_t):
        """
        小球移动动画
        :param d_t:
        :return:
        """
        for i in range(5):
            if i==0 and self.ball_state[0]["end"]==False:

                #第一个球开始移动,判断最后一个球是否移动到中心
                if abs(self.ball_state[4]["rect"].centery-self.window_height//2)<1:#最后一个球移动到中心（误差控制）

                    self.ball_state[i]["run_time"] += d_t
                    self.ball_state[i]["run_time"]%=1
                    self.ball_state[i]["rect"].centery = 60 * math.sin(2*math.pi*self.ball_state[i]["run_time"] +math.pi/2) +self.window_height//2-60

                    #判断当前小球是否到达最高点
                    if abs(self.ball_state[i]["rect"].centery - self.window_height//2 +120)<1:
                        self.ball_state[i]["is_highest"] = True

                #是否经过一次完整的移动后运动到中心
                if self.ball_state[i]["is_highest"] and abs(self.ball_state[i]["rect"].centery - self.window_height//2)<0.1:#第一个球移动到中心
                    self.ball_state[i]["rect"].centery = self.window_height//2
                    self.ball_state[i]["end"] = True

            #判断上一个球是否到达中心
            elif abs(self.ball_state[i-1]["rect"].centery - self.window_height//2+60)<1:
                self.ball_state[i]["start"] = True
            if self.ball_state[i]["start"] and not self.ball_state[i]["end"]:

                self.ball_state[i]["run_time"] += d_t
                self.ball_state[i]["run_time"]%=1
                self.ball_state[i]["rect"].centery = 60 * math.sin(2*math.pi*self.ball_state[i]["run_time"] +math.pi/2) +self.window_height//2-60

                #判断当前小球是否到达最高点
                if abs(self.ball_state[i]["rect"].centery - self.window_height//2 +120)<1:
                    self.ball_state[i]["is_highest"] = True
            #判断是否经过一次完整的移动后运动到中心
            if self.ball_state[i]["is_highest"] and abs(
                    self.ball_state[i]["rect"].centery - self.window_height // 2) < 1:
                self.ball_state[i]["rect"].centery = self.window_height // 2
                self.ball_state[i]["end"] = True

        #判断所有球是否都结束了
        for i in range(5):
            if not self.ball_state[i]["end"]:
                break
        else:
            self.ball_reset()




    def init(self):
        self.display_surface = pygame.display.get_surface()

        #设置文字显示位置
        for i in range(6):
            self.loading_text[i]["rect"].center = (self.window_width//2,self.window_height*0.65)



    def reset(self):
        """

        :return:
        """
        self.is_end = False

        #初始化小球位置与状态
        for i in range(5):
            rect = self.loading_ball.get_rect()
            rect.center = (int(self.window_width*(0.2+(i+1)*0.1)), self.window_height//2)
            self.ball_state[i]["rect"] = rect
            self.ball_state[i]["start"] = False
            self.ball_state[i]["end"] = False
            self.ball_state[i]["run_time"] = 0

        #初始化文字显示
        self.text_show_index = 0
        self.total_time = 0

    def loading_text_show(self,d_t):
        """
        加载文字显示动画
        :param d_t:
        :return:
        """
        self.total_time += d_t
        if self.total_time>0.3:
            self.total_time = 0
            self.text_show_index += 1
            self.text_show_index %= 6

    def draw(self,d_t):
        """

        :param d_t:
        :return:
        """
        if not self.is_end:
            #背景渲染
            self.display_surface.blit(self.bg, (0, 0))

            #小球动画渲染
            self.ball_move(d_t)
            for i in range(5):
                self.display_surface.blit(self.loading_ball, self.ball_state[i]["rect"])

            #加载文字渲染
            self.loading_text_show(d_t)
            self.display_surface.blit(self.loading_text[self.text_show_index]["text"], self.loading_text[self.text_show_index]["rect"])


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((1280, 720))

    loading_page = LoadingPage()
    loading_page.init()

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        dt = clock.tick() / 1000.0
        screen.fill("#ffcd72")
        loading_page.draw(dt)
        pygame.display.update()