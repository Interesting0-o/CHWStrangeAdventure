import pygame
from Pages.Page import Page
from ResourceLoader import ResourceLoader
from settings import Settings
from Elements.MenuButton import MenuButton
from Elements.ButtonGroup import ButtonGroup
from Characters import *
from Voice import Voice


class GameScene(Page):
    def __init__(self):
        super().__init__()
        #音频
        self.voice = None

        #音频加载状态
        self.is_voice_load:bool = False
        #检验当前的选项是否载入
        self.is_choice_load:bool = False

        #资源初始化

        self.plot:dict|None = None
        self.bg_dict:dict|None = None


        #按钮类
        self.button_group = ButtonGroup()
        self.voice_button:MenuButton = None
        self.back_button:MenuButton = None
        self.save_button:MenuButton = None

        #场景记录
        self.current_player_honor = 0
        self.current_chapter = None
        self.scene_record = []

        #玩家类
        self.current_player = None


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
        self.current_bg_scale = None

        #对话框
        self.dialog_bg = ResourceLoader.bg_dict["DialogBG"]
        self.dialog_scale = None
        self.dialog_bg_copy = None

        #音轨
        self.char_channel = Voice.char_channel

        #黑场
        self.black_bg = pygame.surface.Surface((3840, 2160))
        self.black_bg.fill("black")
        self.black_bg.set_alpha(128)

        #角色组
        self.character_group = None

    def reset(self):

        #角色组
        self.character_group = None

        #音频
        self.voice = None

        #音频加载状态
        self.is_voice_load = False
        #检验当前的选项是否载入
        self.is_choice_load = False

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
            "bg":self.get_current_bg()
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
        self.dialog_index = save_data["chapter_data"]["dialog_index"]
        self.current_chapter = save_data["chapter_data"]["chapter"]
        self.scene_record.append(self.current_scene)

        #角色组
        self.character_group = character_group

        #获取当前章节资源
        self.plot = ResourceLoader.plot_dict

    def init(self):
        #获取当前窗口
        self.display_surface = pygame.display.get_surface()

        self.current_bg = ResourceLoader.chapter_bg_dict[self.get_current_bg()]
        self.current_bg_scale = pygame.transform.scale(self.current_bg, (self.window_width, self.window_height))

        #对话框处理
        self.dialog_scale = pygame.transform.scale(self.dialog_bg, (self.window_width, self.window_height))

        #初始化选项框
        self._choice_init()

        #初始化按钮
        self._button_init()



    def _choice_init(self):
        """
        绘制选项框，鼠标悬停时的选项框，和正常时的选项框
        :return:
        """
        # 选项框初始化
        self.choice_bg = pygame.surface.Surface((self.window_width * 0.6, self.window_height * 0.10))
        self.choice_bg.fill("green")
        # 未选中时的选项框添加边框
        pygame.draw.rect(
            self.choice_bg,
            "white",
            (0, 0, self.window_width * 0.6, self.window_height * 0.10),
            border_radius=int(self.window_height * 0.06),
        )
        pygame.draw.rect(
            self.choice_bg,
            "orange",
            (0, 0, self.window_width * 0.6, self.window_height * 0.10),
            border_radius=int(self.window_height * 0.06),
            width=5,
        )
        self.choice_bg.set_colorkey("green")
        # 选中时的选项框添加边框
        self.choice_hover_bg = pygame.surface.Surface((self.window_width * 0.6, self.window_height * 0.10))
        self.choice_hover_bg.fill("green")
        pygame.draw.rect(
            self.choice_hover_bg,
            "#ffd68c",
            (0, 0, self.window_width * 0.6, self.window_height * 0.10),
            border_radius=int(self.window_height * 0.06),
        )
        pygame.draw.rect(
            self.choice_hover_bg,
            "orange",
            (0, 0, self.window_width * 0.6, self.window_height * 0.10),
            border_radius=int(self.window_height * 0.06),
            width=5,
        )
        self.choice_hover_bg.set_colorkey("green")

    def _button_init(self):
        """
        按钮定义
        :return:
        """
        # 音频重播按钮
        voice = ResourceLoader.icon_dict["voice"]
        voice = pygame.transform.scale(voice, (50, 50))
        voice_bg_hover = ResourceLoader.icon_dict["voice_hover"]
        voice_bg_hover = pygame.transform.scale(voice_bg_hover, (50, 50))

        self.voice_button = MenuButton(
            voice,
            voice_bg_hover,
            voice.get_rect(center=(self.window_width * 0.9, self.window_height * 0.92))
        )

        # 回退按钮
        back = ResourceLoader.icon_dict["back"]
        back = pygame.transform.scale(back, (50, 50))
        back_bg_hover = ResourceLoader.icon_dict["back_hover"]
        back_bg_hover = pygame.transform.scale(back_bg_hover, (50, 50))
        self.back_button = MenuButton(
            back,
            back_bg_hover,
            back.get_rect(center=(self.window_width * 0.9 - 50, self.window_height * 0.92))
        )
        # 保存按钮
        save = ResourceLoader.icon_dict["save"]
        save = pygame.transform.scale(save, (50, 50))
        save_bg_hover = ResourceLoader.icon_dict["save_hover"]
        save_bg_hover = pygame.transform.scale(save_bg_hover, (50, 50))
        self.save_button = MenuButton(
            save,
            save_bg_hover,
            save.get_rect(center=(self.window_width * 0.9 + 50, self.window_height * 0.92))
        )

        #将所有的按钮添加到按钮组中
        self.button_group.add_button(self.voice_button,self.back_button,self.save_button)

    def get_current_dialog(self):
        """
        获取当前对话框数据
        :return:
        """
        return self.plot[self.current_chapter][self.current_scene]["dialogues"][self.dialog_index]

    def get_current_bg(self):
        """
        获取当前背景在字典中的的key值
        :return:
        """
        return self.plot[self.current_chapter][self.current_scene]["bg"]

    def get_current_bgm(self):
        """
        获取当前背景音乐在字典中的的key值
        :return:
        """
        return self.plot[self.current_chapter][self.current_scene]["bgm"]

    def _prepare_choice(self):
        """
        选项框内容预渲染
        :return:
        """

        for choice in self.plot[self.current_chapter][self.current_scene]["dialogues"][-1]["choices"]:
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
        """
        渲染角色名字
        :return:
        """
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
        """
        渲染文字对话
        :return:
        """
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
            #选项框动画
            self.choice_box[i].hover_animation()
            #处理选项框点击事件
            if self.choice_box[i].is_press_down(event):
                #下一场景
                self.current_scene = self.get_current_dialog()["choices"][i]["nextScene"]

                self.scene_record.append(self.current_scene)
                self.is_choice_reloads = True
                self.dialog_index = 0

    def is_save_press(self,event:pygame.event.Event):
        """
        判断是否保存按钮被点击
        :param event:
        :return:
        """
        return self.save_button.is_press_down(event)

    def _draw_button(self):
        """
        按钮渲染
        :return:
        """
        # 按钮动画启动
        self.button_group.hover_animation()
        # 按钮渲染
        self.display_surface.blit(self.back_button.img, self.back_button.rect)
        self.display_surface.blit(self.voice_button.img, self.voice_button.rect)
        self.display_surface.blit(self.save_button.img, self.save_button.rect)

    def _draw_photo(self):
        """
        渲染照片,暂时不用，未来实现
        :return:
        """
        if self.get_current_dialog()["photo"] is not None:
            print("photo")

    def _next_text_event(self,event:pygame.event.Event):
        """
        处理下一句对话事件
        :param event:
        :return:
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            #判断当前是否鼠标左键点击且当前对话框类型不是choice
            self.dialog_index += 1

            #更改语音载入状态
            self.is_voice_load = False

            #判断是否到达对话框末尾
            if self.voice is not None:
                self.voice.stop()

            if self.dialog_index >= len(self.plot[self.current_chapter][self.current_scene]["dialogues"]):
                #重置对话框索引
                self.dialog_index = 0

                # 更改语音载入状态
                self.is_voice_load = False

                #更新到下一场景
                self.current_scene = self.plot[self.current_chapter][self.current_scene]["next_scene"]


    def next_chapter(self):
        """
        切换到下一个章节
        :return:
        """
        if self.current_scene is None:
            try:
                print(str(int(self.current_chapter[1:])+1))

                chapter = "C" + str(int(self.current_chapter[1:])+1)
                if chapter not in self.plot.keys():
                    raise KeyError
                #正常切换到下一个章节
                self.current_chapter = chapter
                self.current_scene = self.plot[self.current_chapter].keys()[0]
                self.dialog_index = 0
            except KeyError:
                self.is_end = True
                print("章节不存在,完啦")

    def _voice_event(self):
        """
        处理音频事件
        :return:
        """
        if self.get_current_dialog()["speaker"] != "旁白" and self.get_current_dialog()["speaker"] != "player" and not self.is_voice_load:
            #播放角色语音
            voice_path = self.get_current_dialog()["character"]["voice"]
            self.voice = pygame.mixer.Sound(self.path[:-6] + rf"\resource\sound\voice\{voice_path}.wav")
            self.char_channel = self.voice.play()
            self.is_voice_load = True

    def _button_event(self,event:pygame.event.Event):
        """
        按钮事件处理
        :param event:
        :return:
        """
        if self.voice_button.is_press_down(event) and self.voice is not None and self.is_voice_load:
            #切换当前音频的播放状态
            if self.char_channel.get_busy():
                self.voice.stop()
            else:
                self.char_channel.play(self.voice)

        if self.back_button.is_press_down(event) and self.dialog_index > 0:

            #回退到上一句对话
            self.dialog_index -= 1
            # 更改语音载入状态
            self.is_voice_load = False

            #更改语音载入状态
            if self.voice is not None:
                self.voice.stop()



    def handle_event(self, event: pygame.event.Event)-> None:
        """
        事件处理
        :param event:
        :return:
        """

        #判断是否到达结尾
        if self.is_end:
            return

        if self.plot[self.current_chapter][self.current_scene]["end_with"] == "choice" and not self.is_choice_load:
            self._prepare_choice()
            self.is_choice_load = True


        #当按钮被鼠标悬停时，按钮事件的处理
        if self.button_group.is_hover():
            # 处理按钮事件
            self._button_event(event)
        else:
            # 处理选项框事件
            if self.get_current_dialog()["type"] == "choice":
                #处理按钮点击事件
                self._choice_box_event(event)

            #处理文字对话事件
            elif self.get_current_dialog()["type"] == "dialogue":
                #处理音频事件
                self._voice_event()
                #处理下一句对话事件
                self._next_text_event(event)
                #判断是否到达结尾
                self.next_chapter()

    def draw(self):
        #判断是否到达结尾
        if self.is_end:
            return

        #背景渲染
        self.display_surface.blit(self.current_bg, (0, 0))

        self.dialog_bg_copy = self.dialog_scale.copy()

        #判断当前对话框类型是否为dialogue
        if self.get_current_dialog()["type"]=="dialogue" :
            #获取当前对话角色数据人物贴图
            self._draw_character()
            # 处理照片
            self._draw_photo()
            #人物名字渲染
            self._draw_name()
            # 处理文字对话
            self._draw_text()
            # 对话框渲染
            self.display_surface.blit(self.dialog_bg_copy, (0, 0))

        # 当当前对话框类型为choice时，显示选项框
        elif self.get_current_dialog()["type"]=="choice":
            #图片渲染
            self._draw_photo()
            #将黑场显示出来
            self.display_surface.blit(self.black_bg, (0, 0))
            #渲染选项
            self._draw_choice_box()

        # 按钮渲染
        self._draw_button()

def test():
    """
    测试函数
    :return:
    """
    pygame.mixer.init()

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock =pygame.time.Clock()

    loader = ResourceLoader()
    loader.load_all_resource()
    loader.wait_load_finish()


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
    content_chapter.init()

    print(content_chapter.path[:-6])

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            content_chapter.handle_event(event)
        content_chapter.draw()

        pygame.display.update()

if __name__ == '__main__':
    test()