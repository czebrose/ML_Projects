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
        self.gold = util.STARTING_GOLD
        self.unit_pref = UnitType.PIKEMAN

    def check_input(self, global_map):
        self.highlight_node = self.get_highlight_node(global_map)
        command = self.get_command(global_map)
        self.execute_command(command)

        target = None
        if self.highlight_node:
            target = (self.highlight_node.x, self.highlight_node.y)
        thought = str(self.color) + "\t" + str(target) + "\t" + str(command) + "\t\t"
        return global_map, thought

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

    # Returns the text rect for the given text.
    # text: The text which we're getting the rect for
    # top: The position of the top of that rect
    def get_text_rect(self, win, text, top):
        text_rect = text.get_rect()
        text_rect.top = top
        if self.color is PlayerColor.RED:
            text_rect.right = win.get_width()
        elif self.color is PlayerColor.BLUE:
            text_rect.left = 0
        return text_rect

    def draw(self, win):
        if self.highlight_node:
            x = self.highlight_node.x * util.NODE_SIZE
            y = self.highlight_node.y * util.NODE_SIZE
            if self.color == PlayerColor.BLUE:
                win.blit(NODE_HIGHLIGHT_BLUE_IMG, (x, y))
            elif self.color == PlayerColor.RED:
                win.blit(NODE_HIGHLIGHT_RED_IMG, (x, y))
        color = util.get_color_for_player(self.color)
        text = STAT_FONT.render("Gold: " + str(self.gold), True, color)
        text_rect = self.get_text_rect(win, text, 0)
        win.blit(text, text_rect)
        text = STAT_FONT.render("Unit: " + str(self.unit_pref), True, color)
        text_rect = self.get_text_rect(win, text, util.NODE_SIZE)
        win.blit(text, text_rect)
