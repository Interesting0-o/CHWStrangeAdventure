from Save_Load import SaveLoad
import pygame
pygame.font.init()

class ResourceLoader:

    #路径
    path = __file__[:-18]
    #字体
    font_loliti24 = pygame.font.Font(path+r"\resource\font\萝莉体 第二版.ttf", 24)
    font_loliti36 = pygame.font.Font(path + r"\resource\font\萝莉体 第二版.ttf", 36)
    font_loliti48 = pygame.font.Font(path + r"\resource\font\萝莉体 第二版.ttf", 48)
    font_MiSans_Demibold24 = pygame.font.Font(path+r"\resource\font\MiSans\MiSans-Demibold.ttf", 24)
    font_MiSans_Demibold36 = pygame.font.Font(path + r"\resource\font\MiSans\MiSans-Demibold.ttf", 36)


    #按钮
    yes_button_animation = [
        pygame.image.load(__file__[:-18] +rf"/resource/img/button/yes_button/yes_button_{i:02d}.png") for i in range(30)
    ]
    no_button_animation = [
        pygame.image.load(__file__[:-18] + rf"/resource/img/button/no_button/no_button_{i:02d}.png") for i in range(30)
    ]
    close_button_animation = [
        pygame.image.load(__file__[:-18] + rf"/resource/img/button/close_button/close_button_{i:02d}.png") for i in range(30)
    ]
    frame_setting_button_animation = [
        pygame.image.load(__file__[:-18] + rf"/resource/img/button/frame_setting_button/frame_setting_button_{i:02d}.png") for i in range(30)
    ]
    start_button_animation = [
        pygame.image.load(__file__[:-18] + rf"/resource/img/button/start_button/start_button_1{i:02d}.png") for i in range(30)
    ]
    settings_button_animation = [
        pygame.image.load(__file__[:-18] + rf"/resource/img/button/settings_button/settings_button_{i:02d}.png") for i in range(30)
    ]
    load_button_animation = [
        pygame.image.load(__file__[:-18] + rf"/resource/img/button/load_button/load_button_{i:02d}.png") for i in range(30)
    ]
    quit_button_animation = [
        pygame.image.load(__file__[:-18] + rf"/resource/img/button/quit_button/quit_button_{i:02d}.png") for i in range(30)
    ]

    #图标icon
    voice = pygame.image.load(__file__[:-18] + r"\resource\img\icon\voice.png")
    voice_hover = pygame.image.load(__file__[:-18] + r"\resource\img\icon\voice_hover.png")

    back = pygame.image.load(__file__[:-18] + r"\resource\img\icon\back.png")
    back_hover = pygame.image.load(__file__[:-18] + r"\resource\img\icon\back_hover.png")

    next = pygame.image.load(__file__[:-18] + r"\resource\img\icon\next.png")
    next_hover = pygame.image.load(__file__[:-18] + r"\resource\img\icon\next_hover.png")

    last = pygame.image.load(__file__[:-18] + r"\resource\img\icon\last.png")
    last_hover = pygame.image.load(__file__[:-18] + r"\resource\img\icon\last_hover.png")

    save = pygame.image.load(__file__[:-18] + r"\resource\img\icon\save.png")
    save_hover = pygame.image.load(__file__[:-18] + r"\resource\img\icon\save_hover.png")

    delete = pygame.image.load(__file__[:-18] + r"\resource\img\icon\delete.png")
    delete_hover = pygame.image.load(__file__[:-18] + r"\resource\img\icon\delete_hover.png")



    #游戏场景的背景
    background = {
        "library": pygame.image.load(__file__[:-18] + r"\resource\img\ChapterBG\library.png")
    }

    #游戏开始界面背景
    start_bg = pygame.image.load(__file__[:-18] + r"/resource/img/bg/bg.png")
    title_bg = pygame.image.load(__file__[:-18] + r"/resource/img/title/title.png")

    # 对话框
    dialog_box = pygame.image.load(__file__[:-18] + r"\resource\img\bg\DialogBox.png")

    #对话款背景
    dialog_bg = pygame.image.load(__file__[:-18] + r"\resource\img\BG\DialogBG.png")

    #DemoCharacter资源
    demo_character_neutral = pygame.image.load(__file__[:-18] + r"/resource/characters/demoCharacter/img/neutral.png")
    demo_character_voice ={

    }
    #游戏ui
    big_ui = pygame.image.load(path + r"/resource/img/bg/SettingsPageBG.png")
    quit_window = pygame.image.load(path + r"/resource/img/title/quit.png")


