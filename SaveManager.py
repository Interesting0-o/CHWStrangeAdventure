import datetime
import json
import os
import threading

class SaveManager:

    current_save = None
    init_save = {
        "player": {
            "name": None,
            "honor_value": 0
        },
        "chapter_data": {
            "chapter": "C1",
            "scene": "C1_1",
            "dialog_index": 0,
        },
        "bg": "library"
    }
    path = __file__[:-14]

    @staticmethod
    def get_current_save():
        """
        获取当前保存游戏数据
        :return:
        """
        return SaveManager.current_save

    @staticmethod
    def set_current_save_name(save_name:str):
        """
        设置当前保存游戏名称
        :param save_name:
        :return:
        """
        SaveManager.current_save["player"]["name"] = save_name

    def __init__(self):
        self.save_datas = {} #保存在字典中的存档名称会带有.chw后缀

    def thread_read(self,file):
        """
        用于线程读取保存游戏数据
        :param file:
        :return:
        """
        try:
            with open(self.path+f"save/{file}", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.save_datas[file] = data
        except Exception:
            self.save_datas[file] = "Error"
    #读取保存游戏数据
    def init_save_data(self):
        """
        初始化保存游戏数据
        :return:
        """
        for file in os.listdir(self.path+'save'):
            t = threading.Thread(target=self.thread_read, args=(file,))
            t.start()


    #删除保存游戏数据
    def delete_save_data(self, save_name):
        """
        删除保存游戏数据
        :param save_name:
        :return:
        """
        os.remove(self.path+rf"save\{save_name}.chw")
        self.save_datas.pop(save_name+".chw")
        print(f"删除成功，保存名为{save_name}.chw")

    #保存游戏数据
    def save_save_data(self,data:dict):
        """
        保存游戏数据
        :param data:
        :return:
        """
        current_time = str(datetime.datetime.now().strftime("%m-%d"))
        save_name = data["player"]["name"] + current_time
        with open(self.path+f"save/{save_name}.chw", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        self.save_datas[save_name+".chw"] = data
        return save_name

    #覆盖保存游戏数据
    def cover_save_data(self,data:dict):
        """
        覆盖保存游戏数据
        :param data:
        :return:
        """
        save_name = data["player"]["name"] + str(datetime.datetime.now().strftime("%m-%d"))
        with open(self.path+f"save/{save_name}.chw", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        self.save_datas[save_name] = save_name
        return save_name
        
    #等待所有保存游戏数据读取完成
    def wait_load_finish(self):
        """
        等待所有保存游戏数据读取完成
        :return:
        """
        while len(self.save_datas)!= len(os.listdir(self.path+'save')):
            pass

    #检测读取进度
    def check_load_finish(self):
        """
        检测读取进度
        :return:
        """
        return len(self.save_datas) == len(os.listdir(self.path+'save'))

if __name__ == '__main__':
    save_manager = SaveManager()
    save_manager.init_save_data()