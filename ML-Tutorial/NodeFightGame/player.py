import util
from util import Direction, BuildingType, PlayerCommands, PlayerColor, UnitType
import pygame
import abc
from abc import ABC
from building import Building
pygame.font.init()


NODE_HIGHLIGHT_RED_IMG = util.load_img("node_highlight_red.png")
NODE_HIGHLIGHT_BLUE_IMG = util.load_img("node_highlight_blue.png")

STAT_FONT = pygame.font.SysFont("comicsans", 50)


class PlayerInput(ABC):
    def __init__(self, color):
        self.color = color
        self.highlight_node = None
        self.gold = 2000
        self.unit_pref = UnitType.PIKEMAN

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
        elif command is PlayerCommands.UNIT_ARCHER:
            self.execute_unit_change(node, UnitType.ARCHER)
        elif command is PlayerCommands.UNIT_KNIGHT:
            self.execute_unit_change(node, UnitType.KNIGHT)
        elif command is PlayerCommands.UNIT_PIKEMAN:
            self.execute_unit_change(node, UnitType.PIKEMAN)

    def execute_direction_change(self, node, direction):
        if node and node.get_direction(self.color) is not direction and self.gold >= util.DIRECTION_CHANGE_COST:
            node.set_exit_direction(self.color, direction)
            self.gold -= util.DIRECTION_CHANGE_COST

    def execute_build_building(self, node, building_type):
        if node and node.owner is self.color:
            if node.building and node.building.type is building_type:
                return
            if self.gold >= util.BUILDING_COST:
                node.building = Building(building_type, self.unit_pref)
                self.gold -= util.BUILDING_COST
                self.unit_pref = UnitType.get_next(self.unit_pref)

    def execute_unit_change(self, node, unit_type):
        if node and node.owner is self.color:
            if node.building and node.building.unit_type is not unit_type and self.gold >= util.UNIT_TYPE_CHANGE_COST:
                node.building.unit_type = unit_type
                self.gold -= util.UNIT_TYPE_CHANGE_COST

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
