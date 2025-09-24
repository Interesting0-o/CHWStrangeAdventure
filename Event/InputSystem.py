from .EventBus import EventBus
from typing import List
import pygame as pg

class InputSystem:
    # 这个函数用于处理用户的输入
    def __init__(self, event_bus: EventBus):
        self.bus = event_bus
        self.map = {
            pg.KEYDOWN:{
                pg.K_SPACE: "input.jump",
                pg.K_RETURN: "input.confirm",# return按键就是回车键
                pg.K_ESCAPE: "input.back",
                pg.K_a: "input.left",
                pg.K_d: "input.right",
                pg.K_w: "input.up",
                pg.K_s: "input.down",
            },
            pg.KEYUP:{
                pg.K_a: "input.left_up",
                pg.K_d: "input.right_up",
                pg.K_w: "input.up_up",
                pg.K_s: "input.down_up",
            }
        }

    def update(self, event: List[pg.event.Event]):
        for e in event:# 遍历所有事件
            if e.type in self.map:# 如果事件类型在映射表中
                topic = self.map[e.type].get(e.key)# 找到对应的事件
                if topic:# 如果有对应的事件
                    self.bus.emit(topic, e)# 就使用事件总线发布事件