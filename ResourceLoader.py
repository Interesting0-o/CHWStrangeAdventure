import pygame
import threading
import os
pygame.font.init()

class ResourceLoader:

    #路径
    path = __file__[:-18] + r"\resource"
    img_resource_path = {
        #图片资源
        'bg':path + r'\img\bg',
        'ChapterBG':path + r'\img\ChapterBG',
        'icon':path + r'\img\icon',
        'title':path + r'\img\title'
    }
    bg_dict = {}
    chapter_bg_dict = {}
    icon_dict = {}
    title_dict = {}

    img_dict = {
        "bg":bg_dict,
        "ChapterBG":chapter_bg_dict,
        "icon":icon_dict,
        "title":title_dict
    }

    button_resource_path = {
        #按钮资源
        'close_button':path + r'\img\button\close_button',
        'frame_setting_button':path + r'\img/button\frame_setting_button',
        'load_button':path + r'\img\button/load_button',
        'no_button':path + r'\img\button\no_button',
        'quit_button':path + r'\img\button\quit_button',
        'settings_button':path + r'\img\button\settings_button',
        'start_button':path + r'\img\button\start_button',
        'yes_button':path + r'\img\button\yes_button'
    }
    button_dict = {}


    font_resource_path = {
        "MiSansDemibold" : path + r'\font\MiSans-Demibold.ttf',
        "loli":path + r'\font\萝莉体 第二版.ttf',
    }
    font_size = [24,36]
    font_dict = {}

    #检查所有资源是否加载完毕
    is_load_finish = False

    current_progress = 0


    def __init__(self):
        pass

    def load_all_resource(self)->None:
        """
        加载所有资源
        :return:
        """
        #加载所有的图片资源
        img_thread = [
            threading.Thread(target=self.load_img,args=(path,self.img_dict[name]))
            for name,path in self.img_resource_path.items()
        ]
        #加载所有的按钮资源
        button_thread = [
            threading.Thread(target=self.load_button,args=(name,path))
            for name,path in self.button_resource_path.items()
        ]

        font_24_thread = [
            threading.Thread(target=self.load_font,args=(name,path,24))
            for name ,path in self.font_resource_path.items()
        ]
        font_36_thread = [
            threading.Thread(target=self.load_font,args=(name,path,36))
            for name,path in self.font_resource_path.items()
        ]
        #启动所有线程
        for thread in img_thread + button_thread + font_24_thread + font_36_thread:
            thread.start()



    def load_font(self,name,path,size:int)->None:
        """
        加载字体
        :param name: 字体名称
        :param path: 字体路径
        :param size: 字体大小
        :return: None
        """
        self.font_dict[name + str(size)] = pygame.font.Font(path, size)
        self.current_progress += 1


    def load_button(self,name:str,path:str) -> None:
        """
        加载按钮资源
        :param name: 按钮名称
        :param path: 按钮的路径
        :return: None
        """
        self.button_dict[name] = [ pygame.image.load(path+rf"\{name}_{i:02d}.png")
                                   for i in range(30)]
        self.current_progress += 1

    def load_img(self,path:str, tar_dic:dict)->None:
        """
        加载图片资源
        :param path:
        :param tar_dic:
        :return:
        """
        all_files = os.listdir(path)
        for file in all_files:
            tar_dic[file[:-4]] = pygame.image.load(path+rf"\{file}")
            self.current_progress += 1





def test():
    loader = ResourceLoader()
    print(loader.img_resource_path)
    print(loader.button_resource_path)
    print(loader.font_resource_path)
    print()
    loader.load_all_resource()
    print(loader.current_progress)


if __name__ == '__main__':
    test()