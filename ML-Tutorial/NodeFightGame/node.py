import pygame
from enum import Enum
import util
from location import Location, Direction


RED_NODE_IMG = util.load_img("node_red.png")
BLUE_NODE_IMG = util.load_img("node_blue.png")
NEUTRAL_NODE_IMG = util.load_img("node_neutral.png")

HOME_BUILDING_IMG = util.load_img("building_home.png")

BLUE_PIKEMAN_UNIT_IMG = util.load_img("unit_pikeman_blue.png")
RED_PIKEMAN_UNIT_IMG = util.load_img("unit_pikeman_red.png")
BLUE_ARCHER_UNIT_IMG = util.load_img("unit_archer_blue.png")
RED_ARCHER_UNIT_IMG = util.load_img("unit_archer_red.png")
BLUE_KNIGHT_UNIT_IMG = util.load_img("unit_knight_blue.png")
RED_KNIGHT_UNIT_IMG = util.load_img("unit_knight_red.png")


class Player(Enum):
    ERROR = -1
    NEUTRAL = 0
    BLUE = 1
    RED = 2


class Building(Enum):
    ERROR = -1
    EMPTY = 0
    HOME = 1
    MINE = 2
    BARRACKS = 3


class Unit(Enum):
    ERROR = -1
    EMPTY = 0
    PIKEMAN = 1
    ARCHER = 2
    KNIGHT = 3


class Node(Location):
    def __init__(self, x, y, node_type):
        Location.__init__(self, x, y)
        if node_type == 'N':
            self.owner = Player.NEUTRAL
            self.building = Building.EMPTY
        elif node_type == 'B':
            self.owner = Player.BLUE
            self.building = Building.HOME
        elif node_type == 'R':
            self.owner = Player.RED
            self.building = Building.HOME
        self.unit_in_node = Unit.EMPTY
        self.spawn_type = Unit.PIKEMAN
        self.spawn_timer = 0

    def attempt_spawn(self, player_gold):
        if self.spawn_timer > 0:
            self.spawn_timer -= 1
        elif self.unit_in_node == Unit.EMPTY and player_gold[self.owner] >= util.UNIT_COST:
            self.unit_in_node = self.spawn_type
            self.spawn_timer = util.SPAWN_DELAY
            player_gold[self.owner] -= util.UNIT_COST
        return player_gold

    def draw(self, win):
        pixel_x = self.x * 50
        pixel_y = self.y * 50
        if self.owner == Player.RED:
            win.blit(RED_NODE_IMG, (pixel_x, pixel_y))
        elif self.owner == Player.BLUE:
            win.blit(BLUE_NODE_IMG, (pixel_x, pixel_y))
        else:
            win.blit(NEUTRAL_NODE_IMG, (pixel_x, pixel_y))
        if self.building == Building.HOME:
            win.blit(HOME_BUILDING_IMG, (pixel_x, pixel_y))
        if self.unit_in_node == Unit.PIKEMAN:
            if self.owner == Player.RED:
                win.blit(RED_PIKEMAN_UNIT_IMG, (pixel_x, pixel_y))
            if self.owner == Player.BLUE:
                win.blit(BLUE_PIKEMAN_UNIT_IMG, (pixel_x, pixel_y))
