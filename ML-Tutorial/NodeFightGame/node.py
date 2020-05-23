import util
from util import Direction, UnitType, PlayerColor, BuildingType
from unit import Unit
from location import Location
from building import Building


RED_NODE_IMG = util.load_img("node_red.png")
BLUE_NODE_IMG = util.load_img("node_blue.png")
NEUTRAL_NODE_IMG = util.load_img("node_neutral.png")

NODE_EXIT_RED_NORTH_IMG = util.load_img("node_exit_red_north.png")
NODE_EXIT_RED_SOUTH_IMG = util.load_img("node_exit_red_south.png")
NODE_EXIT_RED_WEST_IMG = util.load_img("node_exit_red_west.png")
NODE_EXIT_RED_EAST_IMG = util.load_img("node_exit_red_east.png")
NODE_EXIT_BLUE_NORTH_IMG = util.load_img("node_exit_blue_north.png")
NODE_EXIT_BLUE_SOUTH_IMG = util.load_img("node_exit_blue_south.png")
NODE_EXIT_BLUE_WEST_IMG = util.load_img("node_exit_blue_west.png")
NODE_EXIT_BLUE_EAST_IMG = util.load_img("node_exit_blue_east.png")


class Node(Location):
    def __init__(self, x, y, node_type):
        Location.__init__(self, x, y)
        if node_type == 'N':
            self.owner = PlayerColor.NEUTRAL
            self.building = Building(BuildingType.EMPTY, UnitType.EMPTY)
        elif node_type == 'B':
            self.owner = PlayerColor.BLUE
            self.building = Building(BuildingType.HOME, UnitType.PIKEMAN)
        elif node_type == 'R':
            self.owner = PlayerColor.RED
            self.building = Building(BuildingType.HOME, UnitType.PIKEMAN)
        self.spawn_timer = 0
        self.exit_direction = {PlayerColor.RED: None, PlayerColor.BLUE: None}
        self.unit_in_loc = self.unit_in_loc

    def add_neighbor(self, direction, neighbor, set_neighbor=True):
        Location.add_neighbor(self, direction, neighbor, set_neighbor)

    def collect_gold(self, players):
        if players.keys().__contains__(self.owner):
            players[self.owner].gold += self.building.generate_gold()
        return players

    def attempt_spawn(self, player_gold):
        if not self.building.can_spawn_unit():
            return player_gold
        if self.spawn_timer > 0:
            self.spawn_timer -= 1
        elif self.unit_in_loc is None and player_gold[self.owner].gold >= util.UNIT_COST:
            self.unit_in_loc = Unit(self.building.unit_type, self.owner, self.exit_direction[self.owner])
            self.spawn_timer = util.SPAWN_DELAY
            player_gold[self.owner].gold -= util.UNIT_COST
        return player_gold

    def get_direction(self, owner):
        if self.exit_direction.keys().__contains__(owner):
            return self.exit_direction[owner]
        return None

    def set_exit_direction(self, owner, direction):
        self.exit_direction[owner] = direction
        if self.unit_in_loc:
            self.unit_in_loc.set_direction(self.exit_direction[self.owner])

    def get_next_node(self, direction):
        return self

    def accept_unit(self):
        Location.accept_unit(self)
        if self.unit_in_loc is not None:
            if self.owner is not self.unit_in_loc.owner:
                self.owner = self.unit_in_loc.owner
                self.building.type = BuildingType.EMPTY
            self.unit_in_loc.set_direction(self.exit_direction[self.owner])

    def check_click(self, x, y):
        top = self.y * util.NODE_WIDTH
        left = self.x * util.NODE_WIDTH
        right = left + util.NODE_WIDTH
        bottom = top + util.NODE_WIDTH
        return left <= x <= right and top <= y <= bottom

    def is_home_node(self, player):
        return self.owner == player and self.building.type == BuildingType.HOME

    def draw_node(self, win, pos):
        if self.owner == PlayerColor.RED:
            win.blit(RED_NODE_IMG, pos)
        elif self.owner == PlayerColor.BLUE:
            win.blit(BLUE_NODE_IMG, pos)
        else:
            win.blit(NEUTRAL_NODE_IMG, pos)

    def draw_node_exit(self, win, pos):
        if self.exit_direction[PlayerColor.RED] == Direction.NORTH:
            win.blit(NODE_EXIT_RED_NORTH_IMG, pos)
        elif self.exit_direction[PlayerColor.RED] == Direction.SOUTH:
            win.blit(NODE_EXIT_RED_SOUTH_IMG, pos)
        elif self.exit_direction[PlayerColor.RED] == Direction.EAST:
            win.blit(NODE_EXIT_RED_EAST_IMG, pos)
        elif self.exit_direction[PlayerColor.RED] == Direction.WEST:
            win.blit(NODE_EXIT_RED_WEST_IMG, pos)
        if self.exit_direction[PlayerColor.BLUE] == Direction.NORTH:
            win.blit(NODE_EXIT_BLUE_NORTH_IMG, pos)
        elif self.exit_direction[PlayerColor.BLUE] == Direction.SOUTH:
            win.blit(NODE_EXIT_BLUE_SOUTH_IMG, pos)
        elif self.exit_direction[PlayerColor.BLUE] == Direction.EAST:
            win.blit(NODE_EXIT_BLUE_EAST_IMG, pos)
        elif self.exit_direction[PlayerColor.BLUE] == Direction.WEST:
            win.blit(NODE_EXIT_BLUE_WEST_IMG, pos)

    def draw(self, win):
        pos = self.get_pixel_pos()
        self.draw_node(win, pos)
        self.draw_node_exit(win, pos)
        self.building.draw(win, pos)
