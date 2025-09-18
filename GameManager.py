import pygame

class GameManager:


    def __init__(self):
        pass 








if __name__ == '__main__':
    game_manager = GameManager()


    pygame.init()

    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("GameDemo")

    clock = pygame.time.Clock()
    dt = clock.tick(60) / 1000.0

    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # game_manager.run(dt)

        pygame.display.update()
        dt = clock.tick(60) / 1000.0    

    

        