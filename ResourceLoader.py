import pygame
import threading
import os
import json
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
    font_size = [24,36,48]
    font_dict = {}


    #剧情加载

    plot_resource_path = path + r'\plot'
    plot_dict = {}

    characters_resource_path = {
        #角色资源
        "DemoCharacter":path + r'\characters\DemoCharacter',
    }
    demo_character_dict = {}



    #检查所有资源是否加载完毕
    is_load_finish = False

    current_progress = 0


    def __init__(self):
        self.thread_list = []

    def load_all_resource(self)->None:
        """
        加载所有资源
        :return:
        """
        #加载所有的图片资源
        img_thread = [
            threading.Thread(target=self.load_img,args=(path,ResourceLoader.img_dict[name]))
            for name,path in self.img_resource_path.items()
        ]
        #加载所有的按钮资源
        button_thread = [
            threading.Thread(target=self.load_button,args=(name,path))
            for name,path in self.button_resource_path.items()
        ]
        #加载所有的字体资源
        font_24_thread = [
            threading.Thread(target=self.load_font,args=(name,path,24))
            for name ,path in self.font_resource_path.items()
        ]
        font_36_thread = [
            threading.Thread(target=self.load_font,args=(name,path,36))
            for name,path in self.font_resource_path.items()
        ]
        font_48_thread = [
            threading.Thread(target=self.load_font,args=(name,path,48))
            for name,path in self.font_resource_path.items()
        ]
        #加载所有的角色资源
        characters_thread = [
            threading.Thread(target=self.load_img,args=(path,self.demo_character_dict))
            for name,path in self.characters_resource_path.items()
        ]

        #加载剧情资源
        plot_thread = threading.Thread(target=self.load_plot)

        #将所有线程加入列表
        self.thread_list = img_thread + button_thread + font_24_thread + font_36_thread + font_48_thread + characters_thread + [plot_thread]

        #启动所有线程
        for thread in self.thread_list:
            thread.start()

    def load_plot(self)->None:
        """
        加载剧情资源
        :return:
        """
        all_files = os.listdir(self.plot_resource_path)
        for file in all_files:
            with open(self.plot_resource_path + rf"\{file}",'r',encoding='utf-8') as f:
                 ResourceLoader.plot_dict[file[:-5]] = json.load(f)
            self.current_progress += 1

    def load_font(self,name,path,size:int)->None:
        """
        加载字体
        :param name: 字体名称
        :param path: 字体路径
        :param size: 字体大小
        :return: None
        """
        ResourceLoader.font_dict[name + str(size)] = pygame.font.Font(path, size)
        self.current_progress += 1

    def load_button(self,name:str,path:str) -> None:
        """
        加载按钮资源
        :param name: 按钮名称
        :param path: 按钮的路径
        :return: None
        """
        ResourceLoader.button_dict[name] = [ pygame.image.load(path+rf"\{name}_{i:02d}.png")
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


    def wait_load_finish(self)->None:
        for t in self.thread_list:
            t.join()

    def get_progress(self)->float:
        return self.current_progress / 35

    def check_load_finish(self)->bool:
        """
        检查资源是否加载完毕
        :return:
        """
        return self.current_progress ==37





def test():
    loader = ResourceLoader()
    loader.load_all_resource()
    # while loader.get_progress() !=1:
    #     print(loader.get_progress())
    print(loader.check_load_finish())
    loader.wait_load_finish()
    print(loader.current_progress)
    print(loader.bg_dict["DialogBG"])
    print(loader.check_load_finish())


if __name__ == '__main__':
    test()