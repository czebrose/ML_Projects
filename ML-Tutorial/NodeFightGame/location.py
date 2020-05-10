import random
from enum import Enum
from node import Unit


class Direction(Enum):
    ERROR = -1
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3


class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = {
            Direction.NORTH: None,
            Direction.SOUTH: None,
            Direction.EAST: None,
            Direction.WEST: None
        }
        self.unit_in_loc = None
        self.expected_units = []

    def add_neighbor(self, direction, neighbor, set_neighbor=True):
        self.neighbors[direction] = neighbor
        if set_neighbor:
            rev_direction = self.reverse_direction(direction)
            neighbor.add_neighbor(rev_direction, self, False)

    def get_neighbors(self):
        return self.neighbors

    @staticmethod
    def reverse_direction(direction):
        if direction == Direction.NORTH:
            return Direction.SOUTH
        if direction == Direction.SOUTH:
            return Direction.NORTH
        if direction == Direction.EAST:
            return Direction.WEST
        if direction == Direction.WEST:
            return Direction.EAST
        return Direction.ERROR

    def get_direction(self):
        return Direction.ERROR

    def notify_move_target(self):
        if self.unit_in_loc is None:
            return
        direction = self.get_direction()
        if direction is None:
            return
        neighbor = self.neighbors[direction]
        if neighbor is None:
            return
        neighbor.expected_units.append((self.unit_in_loc, self))

    def resolve_move_conflicts(self):
        if len(self.expected_units) > 1:
            accept_index = random.randint(0, len(self.expected_units)-1)
            blocked_locations = []
            for index in range(0, len(self.expected_units)):
                if index is not accept_index:
                    unit, loc = self.expected_units[index]
                    blocked_locations.append(loc)
            self.expected_units = [self.expected_units[accept_index]]
            self.resolve_blocked_locations(blocked_locations)

    @staticmethod
    def resolve_blocked_locations(blocked_locations):
        while len(blocked_locations) > 0:
            popped_loc = blocked_locations.pop(0)
            if len(popped_loc.expected_units) > 0:
                for blocked_unit, blocked_loc in popped_loc.expected_units:
                    blocked_locations.append(blocked_loc)
                popped_loc.expected_units = []

    def resolve_passing_conflicts(self):
        if len(self.expected_units) >= 1 and self.unit_in_loc is not None:
            exp_unit_a, exp_loc_a = self.expected_units[0]
            if len(exp_loc_a.expected_units) >= 1:
                exp_unit_b, exp_loc_b = exp_loc_a.expected_units[0]
                if self.unit_in_loc is exp_unit_b and self is exp_loc_b:
                    exp_loc_a.expected_units = []
                    self.expected_units = []

    def accept_unit(self):
        if len(self.expected_units) >= 1:
            unit, loc = self.expected_units[0]
            for direction in loc.neighbors:
                if self is loc.neighbors[direction]:
                    unit.direction = direction
            self.unit_in_loc = unit
            loc.unit_in_loc = None
            self.expected_units = []
