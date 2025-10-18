import pygame

from Pages.TextPage import TextPage
from ResourceLoader import ResourceLoader
from Elements.Button import Button
from Elements.MenuButton import MenuButton
from Pages.Page import Page
from SaveManager import SaveManager


class LoadGamePage(Page):
    def __init__(self):
        """
        初始化页面
        """
        super().__init__()
        #存档删除
        self.save_is_delete = False
        self.delete_save_index = None

        self.current_save_name = None
        self.current_save_data_index = None
        self.current_save_data = None


        #询问页面
        self.load_text_start = False
        self.delete_text_start = False

        self.load_save_done = False
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

        #删除按钮初始化
        delete = pygame.transform.scale(ResourceLoader.delete, (48, 64))
        delete_hover = pygame.transform.scale(ResourceLoader.delete_hover, (48, 64))
        self.delete_button_list = [MenuButton(
            delete.copy(),
            delete_hover.copy(),
            delete.get_rect()
        ) for i in range(6) ]


        #初始化页数
        self.page_num = 1
        self.save_surfaces = []

        #弹出页面
        self.load_text_page = TextPage("是否载入存档") #判断是否载入存档页面
        self.delete_text_page = TextPage("是否删除存档") #判断删除存档页面



    def save_load(self,save_data:dict):
        """
        读取存档数据
        :param save_data:
        :return:
        """
        self.save_data.clear()
        self.save_data = save_data.copy()


    def reset(self):
        """
        `Page`类的重置方法，重置页面状态
        :return:
        """
        self.is_end = False
        #黑场重置
        self.black_surface_alpha = 0

        #背景重置
        self.bg_alpha = 0
        self.bg.set_alpha(self.bg_alpha)
        self.bg_h = -60

        #关闭按钮重置
        self.close_button_value = False

        #重置询问页面
        self.load_text_page.reset()
        self.load_text_start = False

        self.delete_text_page.reset()
        self.delete_text_start = False



    def init(self):
        """
        初始化页面
        :return:
        """

        #询问页面初始化
        self.load_text_page.init()
        self.delete_text_page.init()

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


        #删除按钮初始化
        for i in range(6):
            self.delete_button_list[i].rect.topleft = (
                self.window_width * 0.20 + i % 3 * self.window_width * 0.21,
                self.window_height * 0.20 + i // 3 * self.window_height * 0.32)

        #存档按钮初始化
        self.redraw_save()

        #当前页数
        self.current_page_text = ResourceLoader.font_loliti36.render("Page "+str(self.page_num), True, "black")
        self.current_page_text_rect = self.current_page_text.get_rect(midtop=(self.window_width*0.5,self.window_height*0.1))
        self.text_bg = pygame.surface.Surface(self.current_page_text_rect.size)
        self.text_bg.fill("white")

    def handle_event(self, event):
        """
        处理事件
        :param event:
        :return:
        """

        #处理存档删除事件
        if self.save_is_delete:
            self.delete_save()
            self.redraw_save()
            self.save_is_delete = False
            self.delete_text_page.reset()
            self.delete_text_start = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                #下一页按钮事件
                if self.next_button.rect.collidepoint(event.pos):
                    if len(self.save_data)//6 +1 >self.page_num :
                        self.page_num += 1
                        self.current_page_text = ResourceLoader.font_loliti36.render("Page " + str(self.page_num), True,
                                                                                     "black")

                #上一页按钮事件
                elif self.last_button.rect.collidepoint(event.pos):
                    if self.page_num > 1:
                        self.page_num -= 1
                        self.current_page_text = ResourceLoader.font_loliti36.render("Page " + str(self.page_num), True,
                                                                                     "black")

                #关闭按钮事件
                is_delete_hover = False
                for i in range(6):
                    if self.delete_button_list[i].rect.collidepoint(event.pos):
                        if self.page_num * 6 - 6 + i < len(self.save_data):
                            is_delete_hover = True
                            self.delete_save_index = self.page_num * 6 - 6 + i
                            self.delete_text_start = True

                if not is_delete_hover:
                    #存档按钮事件
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
                self.current_save_name = list(self.save_data.keys())[self.current_save_data_index]
        #删除存档询问界面启动
        if self.delete_text_start:
            if self.delete_text_page.yes_button_value:
                self.save_is_delete =True

    def redraw_save(self):

        num = (len(self.save_data) // 6 + 1) * 6
        keys = list(self.save_data.keys())#存档名列表

        self.save_surfaces.clear()

        save_surface_bg = pygame.Surface((self.window_width * 0.2, self.window_height * 0.3))
        save_surface_bg.fill("green")
        save_surface_bg2 = pygame.Surface((self.window_width * 0.2, self.window_height * 0.3))
        save_surface_bg2.fill("#aaaaaa")

        # 存档按钮渲染
        for i in range(num):
            if i < len(self.save_data):
                # 判断存档是否损坏
                try:
                    if self.save_data[keys[i]] != "Error":
                        text = ResourceLoader.font_MiSans_Demibold24.render(keys[i][:-4], True, "white")
                        text_rect = text.get_rect(midbottom=(self.window_width * 0.1, self.window_height * 0.15))
                        temp = save_surface_bg.copy()
                        bg_copy_ = pygame.transform.scale(
                            ResourceLoader.background[self.save_data[keys[i]]["bg"]].copy(),
                            (self.window_width * 0.2, self.window_height * 0.3))

                        temp.blit(bg_copy_, (0, 0))
                        temp.blit(text, text_rect)
                        temp.set_colorkey("green")
                        self.save_surfaces.append(MenuButton(
                            temp,
                            temp,
                            temp.get_rect(topleft=(self.window_width * 0.20 + (i % 6) % 3 * self.window_width * 0.21,
                                                   self.window_height * 0.20 + (
                                                               i % 6) // 3 * self.window_height * 0.32))
                        ))

                except Exception as e:
                    self.save_data[keys[i]] = "Error"
                    print(e)

                if self.save_data[keys[i]] == "Error":
                    text = ResourceLoader.font_MiSans_Demibold24.render(keys[i][:-4] + " Error", True, "white")
                    text_rect = text.get_rect(midbottom=(self.window_width * 0.1, self.window_height * 0.15))
                    temp = save_surface_bg2.copy()
                    temp.blit(text, text_rect)
                    temp_hover = temp.copy()
                    self.save_surfaces.append(MenuButton(
                        temp,
                        temp_hover,
                        temp.get_rect(topleft=(self.window_width * 0.20 + (i % 6) % 3 * self.window_width * 0.21,
                                               self.window_height * 0.20 + (i % 6) // 3 * self.window_height * 0.32))
                    ))
            else:
                text = ResourceLoader.font_MiSans_Demibold24.render("Empty", True, "white")
                text_rect = text.get_rect(midbottom=(self.window_width * 0.1, self.window_height * 0.15))
                temp = save_surface_bg2.copy()
                temp.blit(text, text_rect)
                temp_hover = temp.copy()
                self.save_surfaces.append(MenuButton(
                    temp,
                    temp_hover,
                    temp.get_rect(topleft=(self.window_width * 0.20 + (i % 6) % 3 * self.window_width * 0.21,
                                           self.window_height * 0.20 + (i % 6) // 3 * self.window_height * 0.32))
                ))

    def delete_save(self):
        if self.save_is_delete:
            key = list(self.save_data.keys())[self.delete_save_index]
            self.save_data.pop(key)
            return key
        else:
            return None

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

            #删除按钮渲染
            self.bg_copy.blit(self.delete_button_list[i].img, self.delete_button_list[i].rect)
            self.delete_button_list[i].hover_animation_blit((0, self.bg_h))


        #按钮事件处理
        if self.close_button.is_pressed_blit((0,self.bg_h)):
            self.close_button_value = True

        self.next_button.hover_animation_blit((0, self.bg_h))
        self.last_button.hover_animation_blit((0, self.bg_h))
        #存档弹窗渲染
        if self.load_text_start:
            self.load_text_page.draw()

        if self.load_text_page.is_end:
            self.load_text_page.is_end = False
            self.load_text_start = False
            self.load_text_page.no_button_value = False
        #删除弹窗渲染
        if self.delete_text_start:
            self.delete_text_page.draw()

        if self.delete_text_page.is_end:
            self.delete_text_page.is_end = False
            self.delete_text_start = False
            self.delete_text_page.no_button_value = False



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
        keys =   pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            page.reset()
        screen.fill("white")
        page.draw()
        print(page.delete_save())
        pygame.display.update()
