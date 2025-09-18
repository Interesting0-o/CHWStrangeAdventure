import pygame

class CircularSlider(pygame.sprite.Sprite):
    def __init__(self,
                  x, y,
                    track_length, track_height, 
                    min_val=0, max_val=100, 
                    initial_val=50, 
                    continuous=True, 
                    knob_color=(200, 200, 200), 
                    track_color=(100, 100, 100), 
                    track_border_color=(50, 50, 50), 
                    track_border_width=2
                    ):
        """
        初始化圆形滑块
        
        参数:
            x, y: 滑块中心位置
            track_length: 滑条长度
            track_height: 滑条高度
            min_val: 最小值
            max_val: 最大值
            initial_val: 初始值
            continuous: 是否为连续滑块 (True) 还是分立滑块 (False)
            knob_color: 滑块按钮颜色
            track_color: 滑条轨道颜色
            track_border_color: 滑条描边颜色
            track_border_width: 滑条描边宽度
        """
        super().__init__()
        
        # 公共成员变量，可供外部访问
        self.value = initial_val       # 当前值
        self.min_val = min_val         # 最小值
        self.max_val = max_val         # 最大值
        self.continuous = continuous   # 是否连续
        
        # 滑块位置和尺寸
        self.x = x
        self.y = y
        self.track_length = track_length
        self.track_height = track_height
        
        # 滑块颜色
        self.knob_color = knob_color
        self.track_color = track_color
        self.track_border_color = track_border_color
        self.track_border_width = track_border_width
        
        # 计算滑条圆角半径（等于高度的一半）
        self.corner_radius = track_height // 2
        
        # 计算总宽度（滑条长度 + 滑块直径）
        self.total_width = track_length + track_height
        self.total_height = track_height
        
        # 创建滑块的表面和矩形区域
        self.image = pygame.Surface((self.total_width, self.total_height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.dragging = False
        
        # 初始化滑块位置
        self.update_knob_position()
        
    def update_knob_position(self):
        """根据当前值更新滑块按钮位置"""
        # 计算滑块按钮在滑条上的位置 (0.0 到 1.0)
        position_ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        
        # 计算滑块按钮的实际坐标（相对于滑块表面）
        self.knob_x = int(position_ratio * self.track_length) + self.track_height // 2
        self.knob_y = self.total_height // 2
        
        # 滑块按钮半径 (使用高度的一半)
        self.knob_radius = self.track_height // 2
        
    def draw(self, surface):
        """绘制滑块到指定表面"""
        # 清空图像
        self.image.fill((0, 0, 0, 0))
        
        # 绘制滑条轨道 (圆角矩形)
        track_rect = pygame.Rect(
            self.track_height // 2, 
            (self.total_height - self.track_height) // 2,
            self.track_length,
            self.track_height
        )
        
        # 绘制滑条背景
        pygame.draw.rect(self.image, self.track_color, track_rect, border_radius=self.corner_radius)
        
        # 绘制滑条描边
        if self.track_border_width > 0:
            pygame.draw.rect(
                self.image, 
                self.track_border_color, 
                track_rect, 
                width=self.track_border_width,
                border_radius=self.corner_radius
            )
        
        # 绘制滑块按钮 (圆形)
        pygame.draw.circle(self.image, self.knob_color, (self.knob_x, self.knob_y), self.knob_radius)
        
        # 绘制滑块按钮描边
        pygame.draw.circle(
            self.image, 
            self.track_border_color, 
            (self.knob_x, self.knob_y), 
            self.knob_radius,
            width=1
        )
        
        # 将滑块绘制到指定表面
        surface.blit(self.image, self.rect)
        
    def handle_event(self, event):
        """处理事件并更新滑块状态"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 检查鼠标是否点击在滑块按钮上
            mouse_x, mouse_y = event.pos
            knob_screen_x = self.rect.x + self.knob_x
            knob_screen_y = self.rect.y + self.knob_y
            
            distance = ((mouse_x - knob_screen_x) ** 2 + (mouse_y - knob_screen_y) ** 2) ** 0.5
            
            if distance <= self.knob_radius:
                self.dragging = True
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
            
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # 更新滑块值基于鼠标位置
            mouse_x, _ = event.pos
            
            # 限制鼠标位置在滑条范围内
            track_start_x = self.rect.x + self.track_height // 2
            track_end_x = track_start_x + self.track_length
            mouse_x = max(track_start_x, min(mouse_x, track_end_x))
            
            # 计算新值
            position_ratio = (mouse_x - track_start_x) / self.track_length
            new_value = self.min_val + position_ratio * (self.max_val - self.min_val)
            
            # 如果是分立滑块，四舍五入到最接近的整数
            if not self.continuous:
                new_value = round(new_value)
                
            # 更新值并确保在范围内
            self.value = max(self.min_val, min(new_value, self.max_val))
            
            # 更新滑块位置
            self.update_knob_position()
            
            return True  # 表示值已更改
            
        return False  # 表示值未更改
    
    def get_value(self):
        """获取当前滑块值"""
        return self.value
    
    def set_value(self, value):
        """设置滑块值"""
        self.value = max(self.min_val, min(value, self.max_val))
        self.update_knob_position()


if __name__ == '__main__':
    import pygame
    import sys

    # 初始化pygame
    pygame.init()

    # 设置窗口
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("增强版圆形滑块示例")

    # 创建滑块实例
    slider = CircularSlider(
        x=400, 
        y=300, 
        track_length=300, 
        track_height=20, 
        min_val=0, 
        max_val=100, 
        initial_val=50,
        continuous=True,
        knob_color=(255, 100, 100),
        track_color=(200, 200, 200),
        track_border_color=(80, 80, 80),
        track_border_width=2
    )

    # 主循环
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # 处理滑块事件
            slider.handle_event(event)
        
        # 清空屏幕
        screen.fill((240, 240, 240))
        
        # 绘制滑块
        slider.draw(screen)
        
        # 显示当前值
        value_text = font.render(f"值: {slider.get_value():.1f}", True, (0, 0, 0))
        screen.blit(value_text, (350, 250))
        
        # 显示滑条尺寸
        size_text = font.render(f"滑条尺寸: {slider.track_length}x{slider.track_height}", True, (0, 0, 0))
        screen.blit(size_text, (320, 200))
        
        # 更新显示
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()




