import pygame
import os
from enum import Enum


STARTING_GOLD = 2000
SPAWN_DELAY = 5
UNIT_COST = 40
BUILDING_COST = 300
UNIT_TYPE_CHANGE_COST = 250
DIRECTION_CHANGE_COST = 50
HOME_GOLD_PRODUCTION = 10
MINE_GOLD_PRODUCTION = 5

NODE_SIZE = 50
BG_WIDTH = 1000
BG_HEIGHT = 1000

DIFFUSION_CYCLES = 1
EMPTY_OWNED_NODE_VALUE = 500
BUILDING_NODE_VALUE = 800
HOME_NODE_VALUE = 1000
UNIT_VALUE = 1000
NEUTRAL_L = 1.0
SAME_UNIT_L = 0.5
COUNTER_UNIT_L = 0.0
ANTI_COUNTER_UNIT_L = 1.0
EMPTY_D = 0.1
NODE_D = 0.25
UNIT_NO_PREF_DIR_D = 0.25
UNIT_TO_PREF_DIR_D = 0.4
UNIT_FROM_PREF_DIR_D = 0.0


class OrderedEnum(Enum):
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


class Direction(OrderedEnum):
    ERROR = -1
    NONE = 0
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4
    MAX = 4


class BuildingType(Enum):
    ERROR = -1
    EMPTY = 0
    HOME = 1
    MINE = 2
    BARRACKS = 3
    MAX = 3


class UnitType(Enum):
    ERROR = -1
    EMPTY = 0
    PIKEMAN = 1
    ARCHER = 2
    KNIGHT = 3
    MAX = 3

    @classmethod
    def get_next(cls, unit_type):
        if unit_type is UnitType.PIKEMAN:
            return UnitType.ARCHER
        if unit_type is UnitType.ARCHER:
            return UnitType.KNIGHT
        if unit_type is UnitType.KNIGHT:
            return UnitType.PIKEMAN
        return unit_type


class PlayerColor(Enum):
    ERROR = -1
    NEUTRAL = 0
    BLUE = 1
    RED = 2
    MAX = 2


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


class SmartPlayerGoal(Enum):
    UNKNOWN = 0
    USE_IMPROVEMENT = 1
    EXPLORE = 1
    EXPAND_MINES = 2
    EXPAND_BARRACKS = 3
    ATTACK_WITH_UNITS = 4
    DEFEND_WITH_UNITS = 5
    CHANGE_UNIT_TYPE = 6


def load_img(img_name):
    return pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", img_name)))


# Adds the given location to the fight queue and return the fight queue.
# fight_queue: dictionary of PlayerColor to a list of Locations
def add_loc_to_fight_queue(fight_queue, owner, location):
    if not fight_queue.keys().__contains__(owner):
        fight_queue[owner] = []
    fight_queue[owner].append(location)
    return fight_queue


def get_command_from_direction(direction):
    if direction == Direction.NORTH:
        return PlayerCommands.DIRECTION_NORTH
    if direction == Direction.SOUTH:
        return PlayerCommands.DIRECTION_SOUTH
    if direction == Direction.WEST:
        return PlayerCommands.DIRECTION_WEST
    if direction == Direction.EAST:
        return PlayerCommands.DIRECTION_EAST
    return PlayerCommands.ERROR


def get_direction_from_command(command):
    if command == PlayerCommands.DIRECTION_NORTH:
        return Direction.NORTH
    if command == PlayerCommands.DIRECTION_EAST:
        return Direction.EAST
    if command == PlayerCommands.DIRECTION_WEST:
        return Direction.WEST
    if command == PlayerCommands.DIRECTION_SOUTH:
        return Direction.SOUTH
    if command == PlayerCommands.CLEAR_DIRECTION:
        return None
    return Direction.ERROR


def get_command_from_unit_type(unit_type):
    if unit_type is UnitType.PIKEMAN:
        return PlayerCommands.UNIT_PIKEMAN
    if unit_type is UnitType.ARCHER:
        return PlayerCommands.UNIT_ARCHER
    if unit_type is UnitType.KNIGHT:
        return PlayerCommands.UNIT_KNIGHT
    return PlayerCommands.ERROR


def get_counter_unit_type(unit_type):
    return UnitType.get_next(unit_type)


def get_color_for_player(player_color):
    if player_color is PlayerColor.RED:
        return 255, 0, 0
    if player_color is PlayerColor.BLUE:
        return 0, 0, 255
    return 0, 0, 0
