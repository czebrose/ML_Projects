import random
from util import Direction


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

    def check_click(self, x, y):
        return False

    def notify_move_target(self):
        if self.unit_in_loc is None:
            return
        direction = self.get_direction(self.unit_in_loc.owner)
        if direction is None:
            return
        neighbor = self.neighbors[direction]
        if neighbor is None:
            return
        neighbor.expected_units.append((self.unit_in_loc, self))
        self.unit_in_loc = None

    def resolve_move_conflicts(self):
        accept_index = -1
        accepted_unit = None
        if self.unit_in_loc is None and len(self.expected_units) > 0:
            accept_index = random.randint(0, len(self.expected_units) - 1)
            accepted_unit = self.expected_units[accept_index]
        blocked_units = []
        for index in range(0, len(self.expected_units)):
            if index is not accept_index:
                blocked_units.append(self.expected_units[index])
        self.expected_units = []
        if accepted_unit:
            self.expected_units.append(accepted_unit)
        self.resolve_blocked_locations(blocked_units)

    @staticmethod
    def resolve_blocked_locations(blocked_units):
        while len(blocked_units) > 0:
            unit, loc = blocked_units.pop(0)
            if len(loc.expected_units) > 0:
                for blocked_unit in loc.expected_units:
                    blocked_units.append(blocked_unit)
            loc.unit_in_loc = unit
            loc.expected_units = []

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
            self.expected_units = []
