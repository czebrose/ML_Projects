from enum import Enum
import util
from util import UnitType, BuildingType
import pygame


HOME_BUILDING_IMG = util.load_img("building_home.png")
MINE_BUILDING_IMG = util.load_img("building_mine.png")
BARRACKS_BUILDING_IMG = util.load_img("building_barracks.png")

ARCHER_IMG = util.load_img("building_unit_archer.png")
KNIGHT_IMG = util.load_img("building_unit_knight.png")
PIKEMAN_IMG = util.load_img("building_unit_pikeman.png")


class Building:
    def __init__(self, type):
        self.type = type
        self.unit_type = UnitType.KNIGHT

    def can_spawn_unit(self):
        return self.type is BuildingType.HOME or self.type is BuildingType.BARRACKS

    def generate_gold(self):
        if self.type is BuildingType.HOME:
            return util.HOME_GOLD_PRODUCTION
        elif self.type == BuildingType.MINE:
            return util.MINE_GOLD_PRODUCTION
        else:
            return 0

    def draw(self, win, pos):
        if self.type == BuildingType.HOME:
            win.blit(HOME_BUILDING_IMG, pos)
        elif self.type == BuildingType.MINE:
            win.blit(MINE_BUILDING_IMG, pos)
        elif self.type == BuildingType.BARRACKS:
            win.blit(BARRACKS_BUILDING_IMG, pos)

        if self.can_spawn_unit():
            if self.unit_type == UnitType.PIKEMAN:
                win.blit(PIKEMAN_IMG, pos)
            elif self.unit_type == UnitType.ARCHER:
                win.blit(ARCHER_IMG, pos)
            elif self.unit_type == UnitType.KNIGHT:
                win.blit(KNIGHT_IMG, pos)
