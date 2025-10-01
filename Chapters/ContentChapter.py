import pygame
import json
from Chapters.Chapter import Chapter
from ResourceLoader import ResourceLoader
from settings import Settings
from Elements.MenuButton import MenuButton
from Characters import *


class ContentChapter(Chapter):
    def __init__(self):
        super().__init__()
        #场景结束控件
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
        self.dialog_bg_copy = self.dialog_bg.copy()

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

    def init(self,
             save_data,#存档数据
             character_group:CharacterGroup,#角色组
             current_player:Player#玩家
             ):
        #玩家引用
        self.current_player = current_player
        #存档数据
        self.save_data = save_data
        self.current_scene = save_data["scene"]
        self.dialog_index = 0
        #角色组
        self.character_group = character_group

        self.display_surface = pygame.display.get_surface()
        with open(self.path[:-9] + f"/data/{self.save_data["chapter"]}.json", "r",encoding="utf-8") as f:
            self.config = json.load(f)

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

        #背景缩放
        self.dialog_bg_copy = pygame.transform.scale(self.dialog_bg, (self.window_width, self.window_height))



    def handle_event(self, event):
        self.next_text(event)


    def next_text(self,event):

        if not self.is_choosing:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.next_text_event = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    print("key down")
                    self.next_text_event = True
                    print("event start")
            else:
                self.next_text_event = False



    def show(self):
        #背景渲染
        self.display_surface.blit(self.current_bg, (0, 0))

        #判断是否结束
        if not self.is_chapter_end:

            # 选项条件预渲染
            if self.config[self.current_scene]["end_with"] == "choice" and self.is_choice_reloads:
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
                self.dialog_index = 0
                if self.current_scene not in self.config:
                    self.is_chapter_end = True

            #判断当前对话框类型是否为dialogue
            elif self.config[self.current_scene]["dialogues"][self.dialog_index]["type"]=="dialogue" :

                # 修改当前状态呢量
                self.is_choosing = False
                #人物图层渲染
                speaker = self.config[self.current_scene]["dialogues"][self.dialog_index]["speaker"]
                if speaker != "旁白":
                    #获取当前对话角色数据
                    if speaker !="player":
                        emotion = self.config[self.current_scene]["dialogues"][self.dialog_index]["character"]["emotion"]
                        position = self.config[self.current_scene]["dialogues"][self.dialog_index]["character"]["position"]
                        img = self.character_group.get_character(speaker).emotions[emotion].copy()
                        img_rect = img.get_rect()
                        img = pygame.transform.scale(img,(self.window_height*0.95 * img_rect.width / img_rect.height,self.window_height*0.95))

                        self.display_surface.blit(img,
                                                  img.get_rect(midbottom = (self.window_width*Settings.position[position],self.window_height)),
                                                  )

                #对话框渲染
                self.display_surface.blit(self.dialog_bg_copy, (0, 0))

                #人物名字渲染
                if speaker != "旁白":
                    if speaker =="player":
                        speaker_name = ResourceLoader.font_MiSans_Demibold36.render(self.current_player.name+":", True, "white")
                    else:
                        speaker_name = ResourceLoader.font_MiSans_Demibold36.render(speaker+":", True, "white")
                    self.display_surface.blit(speaker_name,(
                        self.window_width*0.1,
                        self.window_height*0.65
                    ))

                # 处理文字对话
                text = self.config[self.current_scene]["dialogues"][self.dialog_index]["text"]
                text_surface = ResourceLoader.font_MiSans_Demibold24.render(text, True, "white")
                text_rect = text_surface.get_rect(topleft=(self.window_width*0.1, self.window_height*0.75))
                self.display_surface.blit(text_surface, text_rect)
                #事件处理
                if self.next_text_event:
                    self.dialog_index -= -1
                    self.next_text_event = False

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
                    self.display_surface.blit(self.choice_box[i].img, self.choice_box[i].rect)

                    if self.choice_box[i].is_pressed():
                        self.current_scene = self.config[self.current_scene]["dialogues"][self.dialog_index]["choices"][i]["nextScene"]
                        self.is_choice_reloads = True
                        self.dialog_index = 0
                        if self.current_scene not in self.config:
                            self.is_chapter_end = True




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
    content_chapter.init(save_datas, char_group, player)


    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            content_chapter.handle_event(event)
        content_chapter.show()

        pygame.display.update()