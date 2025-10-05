import datetime
import json
import os
import pygame
import threading

class SaveManager:

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

    def __init__(self):
        self.save_datas = {}

    def thread_read(self,file):
        try:
            with open(self.path+f"save/{file}", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.save_datas[file] = data
        except Exception as e:
            self.save_datas[file] = "Error"

    def init_save_data(self):
        for file in os.listdir(self.path+'save'):
            t = threading.Thread(target=self.thread_read, args=(file,))
            t.start()

    def delete_save_data(self, save_name):
        os.remove(self.path+f"save/{self.save_datas[save_name]}.chw")
        self.save_datas.pop(save_name)


    def save_save_data(self,data:dict):
        current_time = str(datetime.datetime.now().strftime("%Y-%m-%d"))
        save_name = data["player"]["name"] + current_time
        with open(self.path+f"save/{save_name}.chw", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        self.save_datas[save_name] = save_name
        return save_name

    def auto_save(self,data:dict):
        current_time = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        save_name = data["player"]["name"] + current_time + "(自动保存)"
        with open(self.path+f"save/{save_name}.chw", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        self.save_datas[save_name] = save_name
        return save_name

if __name__ == '__main__':
    save_manager = SaveManager()
    save_manager.init_save_data()