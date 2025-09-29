import pygame
pygame.font.init()

class ResourceLoader:

    #路径
    path = __file__[:-18]
    #字体
    font_loliti24 = pygame.font.Font(path+r"\resource\font\萝莉体 第二版.ttf", 24)
    font_loliti36 = pygame.font.Font(path + r"\resource\font\萝莉体 第二版.ttf", 36)
    font_MiSans_Demibold24 = pygame.font.Font(path+r"\resource\font\MiSans\MiSans-Demibold.ttf", 24)

    #对话框
    dialog_box = pygame.image.load(__file__[:-18] +r"\resource\img\bg\DialogBox.png")

    #按钮
    yes_button_animation = [
        pygame.image.load(__file__[:-18] +rf"/resource/img/button/yes_button/yes_button_{i:02d}.png") for i in range(30)
    ]

    no_button_animation = [
        pygame.image.load(__file__[:-18] + rf"/resource/img/button/no_button/no_button_{i:02d}.png") for i in range(30)
    ]

    #游戏场景的背景
    library = pygame.image.load(__file__[:-18] + r"\resource\img\ChapterBG\library.png")



