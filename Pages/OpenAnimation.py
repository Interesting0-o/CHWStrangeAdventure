from Pages.Page import Page
from ResourceLoader import ResourceLoader

import pygame
import numpy as np
import cv2


class OpenAnimation(Page):

    def __init__(self):
        super().__init__()

        #视频对象

        self.cap = None
        #视频路径
        self.video_path = Page.path[:-6] + r"\resource\video\title.mp4"
        #视频的总帧数
        self.total_frame = 300

        #提示文本
        self.test = pygame.font.Font(ResourceLoader.font_resource_path["MiSansDemibold"], 36).render("请按任意键继续", True, "white")
        self.test_rect = self.test.get_rect(center=(Page.window_width/2, Page.window_height*0.9))

        #黑场退出
        self.black_surface = pygame.Surface((3840, 2160))
        self.black_surface.fill((0, 0, 0))
        self.black_alpha = 0
        self.is_black = False


    def reset(self):
        """
        重置动画
        :return:
        """
        self.is_end = True

        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            raise FileNotFoundError("打不开视频，请检查路径")

        #黑场内容重置
        self.is_black = False
        self.black_alpha = 0

    def init(self):
        """
        初始化动画
        :return:
        """
        #缩放动画图片
        self.display_surface = pygame.display.get_surface()

        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            raise FileNotFoundError("打不开视频，请检查路径")



    def handle_event(self, event):
        """
        处理事件
        :param event:
        :return:
        """
        if self.is_end:
            return

        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.is_black = True


    def draw(self):
        """
        绘制动画
        :return:
        """
        if self.is_end:
            return

        ret, frame_bgr = self.cap.read()

        try:
            # 关键：把帧直接缩放到窗口大小
            frame_bgr = cv2.resize(frame_bgr,(Page.window_width, Page.window_height))
        except cv2.error:
            self.is_end = True
            return

        # BGR → RGB → 转 Pygame Surface
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        # OpenCV 的帧是 (height, width, 3)，而 Pygame 的 Surface 要求 (width, height, 3)
        # 先转置轴顺序。去掉额外的垂直翻转以避免图像倒置。
        frame_rgb = np.transpose(frame_rgb, (1, 0, 2))
        frame_surface = pygame.surfarray.make_surface(frame_rgb)

        # 显示
        self.display_surface.blit(frame_surface, (0, 0))

        # 显示提示文本
        self.display_surface.blit(self.test, self.test_rect)

        # 黑场退出
        if self.is_black:
            self.black_alpha += 10
            if self.black_alpha >= 255:
                self.is_end = True
            self.black_surface.set_alpha(self.black_alpha)
            self.display_surface.blit(self.black_surface, (0, 0))




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
            open_animation.handle_event(event)

        open_animation.draw()
        pygame.display.update()

        if open_animation.is_end:
            print("结束")
        print(clock.get_fps())

if __name__ == '__main__':
    test()

