import util
from util import Direction
import pygame
from enum import Enum
import abc
from abc import ABC
pygame.font.init()


NODE_HIGHLIGHT_RED_IMG = util.load_img("node_highlight_red.png")
NODE_HIGHLIGHT_BLUE_IMG = util.load_img("node_highlight_blue.png")

STAT_FONT = pygame.font.SysFont("comicsans", 50)


class PlayerColor(Enum):
    ERROR = -1
    NEUTRAL = 0
    BLUE = 1
    RED = 2


class PlayerCommands(Enum):
    ERROR = -1
    CLEAR_DIRECTION = 0
    DIRECTION_NORTH = 1
    DIRECTION_SOUTH = 2
    DIRECTION_EAST = 3
    DIRECTION_WEST = 4
    BUILD_MINE = 5
    BUILD_BARRACKS = 6
    UNIT_PIKEMAN = 7
    UNIT_ARCHER = 8
    UNIT_KNIGHT = 9


class PlayerInput(ABC):
    def __init__(self, color):
        self.color = color
        self.highlight_node = None
        self.gold = 0

    def check_input(self, global_map):
        self.highlight_node = self.get_highlight_node(global_map)
        command = self.get_command(global_map)
        self.execute_command(command)
        return global_map

    @abc.abstractmethod
    def get_highlight_node(self, global_map) -> object:
        return None

    @abc.abstractmethod
    def get_command(self, global_map) -> object:
        return None

    def execute_command(self, command):
        loc = self.highlight_node
        if command is PlayerCommands.DIRECTION_EAST:
            self.execute_direction_change(loc, Direction.EAST)
        elif command is PlayerCommands.DIRECTION_WEST:
            self.execute_direction_change(loc, Direction.WEST)
        elif command is PlayerCommands.DIRECTION_NORTH:
            self.execute_direction_change(loc, Direction.NORTH)
        elif command is PlayerCommands.DIRECTION_SOUTH:
            self.execute_direction_change(loc, Direction.SOUTH)
        elif command is PlayerCommands.CLEAR_DIRECTION:
            self.execute_direction_change(loc, None)

    def execute_direction_change(self, loc, direction):
        if loc and loc.exit_direction[self.color] is not direction and self.gold >= util.DIRECTION_CHANGE_COST:
            loc.exit_direction[self.color] = direction
            self.gold -= util.DIRECTION_CHANGE_COST

    def draw(self, win):
        if self.highlight_node:
            x = self.highlight_node.x * util.NODE_WIDTH
            y = self.highlight_node.y * util.NODE_WIDTH
            if self.color == PlayerColor.BLUE:
                win.blit(NODE_HIGHLIGHT_BLUE_IMG, (x, y))
            elif self.color == PlayerColor.RED:
                win.blit(NODE_HIGHLIGHT_RED_IMG, (x, y))
        if self.color is PlayerColor.RED:
            x = util.NODE_WIDTH
            y = 2 * util.NODE_WIDTH
            color = (255, 0, 0)
            text = STAT_FONT.render("Gold: " + str(self.gold), 1, color)
            win.blit(text, (x, y))
        if self.color is PlayerColor.BLUE:
            x = util.NODE_WIDTH
            y = util.NODE_WIDTH
            color = (0, 0, 255)
            text = STAT_FONT.render("Gold: " + str(self.gold), 1, color)
            win.blit(text, (x, y))
