import util
from util import Direction
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
        if (button1 and self.color is PlayerColor.BLUE)\
                or (button3 and self.color is PlayerColor.RED):
            (x, y) = pygame.mouse.get_pos()
            print(str(x) + "," + str(y))
            for col in global_map:
                for loc in col:
                    if loc is not None and loc.check_click(x, y):
                        self.highlight_node = loc
        if self.highlight_node:
            keys = pygame.key.get_pressed()
            if self.color == PlayerColor.BLUE:
                if keys[pygame.K_LEFT]:
                    self.highlight_node.exit_direction[self.color] = Direction.WEST
                elif keys[pygame.K_RIGHT]:
                    self.highlight_node.exit_direction[self.color] = Direction.EAST
                elif keys[pygame.K_UP]:
                    self.highlight_node.exit_direction[self.color] = Direction.NORTH
                elif keys[pygame.K_DOWN]:
                    self.highlight_node.exit_direction[self.color] = Direction.SOUTH
                elif keys[pygame.K_KP0]:
                    self.highlight_node.exit_direction[self.color] = None
            elif self.color == PlayerColor.RED:
                pass

        return global_map

    def draw(self, win):
        if self.highlight_node:
            x = self.highlight_node.x * util.NODE_WIDTH
            y = self.highlight_node.y * util.NODE_WIDTH
            if self.color == PlayerColor.BLUE:
                win.blit(NODE_HIGHLIGHT_BLUE_IMG, (x, y))
            elif self.color == PlayerColor.RED:
                win.blit(NODE_HIGHLIGHT_RED_IMG, (x, y))
