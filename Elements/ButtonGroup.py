from Elements.MenuButton import MenuButton
from Elements.Button import Button
import pygame


class ButtonGroup:
    def __init__(self):
        self.__buttons: list[Button|MenuButton] = []


    def add_button(self,*buttons:Button|MenuButton):
        """
        添加按钮到按钮组
        :param buttons:
        :return:
        """
        for button in buttons:
            self.__buttons.append(button)

    def remove_button(self,button:Button|MenuButton):
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

    def is_hover(self,left_top:tuple =(0,0)):
        """
        判断是否在按钮组上
        :param left_top:
        :return:
        """
        for button in self.__buttons:
            if button.is_hover(left_top):
                return True
        return False

    def hover_animation(self,left_top:tuple =(0,0)):
        """
        按钮组上移动画
        :param left_top:
        :return:
        """
        for button in self.__buttons:
            button.hover_animation(left_top)

