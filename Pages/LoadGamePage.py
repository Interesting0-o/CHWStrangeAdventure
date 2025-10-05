import pygame

from Pages.TextPage import TextPage
from ResourceLoader import ResourceLoader
from Elements.Button import Button
from Elements.MenuButton import MenuButton
from Pages.Page import Page
from SaveManager import SaveManager


class LoadGamePage(Page):
    def __init__(self):
        super().__init__()
        self.current_save_data_index = None
        self.load_save_done = False
        self.current_save_data = None
        self.load_text_start = False

        #存档资源

        self.current_page_text_rect = None
        self.current_page_text = None
        self.text_bg = None
        self.save_data = {}
        #黑场资源
        self.black_surface_alpha =0
        self.black_surface = None
        self.is_black_end = False

        #背景资源
        self.bg = ResourceLoader.big_ui
        self.bg_copy = None
        self.bg_rect = self.bg.get_rect()
        self.bg_alpha = 0
        self.bg.set_alpha(self.bg_alpha)
        self.bg_h = -60


        #关闭按钮初始化
        self.close_button = Button(ResourceLoader.close_button_animation[0])
        self.close_button.animation_list = ResourceLoader.close_button_animation
        self.close_button_value = False

        #翻页按钮初始化
        next_img = pygame.transform.scale(ResourceLoader.next, (70, 70))
        next_img_hover = pygame.transform.scale(ResourceLoader.next_hover, (70, 70))
        self.next_button =MenuButton(
            next_img,
            next_img_hover,
            next_img.get_rect()
        )
        last_img = pygame.transform.scale(ResourceLoader.last, (70, 70))
        last_img_hover = pygame.transform.scale(ResourceLoader.last_hover, (70, 70))
        self.last_button = MenuButton(
            last_img,
            last_img_hover,
            last_img.get_rect()
        )

        #初始化页数
        self.page_num = 1
        self.save_surfaces = []

        #弹出页面
        self.load_text_page = TextPage("是否载入存档")

    def save_load(self,save_data:dict):
        self.save_data.clear()
        self.save_data = save_data.copy()

    def init(self):

        self.load_text_page.init()
        self.display_surface =pygame.display.get_surface()

        #黑场初始化
        self.black_surface = pygame.Surface((3840,2160))
        self.black_surface.set_alpha(self.black_surface_alpha)

        #背景初始化
        self.display_surface = pygame.display.get_surface()

        #使用bg_copy作为背景
        self.bg_copy = pygame.transform.scale(self.bg, (self.window_width, self.window_height))
        self.bg_copy.set_alpha(self.bg_alpha)

        #关闭按钮重置

        self.close_button.rect = self.close_button.image.get_rect()
        self.close_button.rect.left = int(self.window_width * 0.86)
        self.close_button.rect.top = int(self.window_height * 0.07)
        self.bg_copy.blit(self.close_button.image, self.close_button.rect)

        #翻页按钮重置
        self.next_button.rect.center = (int(self.window_width * 0.88), int(self.window_height * 0.5))
        self.last_button.rect.center = (int(self.window_width * 0.12), int(self.window_height * 0.5))


        #存档视图渲染
        self.save_surfaces.clear()

        save_surface_bg =pygame.Surface((self.window_width*0.2,self.window_height*0.3))
        save_surface_bg.fill("green")
        save_surface_bg2 = pygame.Surface((self.window_width*0.2,self.window_height*0.3))
        save_surface_bg2.fill("#aaaaaa")


        num = (len(self.save_data) // 6 + 1) * 6
        keys = list(self.save_data.keys())
        for i in range(num):
            if i < len(self.save_data):
                if self.save_data[keys[i]] !="Error":
                    text = ResourceLoader.font_MiSans_Demibold24.render(keys[i][:-4],True,"white")
                    text_rect = text.get_rect(midbottom=(self.window_width*0.1,self.window_height*0.15))
                    temp = save_surface_bg.copy()
                    bg_copy_ = pygame.transform.scale(ResourceLoader.background[self.save_data[keys[i]] ["bg"]].copy(),
                                                      (self.window_width * 0.2, self.window_height * 0.3))
                    temp.blit(bg_copy_,(0,0))
                    temp.blit(text,text_rect)
                    temp.set_colorkey("green")
                    self.save_surfaces.append(MenuButton(
                        temp,
                        temp,
                        temp.get_rect(topleft = (self.window_width*0.20+(i%6)%3*self.window_width*0.21,
                                                 self.window_height*0.20 +(i%6)//3*self.window_height*0.32))
                    ))
                else:
                    text = ResourceLoader.font_MiSans_Demibold24.render(keys[i][:-4] +" Error", True, "white")
                    text_rect = text.get_rect(midbottom=(self.window_width*0.1, self.window_height * 0.15))
                    temp = save_surface_bg2.copy()
                    temp.blit(text, text_rect)
                    temp_hover = temp.copy()
                    self.save_surfaces.append(MenuButton(
                        temp,
                        temp_hover,
                        temp.get_rect(topleft = (self.window_width*0.20+(i%6)%3*self.window_width*0.21,
                                                 self.window_height*0.20 +(i%6)//3*self.window_height*0.32))
                    ))
            else:
                text = ResourceLoader.font_MiSans_Demibold24.render("Empty", True, "white")
                text_rect = text.get_rect(midbottom=(self.window_width*0.1, self.window_height * 0.15))
                temp = save_surface_bg2.copy()
                temp.blit(text, text_rect)
                temp_hover = temp.copy()
                self.save_surfaces.append(MenuButton(
                    temp,
                    temp_hover,
                    temp.get_rect(topleft = (self.window_width*0.20+(i%6)%3*self.window_width*0.21,
                                             self.window_height*0.20 +(i%6)//3*self.window_height*0.32))
                ))

        #当前页数
        self.current_page_text = ResourceLoader.font_loliti36.render("Page "+str(self.page_num), True, "black")
        self.current_page_text_rect = self.current_page_text.get_rect(midtop=(self.window_width*0.5,self.window_height*0.1))
        self.text_bg = pygame.surface.Surface(self.current_page_text_rect.size)
        self.text_bg.fill("white")

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.next_button.rect.collidepoint(event.pos):
                    if len(self.save_data)//6 +1 >self.page_num :
                        self.page_num += 1
                        self.current_page_text = ResourceLoader.font_loliti36.render("Page " + str(self.page_num), True,
                                                                                     "black")
                elif self.last_button.rect.collidepoint(event.pos):
                    if self.page_num > 1:
                        self.page_num -= 1
                        self.current_page_text = ResourceLoader.font_loliti36.render("Page " + str(self.page_num), True,
                                                                                     "black")
                for i in range((self.page_num - 1) * 6, self.page_num * 6):
                    if self.save_surfaces[i].rect.collidepoint(event.pos):
                        if i < len(self.save_data):
                            if self.save_data[list(self.save_data.keys())[i]] != "Error":
                                self.current_save_data_index = i
                                self.load_text_start = True
        #当再次询问界面启动
        if self.load_text_start:

            #弹出界面点击确定时
            if self.load_text_page.yes_button_value:
                self.current_save_data = self.save_data[list(self.save_data.keys())[self.current_save_data_index]]


    def draw(self):
        # 黑场进入
        if not self.close_button_value:
            if self.black_surface_alpha < 120:
                self.black_surface_alpha += 10
                self.black_surface.set_alpha(self.black_surface_alpha)
                self.bg_h += 5
                self.bg_alpha += 21
                self.bg_copy.set_alpha(self.bg_alpha)
        else:
            # 设置页面消失动画
            if self.black_surface_alpha > 0:
                self.black_surface_alpha -= 10
                self.black_surface.set_alpha(self.black_surface_alpha)
                self.bg_h -= 5
                self.bg_alpha -= 21
                self.bg_copy.set_alpha(self.bg_alpha)
                if self.bg_alpha <= 0:
                    self.is_end = True

        # 按钮渲染
        self.close_button.hover_animation_blit((0, 0))
        self.bg_copy.blit(self.close_button.image, self.close_button.rect)

        self.bg_copy.blit(self.next_button.img, self.next_button.rect)
        self.bg_copy.blit(self.last_button.img, self.last_button.rect)

        # 画面元素渲染
        self.display_surface.blit(self.black_surface, (0, 0))
        self.display_surface.blit(self.bg_copy, (0, self.bg_h))
        self.bg_copy.blit(self.text_bg, self.current_page_text_rect)
        self.bg_copy.blit(self.current_page_text, self.current_page_text_rect)

        # 存档视图渲染
        for i in range(( self.page_num - 1 ) * 6,self.page_num * 6):
            self.bg_copy.blit(self.save_surfaces[i].img, self.save_surfaces[i].rect)
            self.save_surfaces[i].hover_animation_blit((0, self.bg_h))


        #按钮事件处理
        if self.close_button.is_pressed_blit((0,self.bg_h)):
            self.close_button_value = True

        self.next_button.hover_animation_blit((0, self.bg_h))
        self.last_button.hover_animation_blit((0, self.bg_h))

        if self.load_text_start:
            self.load_text_page.draw()

        if self.load_text_page.is_end:
            self.load_text_page.is_end = False
            self.load_text_start = False
            self.load_text_page.no_button_value = False



if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    save_manager = SaveManager()
    save_manager.init_save_data()

    page = LoadGamePage()
    page.save_load(save_manager.save_datas)
    page.init()

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            page.handle_event(event)
        screen.fill("white")
        page.draw()
        pygame.display.update()
