import pygame

from Elements import MenuButton
from Pages.Page import Page
from Elements.Slider import Slider
from ResourceLoader import ResourceLoader

pygame.mixer.init()
pygame.font.init()

class VoiceSetting(Page):
    def __init__(self,
                 auto_bgm_volume:float,
                 auto_character_volume:float ,
                 auto_effect_volume:float,
                 ):
        """
        初始化
        :param auto_bgm_volume:
        :param auto_character_volume:
        :param auto_effect_volume:
        """
        super().__init__()
        self.location = None


        self.auto_bgm_volume = auto_bgm_volume
        self.auto_char_volume = auto_character_volume
        self.auto_effect_volume = auto_effect_volume

        self.bg_surface_rect = None
        self.isSettingsChange = False

        self.bg_surface = None

        self.font = ResourceLoader.font_dict["MiSansDemibold36"]

        self._save_button_define_()

    def _test_define_(self):
        """
        定义文本
        :return:
        """

        # 背景音乐大小
        self.bgm_text = ResourceLoader.font_dict["MiSansDemibold24"].render("背景音乐大小:", True, "black")
        self.bgm_text_rect = self.bgm_text.get_rect(center = (self.window_width*0.2*0.6,self.window_height*0.15*0.64))

        # 角色音效大小
        self.char_text = ResourceLoader.font_dict["MiSansDemibold24"].render("角色音效大小:", True, "black")
        self.char_text_rect = self.char_text.get_rect(center = (self.window_width*0.2*0.6,self.window_height*0.15*0.64 + 50))

        # 其他音效大小
        self.effect_text = ResourceLoader.font_dict["MiSansDemibold24"].render("其他音效大小:", True, "black")
        self.effect_text_rect = self.effect_text.get_rect(center = (self.window_width*0.2*0.6,self.window_height*0.15*0.64 + 100))

    def _draw_text_(self):
        """
        绘制文本
        :return:
        """
        self.bg_surface.blit(self.bgm_text, self.bgm_text_rect)
        self.bg_surface.blit(self.char_text, self.char_text_rect)
        self.bg_surface.blit(self.effect_text, self.effect_text_rect)

    def _slider_define_(self):
        self.bgm_slider = Slider(
            x =self.window_width*0.7*0.6, y = self.window_height*0.15*0.64,
            length = 300, height = 25,
            ball_color="white",
            track_color="orange",
            border_color="#dddddd",
            location = self.location,
            max_val= 1.0,
            min_val=0.0,
            initial_val=self.auto_bgm_volume,
        )
        self.char_slider = Slider(
            x =self.window_width*0.7*0.6, y = self.window_height*0.15*0.64 + 50,
            length = 300, height = 25,
            ball_color="white",
            track_color="orange",
            border_color="#dddddd",
            location = self.location,
            max_val= 1.0,
            min_val=0.0,
            initial_val=self.auto_char_volume,
        )

        self.effect_slider = Slider(
            x =self.window_width*0.7*0.6, y = self.window_height*0.15*0.64 + 100,
            length = 300, height = 25,
            ball_color="white",
            track_color="orange",
            border_color="#dddddd",
            location = self.location,
            max_val= 1.0,
            min_val=0.0,
            initial_val=self.auto_effect_volume,
        )
    def _draw_slider_(self):
        """
        绘制滑动条
        :return:
        """
        self.bgm_slider.draw(self.bg_surface)
        self.char_slider.draw(self.bg_surface)
        self.effect_slider.draw(self.bg_surface)


    def _draw_value_text_(self):
        """
        绘制当前值文本框
        :return:
        """
        self.bg_surface.blit(ResourceLoader.font_dict["MiSansDemibold24"].render(f"{100*self.bgm_slider.value:.0f}", True, "black"),
                             (self.window_width*0.7*0.6 + 160,  self.window_height*0.15*0.64 - 15)
                             )
        self.bg_surface.blit(ResourceLoader.font_dict["MiSansDemibold24"].render(f"{100*self.char_slider.value:.0f}", True, "black"),
                             (self.window_width*0.7*0.6 + 160,  self.window_height*0.15*0.64 + 50 - 15)
                             )
        self.bg_surface.blit(ResourceLoader.font_dict["MiSansDemibold24"].render(f"{100*self.effect_slider.value:.0f}", True, "black"),
                             (self.window_width*0.7*0.6 + 160,  self.window_height*0.15*0.64 + 100 - 15)
                             )

    def _slider_event_(self, event:pygame.event.Event):
        """
        处理滑动条事件
        :param event:
        :return:
        """
        self.bgm_slider.handle_event(event)
        self.char_slider.handle_event(event)
        self.effect_slider.handle_event(event)



    def _save_button_define_(self):
        #设置保存按钮
        self.save_button_bg = pygame.Surface((210,35)) #未选中状态
        self.save_button_bg.fill("white")
        self.save_text = ResourceLoader.font_dict["MiSansDemibold36"].render("保存当前设置", True, "#FFA500")
        self.save_button_bg.blit(self.save_text,
                                 self.save_text.get_rect(center = self.save_button_bg.get_rect().center))
        self.save_button_hover_bg = pygame.Surface((210,35)) #鼠标悬停状态
        self.save_button_hover_bg.fill("#FFA500")
        self.save_text_hover = ResourceLoader.font_dict["MiSansDemibold36"].render("保存当前设置", True, "white")
        self.save_button_hover_bg.blit(self.save_text_hover,
                                        self.save_text_hover.get_rect(center = self.save_button_hover_bg.get_rect().center))
        self.save_button = MenuButton(#实例化按钮
            self.save_button_bg,
            self.save_button_hover_bg,
            self.save_button_bg.get_rect(center = (self.window_width*0.5*0.6,self.window_height*0.8*0.8))
        )

    def get_volume(self)->tuple[float,float,float]:
        """
        返回当前音频的音量
        :return:
        """
        return self.bgm_slider.get_value(), self.char_slider.get_value(), self.effect_slider.get_value()

    def is_setting_change(self):
        return self.isSettingsChange

    def reset(self):
        self.is_end = False


    def init(self,
            location:tuple[int,int] = (0,0)    #bg_surface位置
             ):

        self.location = location
        self.bg_surface = pygame.surface.Surface((self.window_width * 0.6, self.window_height * 0.64))
        self.bg_surface.fill((255, 255, 255))
        self.bg_surface_rect = self.bg_surface.get_rect(topleft = location)


        #保存设置按钮初始化
        self.save_button.rect.center = (self.window_width*0.5*0.6,self.window_height*0.9*0.64)

        #定义滑动条
        self._slider_define_()

        # 定义文本
        self._test_define_()




    def handle_event(self, event):
        if self.is_end:
            return

        self._slider_event_(event)
        #保存设置按钮事件
        #保存修改
        if self.save_button.is_press(self.bg_surface_rect.topleft):
            self.isSettingsChange = True
        else:
            self.isSettingsChange = False


    def draw(self,
             location:tuple[int,int] = (0,0)#bg_surface位置
             ):
        if self.is_end:
            return

        self.bg_surface.fill((255, 255, 255))

        #保存设置按钮
        self.save_button.hover_animation(self.location)
        self.bg_surface.blit(self.save_button.img, self.save_button.rect)

        #滑动条渲染

        self._draw_slider_()

        #文本渲染
        self._draw_text_()

        #当前值文本框渲染
        self._draw_value_text_()

def test():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()


    load = ResourceLoader()
    load.load_all_resource()
    load.wait_load_finish()



    voice_setting = VoiceSetting(0.5,0.5,0.5)
    voice_setting.init((200, 200))


    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            voice_setting.handle_event(event)

        screen.fill((0, 0, 0))

        voice_setting.draw()
        screen.blit(voice_setting.bg_surface, (200, 200))

        pygame.display.update()

if __name__ == '__main__':
    test()