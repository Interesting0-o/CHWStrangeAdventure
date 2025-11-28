import pygame
from Pages.Page import Page
from Elements.MenuButton import MenuButton
from ResourceLoader import ResourceLoader



class GameScene(Page):

    def __init__(self):
        super().__init__()

    def button_define(self):
        pass

    def handle_event(self, event):
        pass

    def draw(self):
        self.display_surface = pygame.display.get_surface()

    def reset(self):
        pass

    def init(self):
        self.display_surface = pygame.display.get_surface()


def test():
    import sys

    loader = ResourceLoader()
    loader.load_all_resource()

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    game_scene = GameScene()


    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game_scene.handle_event(event)

        game_scene.draw()
        pygame.display.update()




if __name__ == '__main__':
    test()
