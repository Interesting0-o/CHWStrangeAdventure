import pygame
import json
from Chapters.Chapter import Chapter
from ResourceLoader import ResourceLoader
from Elements.MenuButton import MenuButton


class ContentChapter(Chapter):
    def __init__(self,save_data):
        super().__init__()


        self.config = None
        #存档数据
        self.save_data = save_data
        self.current_scene = save_data["scene"]
        self.dialog_index = 0

        # 选项框内容
        self.choice_bg = None
        self.choice_hover_bg = None
        self.choice_box= []

        # 背景图
        self.current_bg = None
        self.current_bg_alpha = 0
        self.current_bg_copy = None

    def init(self):
        self.display_surface = pygame.display.get_surface()
        with open(self.path[:-9] + f"/data/{self.save_data["chapter"]}.json", "r",encoding="utf-8") as f:
            self.config = json.load(f)

        # 选项框初始化
        self.choice_bg = pygame.surface.Surface((self.window_width*0.6, self.window_height*0.15))
        self.choice_bg.fill("green")
        #未选中时的选项框添加边框
        pygame.draw.rect(
            self.choice_bg,
            "white",
            (0, 0, self.window_width*0.6, self.window_height*0.15),
            border_radius= int(self.window_height*0.06),
        )
        pygame.draw.rect(
            self.choice_bg,
            "orange",
            (0, 0, self.window_width*0.6, self.window_height*0.15),
            border_radius= int(self.window_height*0.06),
            width=5,
        )
        self.choice_bg.set_colorkey("green")
        #选中时的选项框添加边框
        self.choice_hover_bg = pygame.surface.Surface((self.window_width*0.6, self.window_height*0.15))
        self.choice_hover_bg.fill("green")
        pygame.draw.rect(
            self.choice_hover_bg,
            "#ffd68c",
            (0, 0, self.window_width*0.6, self.window_height*0.15),
            border_radius= int(self.window_height*0.06),
        )
        pygame.draw.rect(
            self.choice_hover_bg,
            "orange",
            (0, 0, self.window_width*0.6, self.window_height*0.15),
            border_radius= int(self.window_height*0.06),
            width=5,
        )
        self.choice_hover_bg.set_colorkey("green")

        self.current_bg = eval(f"ResourceLoader.{self.config[self.current_scene]['bg']}")
        self.current_bg_copy = self.current_bg.copy()
        self.current_bg = pygame.transform.scale(self.current_bg_copy, (self.window_width, self.window_height))


        if self.config[self.current_scene]["end_with"] =="choice":
            for i in range(self.config[self.current_scene]["choice_num"] ):

                text = self.config[self.current_scene]["dialogues"][-1]["choices"][i]["text"]
                #未选中时的选项
                img = self.current_bg.copy()
                img_text = ResourceLoader.font_loliti36.render(text, True, "black")
                text_rect = img_text.get_rect(center=(self.window_width*0.5, self.window_height*0.5))
                img.blit(img_text, text_rect)
                #选中时的选项
                img_hover = self.current_bg.copy()
                img_hover_text = ResourceLoader.font_loliti36.render(text, True, "black")
                hover_text_rect = img_hover_text.get_rect(center=(self.window_width*0.5, self.window_height*0.5))
                img_hover.blit(img_hover_text, hover_text_rect)
                self.choice_box.append(MenuButton(
                    img,
                    img_hover,
                    img.get_rect(),
                ))



    def handle_event(self, event):
        pass

    def dialog_system(self):
        pass

    def show(self):
        self.display_surface.blit(self.current_bg, (0, 0))
        #测试
        self.display_surface.blit(self.choice_bg, (0, 0))
        self.display_surface.blit(self.choice_hover_bg, (0, 500))





if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock =pygame.time.Clock()

    save_datas = {"chapter": "C1", "scene": "C1_1"}

    content_chapter = ContentChapter(save_datas)
    content_chapter.init()

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        content_chapter.show()

        pygame.display.update()