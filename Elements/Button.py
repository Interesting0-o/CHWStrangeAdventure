import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self,
                 surface:pygame.Surface,
                 ):
        """
        初始化按钮
        
        参数:
            surface: 按钮的图片
            
        """
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect()
        self.animation_list =[]
        self.index = 0
        self.hover = False
        self.pressed = False
        self.setting_mode = 0


    def is_hovered(self):
        """
        当button直接渲染在screen时
        判断鼠标是否在按钮上
        :return:
        """
        pos =pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.hover = True
            return True
        else:
            self.hover = False
            return False

    def is_hovered_blit(self,left_top:tuple):
        """
        当button需要blit到其他surface上时
        :param left_top:
        :return:
        """
        center_x,center_y =pygame.mouse.get_pos()
        if self.rect.collidepoint((center_x - left_top[0], center_y - left_top[1])):
            self.hover = True
            return True
        else:
            self.hover = False
            return False

    def is_hovered_over_blit(self,left_top:tuple):
        """
        当button需要blit到其他surface上时
        判断鼠标是否在按钮上已经离开
        :param left_top:
        :return:
        """
        center_x, center_y = pygame.mouse.get_pos()
        if self.hover:
            if not self.rect.collidepoint((center_x - left_top[0], center_y - left_top[1])):
                self.hover = False
                return True
            else:
                return False
        else:
            return False


    def is_pressed(self):
        """
        当button直接渲染在screen时
        判断鼠标是否在按钮上按下
        :return:
        """
        mouses_list = pygame.mouse.get_pressed()
        if self.is_hovered() and mouses_list[0]==True and not self.pressed:
            self.pressed = True
            return True
        else:
            self.pressed = False
            return False

    def is_pressed_blit(self,left_top:tuple):
        """
        当button需要blit到其他surface上时
        判断鼠标是否在按钮上按下
        :param left_top:
        :return:
        """
        mouses_list = pygame.mouse.get_pressed()
        if self.is_hovered_blit(left_top) and mouses_list[0]==True and not self.pressed:
            self.pressed = True
            return True
        else:
            self.pressed = False
            return False



    def is_hover_over(self):
        """
        当button直接渲染在screen时
        判断鼠标是否在按钮上已经离开
        :return:
        """
        pos = pygame.mouse.get_pos()
        if self.hover:
            if not  self.rect.collidepoint(pos):
                self.hover = False
                return True
            else:
                return False
        else:
            return False

    def hover_animation_blit(self,left_top:tuple,length:int =28,fps:int = 60):
        """
        当button需要blit到其他surface上时
        :param left_top:
        :param length:
        :return:
        """
        self.is_hovered_blit(left_top)


        if self.hover:
            if self.index < length:
                self.index += int(60/fps)*2
                self.image = self.animation_list[
                    self.index
                ]
        if not self.hover:
            if self.index >0:
                self.index -= int(60/fps)*2
                self.image = self.animation_list[
                    self.index
                ]

    def hover_animation(self,length:int =28,fps:int = 60):


        """
        当button直接渲染在screen时
        :param length:
        :param fps:
        :return:
        """
        self.is_hovered()
        if self.hover:
            if self.index < length:
                self.index += int(60/fps)*2
                self.image = self.animation_list[
                    self.index
                ]
        if not self.hover:
            if self.index >0:
                self.index -= int(60/fps)*2
                self.image = self.animation_list[
                    self.index
                ]
    def setting_button_animation(self,length:int =28,fps:int = 60):
        """
        设置按钮动画,在设置界面使用，当被点击时变为最后一帧效果其余和hover_animation一样
        :param length:
        :param fps:
        :return:

        """
        pass

