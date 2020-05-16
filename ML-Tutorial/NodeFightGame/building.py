from enum import Enum
import util
import pygame


HOME_BUILDING_IMG = util.load_img("building_home.png")
MINE_BUILDING_IMG = util.load_img("building_mine.png")
BARRACKS_BUILDING_IMG = util.load_img("building_barracks.png")


class BuildingType(Enum):
    ERROR = -1
    EMPTY = 0
    HOME = 1
    MINE = 2
    BARRACKS = 3


class Building:
    def __init__(self, type):
        self.type = type

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
