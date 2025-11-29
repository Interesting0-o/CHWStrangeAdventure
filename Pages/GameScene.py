import os
import pygame
import json
from Pages.Page import Page
from ResourceLoader import ResourceLoader
from settings import Settings
from Elements.MenuButton import MenuButton
from Characters import *


class GameScene(Page):
    def __init__(self):
        super().__init__()

        #保存
        self.save_saves = False
        #按钮类

        self.voice_button = None
        self.back_button = None
        self.save_button = None

        #场景记录

        self.is_button_on = False
        self.current_player_honor = 0
        self.current_chapter = None
        self.scene_record = []
        #玩家类
        self.current_player = None

        self.is_choosing = False
        self.is_chapter_end = False

        #存档数据
        self.save_data = None
        self.config = None
        self.current_scene = None
        self.dialog_index = None

        # 选项框内容
        self.choice_bg = None
        self.choice_hover_bg = None
        self.choice_box= []

        # 背景图
        self.current_bg = None
        self.current_bg_alpha = 0
        self.current_bg_copy = None

        #对话框
        self.dialog_bg = ResourceLoader.bg_dict["DialogBG"]
        self.dialog_scale = None
        self.dialog_bg_copy = None

        #事件设置
        self.next_text_event = False

        #黑场
        self.black_bg = pygame.surface.Surface((3840, 2160))
        self.black_bg.fill("black")
        self.black_bg.set_alpha(128)

        #角色组
        self.character_group = None

        #选项条件重载
        self.is_choice_reloads = True

        #音频资源
        self.is_voice_on = True
        self.current_voice = None
        self.is_voice = False

        #剧情文件管理
        self.json_file = []


    def reset(self):
        #保存
        self.save_saves = False
        #场景记录

        self.is_button_on = False
        self.current_chapter = None
        self.scene_record = []

        #玩家内容
        self.current_player = None

        self.is_choosing = False
        self.is_chapter_end = False

        #存档数据
        self.save_data = None
        self.config = None
        self.current_scene = None
        self.dialog_index = None

        # 选项框内容
        self.choice_box.clear()

        #事件设置
        self.next_text_event = False

        #角色组
        self.character_group = None

        #选项条件重载
        self.is_choice_reloads = True

        #音频资源
        self.is_voice_on = True
        self.current_voice = None
        self.is_voice = False


    def to_dict(self):
        return {
            "player":{
                "name" :self.current_player,
                "honor_value":self.current_player_honor,
            },
            "chapter_data":{
                "chapter":self.current_chapter,
                "scene":self.current_scene,
                "dialog_index":self.dialog_index,
            },
            "bg":self.config[self.current_scene]['bg']
        }

    def read_save(self,
        save_data,  # 存档数据
        character_group: CharacterGroup,  # 角色组
                    ):
        #玩家引用
        self.current_player = save_data["player"]["name"]
        self.current_player_honor = save_data["player"]["honor_value"]
        #存档数据
        self.save_data = save_data
        self.current_scene = save_data["chapter_data"]["scene"]
        self.scene_record.append(self.current_scene)
        self.dialog_index = save_data["chapter_data"]["dialog_index"]
        #角色组
        self.character_group = character_group
        self.current_chapter = save_data["chapter_data"]["chapter"]

    def get_chapter_data(self):
        return self.save_data["chapter_data"]["chapter"]

    def init(self):

        self.display_surface = pygame.display.get_surface()
        # 选项框初始化
        self.choice_bg = pygame.surface.Surface((self.window_width*0.6, self.window_height*0.10))
        self.choice_bg.fill("green")
        #未选中时的选项框添加边框
        pygame.draw.rect(
            self.choice_bg,
            "white",
            (0, 0, self.window_width*0.6, self.window_height*0.10),
            border_radius= int(self.window_height*0.06),
        )
        pygame.draw.rect(
            self.choice_bg,
            "orange",
            (0, 0, self.window_width*0.6, self.window_height*0.10),
            border_radius= int(self.window_height*0.06),
            width=5,
        )
        self.choice_bg.set_colorkey("green")
        #选中时的选项框添加边框
        self.choice_hover_bg = pygame.surface.Surface((self.window_width*0.6, self.window_height*0.10))
        self.choice_hover_bg.fill("green")
        pygame.draw.rect(
            self.choice_hover_bg,
            "#ffd68c",
            (0, 0, self.window_width*0.6, self.window_height*0.10),
            border_radius= int(self.window_height*0.06),
        )
        pygame.draw.rect(
            self.choice_hover_bg,
            "orange",
            (0, 0, self.window_width*0.6, self.window_height*0.10),
            border_radius= int(self.window_height*0.06),
            width=5,
        )
        self.choice_hover_bg.set_colorkey("green")

        self.current_bg = ResourceLoader.background[self.config[self.current_scene]['bg']]
        self.current_bg_copy = self.current_bg.copy()
        self.current_bg = pygame.transform.scale(self.current_bg_copy, (self.window_width, self.window_height))


        #对话框处理
        self.dialog_scale = pygame.transform.scale(self.dialog_bg, (self.window_width, self.window_height))

        #按钮处理
        self.is_button_on = False


        #音频重播按钮
        voice = ResourceLoader.voice
        voice = pygame.transform.scale(voice, (50, 50))
        voice_bg_hover = ResourceLoader.voice_hover
        voice_bg_hover = pygame.transform.scale(voice_bg_hover, (50, 50))

        self.voice_button = MenuButton(
            voice,
            voice_bg_hover,
            voice.get_rect(center=(self.window_width*0.9,self.window_height*0.92))
        )

        #回退按钮
        back = ResourceLoader.back
        back = pygame.transform.scale(back, (50, 50))
        back_bg_hover = ResourceLoader.back_hover
        back_bg_hover = pygame.transform.scale(back_bg_hover, (50, 50))
        self.back_button = MenuButton(
            back,
            back_bg_hover,
            back.get_rect(center=(self.window_width*0.9 -50,self.window_height*0.92))
        )
        #保存按钮
        save = ResourceLoader.save
        save = pygame.transform.scale(save, (50, 50))
        save_bg_hover = ResourceLoader.save_hover
        save_bg_hover = pygame.transform.scale(save_bg_hover, (50, 50))
        self.save_button = MenuButton(
            save,
            save_bg_hover,
            save.get_rect(center=(self.window_width*0.9 +50,self.window_height*0.92))
        )

    def handle_event(self, event):
        pass


    def draw(self):
        #背景渲染
        self.display_surface.blit(self.current_bg, (0, 0))

        #判断是否结束
        if not self.is_chapter_end:
            self.dialog_bg_copy = self.dialog_scale.copy()


            # 选项条件预渲染
            if self.is_choice_reloads and self.get_current_dialog()["type"] == "choice":
                self.is_choice_reloads = False
                self._prepare_button()



            #判断当前对话片段是否结束
            if self.dialog_index > len(self.config[self.current_scene]["dialogues"]) - 1:
                self.current_scene = self.config[self.current_scene]["next_scene"]
                self.scene_record.append(self.current_scene)
                self.dialog_index = 0
                if self.current_scene not in self.config:
                    self.is_chapter_end = True

            #判断当前对话框类型是否为dialogue
            elif self.get_current_dialog()["type"]=="dialogue" :

                #获取当前对话角色数据人物贴图
                self._draw_character()
                #人物名字渲染
                self._draw_name()
                # 处理文字对话
                self._draw_text()
                # 对话框渲染
                self.display_surface.blit(self.dialog_bg_copy, (0, 0))

            # 当当前对话框类型为choice时，显示选项框
            elif self.get_current_dialog()["type"]=="choice":
                #将黑场显示出来
                self.display_surface.blit(self.black_bg, (0, 0))
                #渲染选项
                self._draw_choice_box()


        # 按钮渲染
        self._draw_button()


    def chapter_read(self):
        pass






    def get_current_dialog(self):
        """
        获取当前对话框数据
        :return:
        """
        return self.config[self.current_scene]["dialogues"][self.dialog_index]

    def _prepare_button(self):
        """
        选项框初始化
        :return:
        """

        for choice in self.get_current_dialog()["choices"]:
            #获取选项的文字
            text = choice["text"]
            # 未选中时的选项
            img = self.choice_bg.copy()
            img_text = ResourceLoader.font_dict["loli36"].render(text, True, "black")
            img_text_rect = img_text.get_rect(
                center=(self.window_width * 0.5 * 0.6, self.window_height * 0.5 * 0.10))
            img.blit(img_text, img_text_rect)
            # 选中时的选项
            img_hover = self.choice_hover_bg.copy()
            img_hover_text = ResourceLoader.font_dict["loli36"].render(text, True, "white")
            hover_text_rect = img_hover_text.get_rect(
                center=(self.window_width * 0.5 * 0.6, self.window_height * 0.5 * 0.10))
            img_hover.blit(img_hover_text, hover_text_rect)

            #添加选项到选项框中
            self.choice_box.append(MenuButton(
                img,
                img_hover,
                img.get_rect(),
            ))

    def _draw_name(self):
        speaker = self.get_current_dialog()["speaker"]
        if speaker != "旁白":
            if speaker == "player":
                speaker_name = ResourceLoader.font_dict["MiSansDemibold36"].render(self.current_player + ":", True, "white")
            else:
                speaker_name = self.character_group.get_character(speaker).name_surface
            self.dialog_bg_copy.blit(speaker_name, (
                self.window_width * 0.1,
                self.window_height * 0.65
            ))

    def _draw_character(self):
        """
        在当前对话角色不为旁白和玩家时，渲染角色图片
        :return:
        """
        speaker = self.get_current_dialog()["speaker"]
        if speaker != "旁白" and speaker !="player":
            #获取当前对话角色情绪与位置信息
            emotion = self.get_current_dialog()["character"]["emotion"]
            position = self.get_current_dialog()["character"]["position"]
            img = self.character_group.get_character(speaker).emotions[emotion]

            img_rect = img.get_rect()
            # 调整图片大小
            img = pygame.transform.scale(img, (self.window_height * 0.95 * img_rect.width / img_rect.height,
                                               self.window_height * 0.95))
            #渲染图片
            self.display_surface.blit(img,
                                      img.get_rect(
                                          midbottom=(self.window_width * Settings.position[position], self.window_height)),
                                      )

    def _draw_text(self):
        text = self.get_current_dialog()["text"]
        text_surface = ResourceLoader.font_dict["MiSansDemibold24"].render(text, True, "white")
        text_rect = text_surface.get_rect(topleft=(self.window_width * 0.1, self.window_height * 0.75))
        self.dialog_bg_copy.blit(text_surface, text_rect)

    def _draw_choice_box(self):
        """
        渲染选项框
        :return:
        """
        mid = 0.7 / (len(self.choice_box) + 1)
        for i in range(len(self.choice_box)):

            self.choice_box[i].rect.center = (self.window_width * 0.5,
                                              (0.15 + mid * (i + 1)) * self.window_height)
            self.display_surface.blit(self.choice_box[i].img, self.choice_box[i].rect)

    def _choice_box_event(self,event:pygame.event.Event):
        """
        选项框事件处理
        :return:
        """
        for i in range(len(self.choice_box)):
            self.choice_box[i].hover_animation()
            #处理选项框点击事件
            if self.choice_box[i].is_press_down(event):
                self.current_scene = self.get_current_dialog()["choices"][i]["nextScene"]
                self.scene_record.append(self.current_scene)
                self.is_choice_reloads = True
                self.dialog_index = 0

    def _draw_button(self):
        """
        按钮渲染
        :return:
        """
        # 按钮渲染
        self.display_surface.blit(self.back_button.img, self.back_button.rect)
        self.display_surface.blit(self.voice_button.img, self.voice_button.rect)
        self.display_surface.blit(self.save_button.img, self.save_button.rect)



def test():
    """
    测试函数
    :return:
    """
    loader = ResourceLoader()
    loader.load_all_resource()
    loader.wait_load_finish()

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock =pygame.time.Clock()

    save_datas = {"player":
                      {
                          "name": "陈海文",
                          "honor_value": 0

                      },
                  "chapter_data":
                      {
                      "chapter": "C1",
                      "scene": "C1_1",
                      "dialog_index": 0
                        }
                  }

    demo = DemoCharacter()

    char_group =CharacterGroup()
    char_group.add_character(demo)

    content_chapter = GameScene()
    content_chapter.read_save(save_datas, char_group)
    content_chapter.chapter_read()
    content_chapter.init()



    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            content_chapter.handle_event(event)
        content_chapter.draw()
        print(content_chapter.current_chapter)

        pygame.display.update()


if __name__ == '__main__':
    test()