import util
from util import Direction
import pygame
from enum import Enum
import abc
from abc import ABC
from building import BuildingType, Building
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
        node = self.highlight_node
        if command is PlayerCommands.DIRECTION_EAST:
            self.execute_direction_change(node, Direction.EAST)
        elif command is PlayerCommands.DIRECTION_WEST:
            self.execute_direction_change(node, Direction.WEST)
        elif command is PlayerCommands.DIRECTION_NORTH:
            self.execute_direction_change(node, Direction.NORTH)
        elif command is PlayerCommands.DIRECTION_SOUTH:
            self.execute_direction_change(node, Direction.SOUTH)
        elif command is PlayerCommands.CLEAR_DIRECTION:
            self.execute_direction_change(node, None)
        elif command is PlayerCommands.BUILD_BARRACKS:
            self.execute_build_building(node, BuildingType.BARRACKS)
        elif command is PlayerCommands.BUILD_MINE:
            self.execute_build_building(node, BuildingType.MINE)

    def execute_direction_change(self, node, direction):
        if node and node.exit_direction[self.color] is not direction and self.gold >= util.DIRECTION_CHANGE_COST:
            node.exit_direction[self.color] = direction
            self.gold -= util.DIRECTION_CHANGE_COST

    def execute_build_building(self, node, building_type):
        if node and node.owner is self.color:
            if node.building and node.building.type is building_type:
                return
            if self.gold >= util.BUILDING_COST:
                node.building = Building(building_type)
                self.gold -= util.BUILDING_COST

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
