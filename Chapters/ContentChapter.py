import pygame
import json
import threading
from Chapters.Chapter import Chapter
from ResourceLoader import ResourceLoader
from settings import Settings
from Elements.MenuButton import MenuButton
from Characters import *


class ContentChapter(Chapter):
    def __init__(self):
        super().__init__()
        #场景记录
        self.scene_record = []
        #玩家类
        self.current_player = None

        self.is_choosing = False
        self.is_chapter_end = None

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
        self.dialog_bg = ResourceLoader.dialog_bg
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

        #预加载音频资源
        self.voice_dic = {}
        self.is_voice_on = True
        self.current_voice = None
        self.is_voice = False

        #音频处理线程
        self.t = None

        #音频重播按钮
        voice = ResourceLoader.voice
        voice = pygame.transform.scale(voice, (50, 50))
        voice_bg_hover = ResourceLoader.voice_hover
        voice_bg_hover = pygame.transform.scale(voice_bg_hover, (50, 50))
        #按钮处理
        self.is_button_on = False
        # 音频按钮
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

    def to_dict(self):
        return{
            "chapter": self.save_data["chapter"],
            "scene": self.current_scene,
            "dialog_index": self.dialog_index
        }


    def read_config(self,
        save_data,  # 存档数据
        character_group: CharacterGroup,  # 角色组
        current_player: Player# 玩家
                    ):
        #玩家引用
        self.current_player = current_player
        #存档数据
        self.save_data = save_data
        self.current_scene = save_data["scene"]
        self.scene_record.append(self.current_scene)
        self.dialog_index = 0
        #角色组
        self.character_group = character_group

        self.display_surface = pygame.display.get_surface()
        with open(self.path[:-9] + f"/data/{self.save_data["chapter"]}.json", "r",encoding="utf-8") as f:
            self.config = json.load(f)



    def init(self):


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

        self.current_bg = eval(f"ResourceLoader.{self.config[self.current_scene]['bg']}")
        self.current_bg_copy = self.current_bg.copy()
        self.current_bg = pygame.transform.scale(self.current_bg_copy, (self.window_width, self.window_height))


        #对话框处理
        self.dialog_scale = pygame.transform.scale(self.dialog_bg, (self.window_width, self.window_height))

        #音频预加载
        self.thread_read()



    def handle_event(self, event):

        #事件处理：按钮按下
        # 回退按钮
        if self.back_button.is_hovered():
            self.is_button_on = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.dialog_index >0:
                    self.dialog_index -=1
        #音频播放
        elif self.voice_button.is_hovered():
            self.is_button_on = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.is_voice_on = True
        else :
            self.is_button_on = False


        self.next_text(event)


    def next_text(self,event):

        if not (self.is_choosing or self.is_button_on):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print("mouse down")
                    self.next_text_event = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self.next_text_event = True
            else:
                self.next_text_event = False

    def thread_read(self):
        for i in range(len(self.config[self.current_scene]["dialogues"])):
            if self.config[self.current_scene]["dialogues"][i]["type"]=="dialogue":
                speaker = self.config[self.current_scene]["dialogues"][i]["speaker"]

                if speaker != "旁白" and speaker !="player":
                    voice = self.config[self.current_scene]["dialogues"][i]["character"]["voice"]
                    self.voice_dic[voice] = pygame.mixer.Sound(
                        self.path[:-9] + rf"/resource/characters/{speaker}/voice/{voice}.wav"
                    )



    def show(self):
        #背景渲染
        self.display_surface.blit(self.current_bg, (0, 0))

        #判断是否结束
        if not self.is_chapter_end:
            self.dialog_bg_copy = self.dialog_scale.copy()


            # 选项条件预渲染
            if self.is_choice_reloads and self.config[self.current_scene]["end_with"] == "choice":
                self.is_choice_reloads = False
                num = self.config[self.current_scene]["choice_num"]
                for i in range(num):
                    text = self.config[self.current_scene]["dialogues"][-1]["choices"][i]["text"]
                    # 未选中时的选项
                    img = self.choice_bg.copy()
                    img_text = ResourceLoader.font_loliti36.render(text, True, "black")
                    img_text_rect = img_text.get_rect(
                        center=(self.window_width * 0.5 * 0.6, self.window_height * 0.5 * 0.10))
                    img.blit(img_text, img_text_rect)
                    # 选中时的选项
                    img_hover = self.choice_hover_bg.copy()
                    img_hover_text = ResourceLoader.font_loliti36.render(text, True, "white")
                    hover_text_rect = img_hover_text.get_rect(
                        center=(self.window_width * 0.5 * 0.6, self.window_height * 0.5 * 0.10))
                    img_hover.blit(img_hover_text, hover_text_rect)
                    self.choice_box.append(MenuButton(
                        img,
                        img_hover,
                        img.get_rect(),
                    ))


            #判断当前索引是否大于对话框长度
            if self.dialog_index > len(self.config[self.current_scene]["dialogues"]) - 1:
                self.current_scene = self.config[self.current_scene]["next_scene"]
                self.scene_record.append(self.current_scene)
                self.dialog_index = 0
                if self.current_scene in self.config:
                    # 音频资源清理，并开启音频处理线程
                    self.t = threading.Thread(target=self.thread_read)
                    self.t.start()
                else:
                    self.is_chapter_end = True

            #判断当前对话框类型是否为dialogue
            elif self.config[self.current_scene]["dialogues"][self.dialog_index]["type"]=="dialogue" :

                # 修改当前状态呢量
                self.is_choosing = False
                #人物图层渲染
                speaker = self.config[self.current_scene]["dialogues"][self.dialog_index]["speaker"]
                if speaker != "旁白":
                    #获取当前对话角色数据人物贴图
                    if speaker !="player":
                        emotion = self.config[self.current_scene]["dialogues"][self.dialog_index]["character"]["emotion"]
                        position = self.config[self.current_scene]["dialogues"][self.dialog_index]["character"]["position"]
                        img = self.character_group.get_character(speaker).emotions[emotion].copy()
                        img_rect = img.get_rect()
                        img = pygame.transform.scale(img,(self.window_height*0.95 * img_rect.width / img_rect.height,self.window_height*0.95))

                        self.display_surface.blit(img,
                                                  img.get_rect(midbottom = (self.window_width*Settings.position[position],self.window_height)),
                                                  )

                #人物名字渲染
                if speaker != "旁白":
                    if speaker =="player":
                        speaker_name = ResourceLoader.font_MiSans_Demibold36.render(self.current_player.name+":", True, "white")
                    else:
                        speaker_name = ResourceLoader.font_MiSans_Demibold36.render(speaker+":", True, "white")
                    self.dialog_bg_copy.blit(speaker_name,(
                        self.window_width*0.1,
                        self.window_height*0.65
                    ))
                #音频载入
                if  self.is_voice_on:
                    if speaker != "旁白" and speaker !="player":
                        voice_id = self.config[self.current_scene]["dialogues"][self.dialog_index]["character"]["voice"]
                        self.current_voice = self.voice_dic[voice_id]
                        self.current_voice.play()
                        self.is_voice_on = False
                        self.is_voice = True
                    else:
                        self.is_voice = False

                # 处理文字对话
                text = self.config[self.current_scene]["dialogues"][self.dialog_index]["text"]
                text_surface = ResourceLoader.font_MiSans_Demibold24.render(text, True, "white")
                text_rect = text_surface.get_rect(topleft=(self.window_width*0.1, self.window_height*0.75))
                self.dialog_bg_copy.blit(text_surface, text_rect)
                #事件处理
                if self.next_text_event:
                    self.dialog_index -= -1
                    self.is_voice_on = True
                    self.next_text_event = False
                    if self.is_voice:
                        self.current_voice.stop()
                        self.is_voice = False

            # 当当前对话框类型为choice时，显示选项框
            elif self.config[self.current_scene]["dialogues"][self.dialog_index]["type"]=="choice":
                #修改当前状态呢量
                self.is_choosing = True
                #将黑场显示出来
                self.display_surface.blit(self.black_bg, (0, 0))
                #渲染选项，并添加事件
                mid = 0.7/(len(self.choice_box)+1)
                for i in range(len(self.choice_box)):
                    self.choice_box[i].rect.center = (self.window_width*0.5,
                                                      (0.15+mid*(i+1))*self.window_height)
                    self.choice_box[i].hover_animation()
                    self.dialog_bg_copy.blit(self.choice_box[i].img, self.choice_box[i].rect)

                    if self.choice_box[i].is_pressed():
                        self.current_scene = self.config[self.current_scene]["dialogues"][self.dialog_index]["choices"][i]["nextScene"]
                        self.scene_record.append(self.current_scene)
                        self.is_choice_reloads = True
                        self.dialog_index = 0

                        #结束判断
                        if self.current_scene  in self.config:
                            # 音频资源清理，并开启音频处理线程
                            self.t = threading.Thread(target=self.thread_read)
                            self.t.start()
                        else:
                            self.is_chapter_end = True
        # 对话框渲染
        self.display_surface.blit(self.dialog_bg_copy, (0, 0))

        self.voice_button.hover_animation()
        self.display_surface.blit(self.back_button.img, self.back_button.rect)
        self.back_button.hover_animation()
        self.display_surface.blit(self.voice_button.img, self.voice_button.rect)






if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock =pygame.time.Clock()

    save_datas = {"chapter": "C1", "scene": "C1_1"}

    demo = DemoCharacter()

    player = Player()
    player.name = "陈海文"

    char_group =CharacterGroup()
    char_group.add_character(demo)

    content_chapter = ContentChapter()
    content_chapter.read_config(save_datas, char_group, player)
    content_chapter.init()


    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            content_chapter.handle_event(event)
        content_chapter.show()
        pygame.display.update()