from enum import Enum


class Direction(Enum):
    ERROR = -1
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3


class Location:
    neighbors = {
        Direction.NORTH: None,
        Direction.SOUTH: None,
        Direction.EAST: None,
        Direction.WEST: None
    }

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
