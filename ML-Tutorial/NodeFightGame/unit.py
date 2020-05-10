import pygame
import util
from enum import Enum
from player import Player


BLUE_PIKEMAN_UNIT_IMG = util.load_img("unit_pikeman_blue.png")
RED_PIKEMAN_UNIT_IMG = util.load_img("unit_pikeman_red.png")
BLUE_ARCHER_UNIT_IMG = util.load_img("unit_archer_blue.png")
RED_ARCHER_UNIT_IMG = util.load_img("unit_archer_red.png")
BLUE_KNIGHT_UNIT_IMG = util.load_img("unit_knight_blue.png")
RED_KNIGHT_UNIT_IMG = util.load_img("unit_knight_red.png")


class UnitType(Enum):
    ERROR = -1
    EMPTY = 0
    PIKEMAN = 1
    ARCHER = 2
    KNIGHT = 3


class Unit:
    def __init__(self, unit_type, owner, direction):
        self.unit_type = unit_type
        self.owner = owner
        self.direction = direction

    def draw(self, win, pos):
        if self.unit_type == UnitType.PIKEMAN:
            if self.owner == Player.RED:
                win.blit(RED_PIKEMAN_UNIT_IMG, pos)
            if self.owner == Player.BLUE:
                win.blit(BLUE_PIKEMAN_UNIT_IMG, pos)
