import util
import pygame
from enum import Enum


NODE_HIGHLIGHT_RED_IMG = util.load_img("node_highlight_red.png")
NODE_HIGHLIGHT_BLUE_IMG = util.load_img("node_highlight_blue.png")


class PlayerColor(Enum):
    ERROR = -1
    NEUTRAL = 0
    BLUE = 1
    RED = 2


class PlayerInput:
    def __init__(self, color):
        self.color = color
        self.highlight_node = None
        self.gold = 0

    def check_input(self, global_map):
        (button1, button2, button3) = pygame.mouse.get_pressed()
        if button1:
            (x, y) = pygame.mouse.get_pos()
            print(str(x) + "," + str(y))
            for col in global_map:
                for loc in col:
                    if loc is not None and loc.check_click(x, y):
                        self.highlight_node = loc
        return global_map

    def draw(self, win):
        if self.highlight_node:
            x = self.highlight_node.x * util.NODE_WIDTH
            y = self.highlight_node.y * util.NODE_WIDTH
            if self.color == PlayerColor.BLUE:
                win.blit(NODE_HIGHLIGHT_BLUE_IMG, (x, y))
            elif self.color == PlayerColor.RED:
                win.blit(NODE_HIGHLIGHT_RED_IMG, (x, y))
