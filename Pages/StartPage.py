import pygame
from settings import Settings
from Pages.Page import Page
from Elements.Button import Button
from ResourceLoader import ResourceLoader

class StartPage(Page):
    def __init__(self):
        super().__init__()
        #创建背景图片和标题

        self.bg_image = ResourceLoader.start_bg.convert()
        self.bg_rect = self.bg_image.get_rect()
        self.title =ResourceLoader.title_bg.convert_alpha()
        self.title_rect = self.title.get_rect()
        self.bg_image_copy = self.bg_image.copy()
        self.title_copy = self.title.copy()


        self.dt = pygame.time.Clock().tick(Settings.FPS)
        #按钮初始化
        self.start_button = None
        self.load_button = None
        self.quit_button = None
        self.settings_button = None
        self.button_group = pygame.sprite.Group()
        #版本信息显示
        self.font_1 = ResourceLoader.font_loliti24
        self.version =self.font_1.render("游戏版本："+Settings.GAME_VERSION,True,(0,0,0))
        self.version_rect = self.version.get_rect()
        
        #按钮背景初始化
        self.buttons_bg = pygame.Surface((240,350))
        self.buttons_bg_rect = None

        #按钮初始化
        if True:
            self.start_button =Button(ResourceLoader.start_button_animation[0])
            self.load_button = Button(ResourceLoader.load_button_animation[0])
            self.quit_button = Button(ResourceLoader.quit_button_animation[0])
            self.settings_button = Button(ResourceLoader.settings_button_animation[0])

            # 载入Button动画
            self.start_button.animation_list = ResourceLoader.start_button_animation
            self.load_button.animation_list = ResourceLoader.load_button_animation
            self.quit_button.animation_list = ResourceLoader.quit_button_animation
            self.settings_button.animation_list = ResourceLoader.settings_button_animation

            self.button_group.add(
                self.start_button,
                self.load_button,
                self.settings_button,
                self.quit_button,
            )

    def init(self):
        self.display_surface = pygame.display.get_surface()
        #版本资源
        self.version_rect.bottomleft=(10,self.window_height-20)
        #实例化按钮
        self.start_button.rect.center = (self.window_width * 0.5, self.window_height * 0.6)
        self.load_button.rect.center = (self.window_width * 0.5, self.window_height * 0.6+70)
        self.quit_button.rect.center = (self.window_width * 0.5, self.window_height * 0.6+210)
        self.settings_button.rect.center = (self.window_width * 0.5, self.window_height * 0.6+140)

        #按钮选项框绘制
        self.buttons_bg_rect = self.buttons_bg.get_rect(center = (
            self.window_width * 0.5,
            self.window_height * 0.6+105
        ))
        pygame.draw.rect(self.buttons_bg,"white",(0,0,240,350),border_radius=20)
        self.buttons_bg.set_colorkey("#000000")
        self.buttons_bg.set_alpha(128)
        self.title_rect.center = (int(self.window_width /2), int(self.window_height * 0.13))
        #判断背景图片是否需要缩放
        if self.bg_rect.size != self.display_surface.get_size():
            self.bg_image = pygame.transform.scale(self.bg_image_copy, self.display_surface.get_size())
            self.bg_rect = self.bg_image.get_rect()
        #判断标题图片是否需要缩放
        if self.title.get_size()[0] != self.display_surface.get_size()[0]*0.4 or self.title.get_size()[1] != self.display_surface.get_size()[1]*0.4:
            self.title = pygame.transform.scale(self.title_copy,
                                                   (int(self.display_surface.get_size()[0]*0.4),
                                                   int(self.display_surface.get_size()[1]*0.4)
                                                   ))
            self.title_rect = self.title.get_rect(center=(
                self.display_surface.get_size()[0]//2,
                self.display_surface.get_size()[1]*0.3
            ))


    def reset(self):
        self.is_end = False
        #按钮初始化
        self.start_button.image = ResourceLoader.start_button_animation[0]
        self.start_button.index = 0
        self.load_button.image= ResourceLoader.load_button_animation[0]
        self.load_button.index = 0
        self.quit_button.image = ResourceLoader.quit_button_animation[0]
        self.quit_button.index = 0
        self.settings_button.image = ResourceLoader.settings_button_animation[0]
        self.settings_button.index = 0


    def draw(self):
        self.display_surface.blit(self.bg_image, self.bg_rect)
        self.display_surface.blit(self.buttons_bg,self.buttons_bg_rect)
        self.button_group.draw(self.display_surface)


        if not self.is_end:
            self.start_button.hover_animation()
            self.load_button.hover_animation()
            self.settings_button.hover_animation()
            self.quit_button.hover_animation()

        self.display_surface.blit(self.title, self.title_rect)
        self.display_surface.blit(self.version,self.version_rect)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption('StartPage', "StartPage")
    clock = pygame.time.Clock()
    start_page = StartPage()
    start_page.init()
    while True:
        clock.tick(Settings.FPS)
        x,y = pygame.mouse.get_pos()
        mouses = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        start_page.draw()

        if __name__ == "__main__":
            if start_page.start_button.is_pressed():
                print("click start button")
            if start_page.load_button.is_pressed():
                print("click load button")
            if start_page.settings_button.is_pressed():
                print("click Settings button")
            if start_page.quit_button.is_pressed():
                print("click quit button")
        pygame.display.update()

