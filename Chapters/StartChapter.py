import pygame
from Chapters.Chapter import Chapter
from Elements.InputBox import InputBox
from Elements.MenuButton import MenuButton
from ResourceLoader import ResourceLoader
from Characters.Player import *

class StartChapter(Chapter):
    def __init__(self):
        super().__init__()

        self.input_box = None
        #背景图初始化
        self.bg = ResourceLoader.dialog_box
        self.bg_copy = self.bg
        self.bg_rect = None
        #按钮初始化
        text = "确定"
        #按钮图片(未选中时)初始化
        img = ResourceLoader.font_loliti36.render(text, True, "orange")
        img_rect = img.get_rect()
        img_bg = pygame.surface.Surface((img_rect.width + 80, img_rect.height + 10))
        img_bg.fill("green")
        pygame.draw.rect(img_bg,
                               "white",
                               (0, 0, img_bg.get_width(), img_bg.get_height()),
                               border_radius=10
                               )
        pygame.draw.rect(img_bg,
                               "orange",
                               (0, 0, img_bg.get_width(), img_bg.get_height()),
                               3,
                               border_radius=10
                               )
        img_rect.center = (img_bg.get_width()/2, img_bg.get_height()/2)
        img_bg.blit(img,img_rect)
        img_bg.set_colorkey("green")
        #按钮图片(选中时)初始化
        img_hover = ResourceLoader.font_loliti36.render(text, True, "white")
        img_hover_rect = img_hover.get_rect()
        img_hover_bg = pygame.surface.Surface((img_rect.width + 80, img_rect.height + 10))
        img_hover_bg.fill("green")
        pygame.draw.rect(img_hover_bg,
                               "#ffd68c",
                               (0, 0, img_hover_bg.get_width(), img_hover_bg.get_height()),
                               border_radius=10
                               )
        pygame.draw.rect(img_hover_bg,
                               "orange",
                               (0, 0, img_hover_bg.get_width(), img_hover_bg.get_height()),
                                5,
                               border_radius=10
                               )
        img_hover_rect.center = (img_hover_bg.get_width()/2, img_hover_bg.get_height()/2)
        img_hover_bg.blit(img_hover,img_hover_rect)
        img_hover_bg.set_colorkey("green")
        #按钮初始化
        self.mouse_down = False
        self.sure_button = MenuButton(
            img_bg,
            img_hover_bg,
            img_bg.get_rect(),
        )

    def init(self):
        self.display_surface = pygame.display.get_surface()
        #输入框初始化

        self.input_box = InputBox(
            location=(self.window_width/2 - 200, self.window_height/2 - 50 ),
            size=(400, 50),
            font=ResourceLoader.font_MiSans_Demibold24,
            max_length=15,
            text = "请输入您的称呼"
        )
        #背景图缩放
        self.bg = pygame.transform.scale_by(self.bg_copy,0.8)
        self.bg_rect = self.bg.get_rect()
        self.bg_rect.center = (int(self.window_width/2), int(self.window_height/2))
        #按钮位置
        self.sure_button.rect.center = (int(self.window_width/2), int(self.window_height/2 +60))

    def handle_event(self, event):
        self.input_box.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_down = True
        else:
            self.mouse_down = False

        # 按钮事件处理
        if self.sure_button.is_pressed_down(self.mouse_down):
            if self.input_box.text == "请输入您的称呼" or self.input_box.text == "请输入有效的称呼！" or self.input_box.text == "名称不可使用空白字符！":
                self.input_box.text = "请输入有效的称呼！"
            elif self.input_box.text == "":
                self.input_box.text = "名称不可使用空白字符！"
            else:
                player.name = self.input_box.text
                self.is_end = True

    def reset(self):
        """
        重置本章节
        :return:
        """
        self.is_end = False
        self.input_box.text = ""


    def show(self,player:Player):
        if not self.is_end:
            #背景显示
            self.display_surface.fill("black")
            self.display_surface.blit(self.bg, self.bg_rect)
            self.input_box.draw(self.display_surface)
            #按钮显示
            self.sure_button.hover_animation()
            self.display_surface.blit(self.sure_button.img, self.sure_button.rect)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))

    #初始化
    start_chapter = StartChapter()
    start_chapter.init()

    player = Player()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                start_chapter.reset()

            start_chapter.handle_event(event)


        start_chapter.show(player)
        pygame.display.update()
