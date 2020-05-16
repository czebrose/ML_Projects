import pygame
import util
from enum import Enum
from player import PlayerColor


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

    # Returns true if the given enemy type would kill this unit.
    def get_fight_result(self, enemy_type):
        if self.unit_type is UnitType.PIKEMAN:
            return enemy_type is UnitType.PIKEMAN or enemy_type is UnitType.ARCHER
        elif self.unit_type is UnitType.ARCHER:
            return enemy_type is UnitType.ARCHER or enemy_type is UnitType.KNIGHT
        elif self.unit_type is UnitType.KNIGHT:
            return enemy_type is UnitType.KNIGHT or enemy_type is UnitType.PIKEMAN
        else:
            return True

    def draw(self, win, pos):
        if self.unit_type == UnitType.PIKEMAN:
            if self.owner == PlayerColor.RED:
                win.blit(RED_PIKEMAN_UNIT_IMG, pos)
            if self.owner == PlayerColor.BLUE:
                win.blit(BLUE_PIKEMAN_UNIT_IMG, pos)


def resolve_fight_round(round_fighters):
    fight_results = {}
    for color in round_fighters:
        fight_results[color] = False

    while list(fight_results.values()).count(False) > 1:
        results_iter = iter(fight_results)
        color_a = None
        color_b = None
        while color_a is None or color_b is None:
            c = next(results_iter)
            if not fight_results[c]:
                # if this unit is alive
                if not color_a:
                    color_a = c
                elif not color_b:
                    color_b = c
        unit_a = round_fighters[color_a].unit_in_loc
        unit_b = round_fighters[color_b].unit_in_loc
        fight_results[color_a] = unit_a.get_fight_result(unit_b.unit_type)
        fight_results[color_b] = unit_b.get_fight_result(unit_a.unit_type)

    return fight_results
