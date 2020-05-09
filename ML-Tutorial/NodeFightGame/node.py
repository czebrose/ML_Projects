import pygame
from enum import Enum
import util
from unit import Unit, UnitType
from location import Location, Direction


RED_NODE_IMG = util.load_img("node_red.png")
BLUE_NODE_IMG = util.load_img("node_blue.png")
NEUTRAL_NODE_IMG = util.load_img("node_neutral.png")

NODE_EXIT_NORTH_IMG = util.load_img("node_exit_north.png")
NODE_EXIT_SOUTH_IMG = util.load_img("node_exit_south.png")
NODE_EXIT_WEST_IMG = util.load_img("node_exit_west.png")
NODE_EXIT_EAST_IMG = util.load_img("node_exit_east.png")

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
        self.spawn_type = UnitType.PIKEMAN
        self.spawn_timer = 0
        self.exit_direction = None

    def add_neighbor(self, direction, neighbor, set_neighbor=True):
        Location.add_neighbor(self, direction, neighbor, set_neighbor)
        self.exit_direction = direction

    def collect_gold(self, player_gold):
        if self.building == Building.HOME:
            player_gold[self.owner] += util.HOME_GOLD_PRODUCTION
        elif self.building == Building.MINE:
            player_gold[self.owner] += util.MINE_GOLD_PRODUCTION
        return player_gold

    def attempt_spawn(self, player_gold):
        if self.spawn_timer > 0:
            self.spawn_timer -= 1
        elif self.unit_in_node is None and player_gold[self.owner] >= util.UNIT_COST:
            self.unit_in_node = Unit(self.spawn_type, self.owner)
            self.spawn_timer = util.SPAWN_DELAY
            player_gold[self.owner] -= util.UNIT_COST
        return player_gold

    def draw_node(self, win, pos):
        if self.owner == Player.RED:
            win.blit(RED_NODE_IMG, pos)
        elif self.owner == Player.BLUE:
            win.blit(BLUE_NODE_IMG, pos)
        else:
            win.blit(NEUTRAL_NODE_IMG, pos)

    def draw_node_exit(self, win, pos):
        if self.exit_direction == Direction.NORTH:
            win.blit(NODE_EXIT_NORTH_IMG, pos)
        elif self.exit_direction == Direction.SOUTH:
            win.blit(NODE_EXIT_SOUTH_IMG, pos)
        elif self.exit_direction == Direction.EAST:
            win.blit(NODE_EXIT_EAST_IMG, pos)
        elif self.exit_direction == Direction.WEST:
            win.blit(NODE_EXIT_WEST_IMG, pos)

    def draw_building(self, win, pos):
        if self.building == Building.HOME:
            win.blit(HOME_BUILDING_IMG, pos)

    def draw_unit(self, win, pos):
        if self.unit_in_node is not None and self.unit_in_node.unit_type == UnitType.PIKEMAN:
            if self.owner == Player.RED:
                win.blit(RED_PIKEMAN_UNIT_IMG, pos)
            if self.owner == Player.BLUE:
                win.blit(BLUE_PIKEMAN_UNIT_IMG, pos)

    def draw(self, win):
        pixel_x = self.x * 50
        pixel_y = self.y * 50
        pos = (pixel_x, pixel_y)
        self.draw_node(win, pos)
        self.draw_node_exit(win, pos)
        self.draw_building(win, pos)
        self.draw_unit(win, pos)
