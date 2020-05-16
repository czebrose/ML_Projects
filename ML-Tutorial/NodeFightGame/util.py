import pygame
import os
from enum import Enum


SPAWN_DELAY = 5
UNIT_COST = 40
BUILDING_COST = 300
UNIT_TYPE_CHANGE_COST = 1000
DIRECTION_CHANGE_COST = 100
HOME_GOLD_PRODUCTION = 10
MINE_GOLD_PRODUCTION = 5

NODE_WIDTH = 50


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
    NORTH = 0
    SOUTH = 1
    WEST = 2
    EAST = 3
    MAX = 10


class BuildingType(Enum):
    ERROR = -1
    EMPTY = 0
    HOME = 1
    MINE = 2
    BARRACKS = 3


class UnitType(Enum):
    ERROR = -1
    EMPTY = 0
    PIKEMAN = 1
    ARCHER = 2
    KNIGHT = 3


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


def load_img(img_name):
    return pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", img_name)))


def add_loc_to_fight_queue(fight_queue, owner, location):
    if not fight_queue.keys().__contains__(owner):
        fight_queue[owner] = []
    fight_queue[owner].append(location)
    return fight_queue