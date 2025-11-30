import pygame

class Button:
    def __init__(self,
                 surface_list:list[pygame.Surface],
                 ):
        """
        初始化按钮
        参数:
            surface: 按钮的图片列表
        """
        self.image = surface_list[0]
        self.rect = self.image.get_rect()
        self.animation_list =surface_list
        self.index = 0
        self.setting_mode = 0
        self.value = False


    def is_hover(self,left_top:tuple =(0,0)):
        """
        判断鼠标是否在按钮上
        :param left_top:
        :return:
        """
        center_x,center_y =pygame.mouse.get_pos()
        return True if self.rect.collidepoint((center_x - left_top[0], center_y - left_top[1])) else False

    def is_press(self,left_top:tuple=(0,0)):
        """
        判断鼠标是否在按钮上按下
        :param left_top:
        :return:
        """
        mouses_list = pygame.mouse.get_pressed()
        return True if self.is_hover(left_top) and mouses_list[0] else False

    def hover_animation(self,left_top:tuple=(0,0),length:int =28,fps:int = 60):
        """
        当button需要blit到其他surface上时
        :param left_top:
        :param length:
        :param fps:
        :return:
        """
        self.is_hover(left_top)
        if self.is_hover(left_top) and self.index < length:
            self.index += int(60/fps)*2
            self.image = self.animation_list[self.index]
        if not self.is_hover(left_top) and self.index >0:
            self.index -= int(60/fps)*2
            self.image = self.animation_list[self.index]

    def setting_button_animation(self,
                                 mouse_down:bool,
                                 length:int =28,
                                 left_top:tuple = (0,0),
                                 fps:int = 60):
        """
        设置按钮动画,在设置界面使用，当被点击时变为最后一帧效果其余和hover_animation一样
        :param mouse_down: event中的鼠标按下事件
        :param length:
        :param left_top:
        :param fps:
        :return:
        """

        self.is_hover(left_top)
        if self.is_hover(left_top) or self.setting_mode==1:
            if self.index < length:
                self.index += int(60 / fps) * 2
                self.image = self.animation_list[self.index]
        elif not self.is_hover(left_top):
            if self.index > 0:
                self.index -= int(60 / fps) * 2
                self.image = self.animation_list[self.index]


    def is_press_down(self,
                        event:pygame.event.Event,
                        left_top:tuple = (0,0)
                        ):
        """
        当button直接渲染在screen时
        :param event:
        :param left_top:
        :return:
        """
        return True if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hover(left_top) else False

    def draw(self,bg_surface:pygame.Surface):
        bg_surface.blit(self.image,self.rect)

def test():
    from ResourceLoader import ResourceLoader
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    loader = ResourceLoader()
    loader.load_all_resource()
    loader.wait_load_finish()


    button = Button(loader.button_dict['start_button'])

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if button.is_press_down(event):
                print('start')

        screen.blit(button.image, button.rect)
        button.hover_animation()
        pygame.display.update()


if __name__ == '__main__':
    test()

