import util
from util import Direction, PlayerColor
from fight import Fight
from diffusion import LocDiffusion
import unit
import abc
from abc import ABC


class Location(ABC):
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
        self.diffusion = LocDiffusion()

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

    @abc.abstractmethod
    def get_direction(self):
        return Direction.ERROR

    def get_next_node(self, direction):
        n = self.neighbors[direction]
        if n:
            return n.get_next_node(direction)
        else:
            return None

    def check_click(self, x, y):
        return False

    def is_home_node(self, player):
        return False

    def collect_gold(self, players):
        return players

    def attempt_spawn(self, players):
        return players

    def prepare_diffusion(self):
        #self.diffusion.reset()
        if self.unit_in_loc:
            self.diffusion.set_unit_value(self.unit_in_loc.unit_type, self.unit_in_loc.owner)

    def diffuse(self):
        diffusion_neighbors = {}
        for direction in self.neighbors:
            n = self.neighbors[direction]
            if n:
                diffusion_neighbors[direction] = n.diffusion
        self.diffusion.spread(diffusion_neighbors)

    def fight(self):
        # list of Fight objects
        fights = []
        # only fight if there's a unit here
        if not self.unit_in_loc:
            return fights
        # dictionary of PlayerColor to list of locations
        fighting_locations = {}
        fighting_locations = self.add_fighting_neighbor(fighting_locations, Direction.EAST)
        fighting_locations = self.add_fighting_neighbor(fighting_locations, Direction.WEST)
        fighting_locations = self.add_fighting_neighbor(fighting_locations, Direction.SOUTH)
        fighting_locations = self.add_fighting_neighbor(fighting_locations, Direction.NORTH)
        if self.unit_in_loc:
            fighting_locations = util.add_loc_to_fight_queue(fighting_locations, self.unit_in_loc.owner, self)

        while len(fighting_locations.keys()) > 1:
            # Dictionary of PlayerColor to Location
            round_fighters = {}
            for color in fighting_locations.keys():
                round_fighters[color] = fighting_locations[color].pop()
            while len(round_fighters) > 1:
                fight_results = unit.resolve_fight_round(round_fighters)
                for color in fight_results:
                    if fight_results[color]:
                        round_fighters[color].unit_in_loc = None
                        dead_loc = round_fighters.pop(color)
                        fights.append(Fight((dead_loc.x, dead_loc.y)))
                        if len(fighting_locations[color]) == 0:
                            # If this was the last unit for this player, remove that player from the fight.
                            fighting_locations.pop(color)
                    else:
                        fighting_locations[color].append(round_fighters[color])
        return fights

    def add_fighting_neighbor(self, fighting_locations, neighbor_dir):
        if self.neighbors[neighbor_dir] and self.neighbors[neighbor_dir].unit_in_loc:
            neighbor_owner = self.neighbors[neighbor_dir].unit_in_loc.owner
            fighting_locations\
                = util.add_loc_to_fight_queue(fighting_locations, neighbor_owner, self.neighbors[neighbor_dir])
        return fighting_locations

    def notify_move_target(self):
        if self.unit_in_loc is None:
            return
        direction = self.get_direction(self.unit_in_loc.owner)
        if direction is None:
            return
        neighbor = self.neighbors[direction]
        if neighbor is None:
            return
        neighbor.expected_units.append((self.unit_in_loc, self, direction))
        self.unit_in_loc = None

    def resolve_move_conflicts(self):
        accepted_unit = None
        if self.unit_in_loc is None and len(self.expected_units) > 0:
            accepted_unit = self.pick_expected_unit()
        blocked_units = []
        for unit in self.expected_units:
            if unit is not accepted_unit:
                blocked_units.append(unit)
        self.expected_units = []
        if accepted_unit:
            self.expected_units.append(accepted_unit)
        self.resolve_blocked_locations(blocked_units)

    def pick_expected_unit(self):
        self.expected_units.sort(key=lambda x: x[2])
        return self.expected_units[0]

    @staticmethod
    def resolve_blocked_locations(blocked_units):
        while len(blocked_units) > 0:
            unit, loc, dir = blocked_units.pop(0)
            if len(loc.expected_units) > 0:
                for blocked_unit in loc.expected_units:
                    blocked_units.append(blocked_unit)
            loc.unit_in_loc = unit
            loc.expected_units = []

    def accept_unit(self):
        if len(self.expected_units) >= 1:
            unit, loc, direction = self.expected_units[0]
            unit.set_direction(direction)
            unit.loc_changed()
            self.unit_in_loc = unit
            self.expected_units = []

    def get_pixel_pos(self):
        pixel_x = self.x * util.NODE_SIZE
        pixel_y = self.y * util.NODE_SIZE
        return pixel_x, pixel_y

    @abc.abstractmethod
    def draw(self, win):
        pass

    def draw_unit(self, win):
        pixel_x, pixel_y = self.get_pixel_pos()
        if self.unit_in_loc is not None:
            self.unit_in_loc.draw(win, (pixel_x, pixel_y))
