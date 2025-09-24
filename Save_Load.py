import threading
import pygame
import os
from Event import EventBus
from concurrent.futures import ThreadPoolExecutor

class SaveLoad:
    instance = None
    def __new__(cls):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.event_bus = EventBus()
        self.pool = ThreadPoolExecutor(max_workers=20)
        self.number = 0
        self.lock = threading.Lock()

    def get_filename_index(self, file_name:str)->int:
        number = 0
        for i in range(len(file_name)):
            if file_name[i].isdigit():
                number = number * 10 + int(file_name[i])
        return number
    
    def __LoadImage_ofList(self, file_path:str, list:list, index:int):
        list[index] = pygame.image.load(file_path)

    def LoadImage_fileDir(self, fileDir_path:str, list:list):
        files_list = os.listdir(fileDir_path)
        for file in files_list:
            file_path = os.path.join(fileDir_path, file)
            if os.path.isfile(file_path):
                self.pool.submit(self.__LoadImage_ofList, file_path, list, self.get_filename_index(file))
        self.pool.shutdown(wait=True)
        #EventBus.emit("load_image_finish")
        
if __name__ == "__main__":
    
    screen = pygame.display.set_mode((1280, 720))
    surface = pygame.display.get_surface()
    list = [None for i in range(300)]
    SaveLoad().LoadImage_fileDir(rf"resource/video/openVideo", list)

    index = 0
    while True:
        pygame.time.Clock().tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        if index < 299:
            surface.blit(list[index], (0, 0))
            index += 1
        pygame.display.update()