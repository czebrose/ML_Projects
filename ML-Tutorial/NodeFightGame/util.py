import pygame
import os
from enum import Enum


SPAWN_DELAY = 5
UNIT_COST = 10
BUILDING_COST = 300
UNIT_TYPE_CHANGE_COST = 100
DIRECTION_CHANGE_COST = 20
HOME_GOLD_PRODUCTION = 50
MIND_GOLD_PRODUCTION = 30

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


def load_img(img_name):
    return pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", img_name)))


def add_loc_to_fight_queue(fight_queue, owner, location):
    if not fight_queue.keys().__contains__(owner):
        fight_queue[owner] = []
    fight_queue[owner].append(location)
    return fight_queue