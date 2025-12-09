import pygame

from Elements import MenuButton
from Voice import Voice
from settings import Settings
from Pages.Page import Page
from Elements.Slider import Slider
from ResourceLoader import ResourceLoader

pygame.mixer.init()
pygame.font.init()

class VoiceSetting(Page):
    def __init__(self,location:tuple[int,int] = (0,0)):
        """
        初始化声音设置页面
        :param location:
        """
        super().__init__()
        self.location = location

        self.bg_surface_rect = None
        self.isSettingChanged = False

        self.bg_surface = None


        self.char_channel = Voice.char_channel
        self.effect_channel = Voice.effect_channel

        self.font = ResourceLoader.font_dict["MiSansDemibold36"]

        self._save_button_define_()
        self._slider_define_()


    def _slider_define_(self):
        self.bgm_slider = Slider(
            x =200, y = 200,
            length = 300, height = 30,
            ball_color="white",
            track_color="orange",
            border_color="#dddddd",
            location = self.location
        )
        self.char_slider = Slider(
            x =200, y = 300,
            length = 300, height = 30,
            ball_color="white",
            track_color="orange",
            border_color="#dddddd",
            location = self.location
        )
        self.effect_slider = Slider(
            x =200, y = 400,
            length = 300, height = 30,
            ball_color="white",
            track_color="orange",
            border_color="#dddddd",
            location = self.location
        )
    def _draw_slider_(self):
        """
        绘制滑动条
        :return:
        """
        self.bgm_slider.draw(self.bg_surface)
        self.char_slider.draw(self.bg_surface)
        self.effect_slider.draw(self.bg_surface)


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

    def is_setting_changed(self):
        return self.isSettingChanged

    def reset(self):
        self.is_end = False

    def init(self,
            location:tuple[int,int] = (0,0)    #bg_surface位置
             ):


        self.bg_surface = pygame.surface.Surface((self.window_width * 0.6, self.window_height * 0.64))
        self.bg_surface.fill((255, 255, 255))
        self.bg_surface_rect = self.bg_surface.get_rect(topleft = location)


        #保存设置按钮初始化
        self.save_button.rect.center = (self.window_width*0.5*0.6,self.window_height*0.9*0.64)



    def handle_event(self, event):
        if self.is_end:
            return

        self._slider_event_(event)


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

def test():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()


    load = ResourceLoader()
    load.load_all_resource()
    load.wait_load_finish()



    voice_setting = VoiceSetting((200, 200))
    voice_setting.init()


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