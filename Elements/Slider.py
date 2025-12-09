import pygame


class Slider:

    def __init__(self,
                 x, y,
                 length, height,
                 min_val=0, max_val=100,
                 initial_val=50,
                 continuous=True,
                 feet=None,
                 ball_color:int|tuple[int, int, int]|str=0x0000ff,
                 track_color:int|tuple[int, int, int]|str=0xff0000,
                 border_color:int|tuple[int, int, int]|str=(50, 50, 50),
                 border=2,
                 location=(0, 0)
                 ):
        """
        初始化滑块

        参数:
            x, y: 滑块中心位置
            length: 滑条长度（不包含圆角部分）
            height: 滑条高度（不包含描边）
            min_val: 最小值
            max_val: 最大值
            initial_val: 初始值
            continuous: 是否为连续滑块 (True) 还是分立滑块 (False)
            feet: 步长（仅用于分立滑块）
            ball_color: 滑块按钮颜色
            track_color: 滑条轨道颜色
            border_color: 滑条描边颜色
            border: 滑条描边宽度
            location: bg_surface的左上角坐标
        """
        if not continuous and feet is not None and length % feet != 0:
            raise ValueError("滑块长度必须为步长的整数倍")

        self.x = x
        self.y = y
        self.length = length
        self.height = height
        self.min_val = min_val
        self.max_val = max_val
        self.continuous = continuous
        self.feet = feet
        self.ball_color = ball_color
        self.track_color = track_color
        self.border_color = border_color
        self.border = border
        self.location = location

        # 用于分立滑块的步数
        if not continuous and feet is not None:
            self.num_steps = (max_val - min_val) // feet

        # 拖拽状态
        self.dragging = False

        # 创建滑条轨道
        self.img = pygame.Surface((self.length + 2 * self.border, self.height + 2 * self.border), pygame.SRCALPHA)
        self.img_rect = self.img.get_rect(center=(self.x, self.y))

        # 绘制滑条轨道背景
        pygame.draw.rect(self.img,
                         color=self.track_color,
                         rect=(0, 0, self.length + 2 * self.border, self.height + 2 * self.border),
                         border_radius=(self.height // 2 + self.border)
                         )
        # 绘制滑条的描边
        pygame.draw.rect(self.img,
                         color=self.border_color,
                         rect=(0, 0, self.length + 2 * self.border, self.height + 2 * self.border),
                         border_radius=(self.height // 2 + self.border),
                         width=self.border
                         )

        # 创建小球
        ball_radius = self.height // 2
        self.ball_img = pygame.Surface((ball_radius * 2, ball_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.ball_img, self.ball_color, (ball_radius, ball_radius), ball_radius)

        # 计算滑块可移动的范围（相对于滑条轨道）
        self.start_pos = self.border + ball_radius
        self.end_pos = self.length + 2 * self.border - ball_radius

        # 设置初始值
        self.value = initial_val
        self.update_ball_position_from_value()

    def get_value(self):
        """
        获取当前值
        :return: 当前滑块的值
        """
        return self.value

    def update_ball_position_from_value(self):
        """
        根据当前值更新滑块按钮位置
        """
        # 计算值在[min_val, max_val]范围内的比例
        value_ratio = (self.value - self.min_val) / (self.max_val - self.min_val)

        # 计算小球在滑条上的位置
        ball_x = self.start_pos + value_ratio * (self.end_pos - self.start_pos)

        # 更新小球位置
        ball_center_x = self.img_rect.x + ball_x
        self.ball_img_rect = self.ball_img.get_rect(center=(ball_center_x, self.y))

    def set_value_from_position(self, mouse_x):
        """
        根据鼠标位置设置值
        :param mouse_x: 鼠标的x坐标
        """
        # 将鼠标位置转换为相对于滑条轨道的x坐标
        rel_x = mouse_x - self.img_rect.x

        # 限制在滑条范围内
        rel_x = max(min(rel_x, self.end_pos), self.start_pos)

        # 计算位置比例
        pos_ratio = (rel_x - self.start_pos) / (self.end_pos - self.start_pos)

        if self.continuous:
            # 连续滑块：直接根据比例计算值
            self.value = self.min_val + pos_ratio * (self.max_val - self.min_val)
        else:
            # 分立滑块：根据步长计算值
            step = round(pos_ratio * self.num_steps)
            self.value = self.min_val + step * self.feet

        # 更新小球位置
        self.update_ball_position_from_value()

    def handle_event(self, event):
        """
        处理事件
        :param event: pygame事件
        :return: 如果值发生变化返回True，否则返回False
        """
        value_changed = False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x -= self.location[0]
        mouse_y -= self.location[1]

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 检查是否点击了小球
            if self.ball_img_rect.collidepoint((mouse_x, mouse_y)):
                self.dragging = True
                value_changed = True
            # 检查是否点击了滑条轨道
            elif self.img_rect.collidepoint((mouse_x, mouse_y)):
                self.dragging = True
                self.set_value_from_position(mouse_x)
                value_changed = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                self.dragging = False
                value_changed = True

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.set_value_from_position(mouse_x)
                value_changed = True

        return value_changed

    def draw(self, bg_surface):
        """
        绘制滑块到指定表面
        :param bg_surface: 目标表面
        """
        # 绘制滑条轨道
        bg_surface.blit(self.img, self.img_rect)

        # 绘制小球
        bg_surface.blit(self.ball_img, self.ball_img_rect)


def test():
    """测试函数"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    pygame.display.set_caption("滑块测试")

    # 创建连续滑块
    continuous_slider = Slider(
        400, 200,
        300, 20,
        min_val=0, max_val=100,
        initial_val=50,
        continuous=True,
        ball_color=(0, 100, 255),
        track_color=(200, 200, 200)
    )

    # 创建分立滑块
    discrete_slider = Slider(
        400, 300,
        300, 20,
        min_val=0, max_val=100,
        initial_val=0,
        continuous=False,
        feet=20,
        ball_color=(255, 100, 0),
        track_color=(200, 200, 200)
    )

    # 创建字体用于显示值
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 处理滑块事件
            continuous_changed = continuous_slider.handle_event(event)
            discrete_changed = discrete_slider.handle_event(event)

            if continuous_changed or discrete_changed:
                # 值发生变化时可以在这里添加处理逻辑
                pass

        screen.fill((240, 240, 240))

        # 绘制滑块
        continuous_slider.draw(screen)
        discrete_slider.draw(screen)

        # 显示滑块值
        cont_text = font.render(f"连续滑块值: {continuous_slider.get_value():.1f}", True, (0, 0, 0))
        disc_text = font.render(f"分立滑块值: {discrete_slider.get_value()}", True, (0, 0, 0))
        screen.blit(cont_text, (400 - cont_text.get_width() // 2, 150))
        screen.blit(disc_text, (400 - disc_text.get_width() // 2, 250))

        # 显示说明文字
        info_font = pygame.font.Font(None, 24)
        info_text = info_font.render("点击并拖动小球或滑条来调整值", True, (100, 100, 100))
        screen.blit(info_text, (400 - info_text.get_width() // 2, 350))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    test()