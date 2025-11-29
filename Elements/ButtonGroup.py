from typing import List
from Elements.Button import Button
import pygame


class ButtonGroup:
    def __init__(self):
        self.__buttons: List[Button] = []


    def add_button(self,button:Button):
        """
        添加按钮到按钮组
        :param button:
        :return:
        """
        self.__buttons.append(button)

    def remove_button(self,button:Button):
        """
        移除按钮
        :param button:
        :return:
        """
        self.__buttons.remove(button)

    def remove_button_by_index(self,index:int):
        """
        移除按钮
        :param index:
        :return:
        """
        self.__buttons.pop(index)

    def get_button_by_index(self,index:int):
        """
        获取按钮
        :param index:
        :return:
        """
        return self.__buttons[index]

    def draw(self,surface:pygame.Surface):
        """
        绘制按钮组
        :param surface:
        :return:
        """
        for button in self.__buttons:
            button.draw(surface)
