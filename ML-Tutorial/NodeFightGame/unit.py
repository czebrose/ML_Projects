from enum import Enum


class UnitType(Enum):
    ERROR = -1
    EMPTY = 0
    PIKEMAN = 1
    ARCHER = 2
    KNIGHT = 3


class Unit:
    def __init__(self, unit_type, owner):
        self.unit_type = unit_type
        self.owner = owner
