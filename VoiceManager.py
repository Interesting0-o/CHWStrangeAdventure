import pygame
pygame.mixer.init()


class VoiceManager:

    char_channel = pygame.mixer.Channel(0)
    effect_channel = pygame.mixer.Channel(1)
    path = __file__[:-16]
    bgm_path = {
        "main": path + r"\resource\sound\bgm\main.mp3",
    }

    is_bgm_playing = False

    def __init__(self)->None:
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)

    def set_volume(self, volume:tuple[float,float,float])->None:

        #设置背景音乐音量
        pygame.mixer.music.set_volume(volume[0])
        #设置角色音效音量
        self.char_channel.set_volume(volume[1])
        #设置特效音效音量
        self.effect_channel.set_volume(volume[2])

    @staticmethod
    def play_bgm(bgm_name:str)->None:
        if not VoiceManager.is_bgm_playing:
            pygame.mixer.music.load(VoiceManager.bgm_path[bgm_name])
            pygame.mixer.music.play(-1)
            VoiceManager.is_bgm_playing = True

if __name__ == '__main__':
    vm = VoiceManager()
    vm.play_bgm("main")