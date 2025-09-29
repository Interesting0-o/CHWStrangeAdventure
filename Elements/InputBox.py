import pygame
import pygame.freetype

class InputBox:
    def __init__(self,
                 location,
                 size,
                 font,
                 max_length=None,
                 text=''
                 ):
        """

        :param location:
        :param size:
        :param font:
        :param max_length:
        :param text:
        """
        try:
            self.rect = pygame.Rect(location[0], location[1], size[0], size[1])
        except:
            raise ValueError("location 和 size 参数格式错误，请确保它们是元组且长度为 2")
        self.color = (50, 50, 50)
        self.text = text
        self.font = font or pygame.font.Font(None, 32)
        self.max_length = max_length
        self.active = False
        self.cursor_visible = True
        self.last_cursor_blink = pygame.time.get_ticks()  # 上一次光标闪烁的时间
        self.input_box_bg = pygame.Surface((size[0], size[1]))  # 输入框背景图
        self.input_box_bg.fill((255, 255, 255))

        # 中文输入相关属性
        self.composing_text = ""  # 正在输入的文本（用于输入法）
        self.composing_pos = 0  # 输入法文本的插入位置

        # 光标闪烁间隔（毫秒）
        self.cursor_blink_interval = 500

    def handle_event(self, event):
        """
        处理输入框事件, 返回 True 表示事件已被处理
        :param event:
        :return:
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 点击输入框激活
            self.active = self.rect.collidepoint(event.pos)
            return False

        if not self.active:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                # 处理退格键
                if self.composing_text:
                    # 如果有正在输入的文本，先清空
                    self.composing_text = ""
                elif self.text:
                    # 删除最后一个字符（考虑UTF-8字符）
                    self.text = self.text[:-1]
                return True

            elif event.key == pygame.K_RETURN:
                # 回车键确认输入
                if self.composing_text:
                    self.text += self.composing_text
                    self.composing_text = ""
                self.active = False
                return True

        elif event.type == pygame.TEXTEDITING:
            # 处理输入法编辑事件（正在输入但未确认）
            self.composing_text = event.text
            self.composing_pos = event.start
            return True

        elif event.type == pygame.TEXTINPUT:
            # 处理文本输入事件（输入已确认）
            if self.max_length is None or len(self.text) + len(event.text) <= self.max_length:
                self.text += event.text
            self.composing_text = ""  # 清空正在输入的文本
            return True

        return False

    def update(self):
        # 更新光标闪烁
        current_time = pygame.time.get_ticks()
        if current_time - self.last_cursor_blink > self.cursor_blink_interval:
            self.cursor_visible = not self.cursor_visible
            self.last_cursor_blink = current_time

    def draw(self, bg_surface):
        # 绘制输入框背景
        bg_surface.blit(self.input_box_bg, (self.rect.x, self.rect.y))

        # 绘制边框
        border_color = (0, 120, 215) if self.active else (200, 200, 200)
        pygame.draw.rect(bg_surface, border_color, self.rect, 2,border_radius=10)

        # 准备要显示的文本
        display_text = self.text + self.composing_text

        # 渲染文本
        text_surface = self.font.render(display_text, True, self.color)

        # 计算文本位置（垂直居中）
        text_rect = text_surface.get_rect()
        text_rect.midleft = (self.rect.x + 5, self.rect.centery)

        # 绘制文本
        bg_surface.blit(text_surface, text_rect)

        # 如果输入框激活，绘制光标
        if self.active and self.cursor_visible:
            # 计算光标位置
            if self.composing_text:
                # 如果有正在输入的文本，光标在已确认文本之后
                confirmed_text = self.font.render(self.text, True, self.color)
                cursor_x = text_rect.left + confirmed_text.get_width()
            else:
                # 否则光标在全部文本之后
                cursor_x = text_rect.right

            cursor_rect = pygame.Rect(cursor_x, self.rect.y + 5, 2, self.rect.height - 10)
            pygame.draw.rect(bg_surface, self.color, cursor_rect)

            # 如果有正在输入的文本，用下划线标记
            if self.composing_text:
                composing_surface = self.font.render(self.composing_text, True, (255, 0, 0))  # 红色显示正在输入的文本
                composing_rect = composing_surface.get_rect()
                composing_rect.midleft = (cursor_x, self.rect.centery)
                bg_surface.blit(composing_surface, composing_rect)

                # 绘制下划线
                underline_y = composing_rect.bottom + 2
                pygame.draw.line(bg_surface, (255, 0, 0),
                                 (composing_rect.left, underline_y),
                                 (composing_rect.right, underline_y), 1)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("输入框测试 - 支持中文输入")
    clock = pygame.time.Clock()

    # 创建输入框
    input_box = InputBox(
        location=(100, 100),
        size=(400, 40),
        max_length=20,
        font =pygame.font.Font(r"E:\code\GameDemo\resource\font\MiSans\MiSans-Demibold.ttf", 24)
    )

    # 提示文本
    font = pygame.font.Font(r"E:\code\GameDemo\resource\font\MiSans\MiSans-Demibold.ttf", 24)
    hint_text = "点击输入框开始输入，支持中文输入法"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 处理输入框事件
            input_box.handle_event(event)
            # 按ESC键退出
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # 更新输入框状态
        input_box.update()
        # 绘制
        screen.fill((240, 240, 240))
        # 绘制提示文本
        hint_surface = font.render(hint_text, True, (100, 100, 100))
        screen.blit(hint_surface, (100, 60))
        # 绘制输入框
        input_box.draw(screen)
        # 显示当前输入的文本
        text_display = font.render(f"已输入: {input_box.text}", True, (0, 0, 0))
        screen.blit(text_display, (100, 160))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()