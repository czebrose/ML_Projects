import util
from util import PlayerColor, UnitType, Direction
import unit


UNIT_LIST = [UnitType.PIKEMAN, UnitType.KNIGHT, UnitType.ARCHER]
PLAYER_LIST = [PlayerColor.BLUE, PlayerColor.RED, PlayerColor.NEUTRAL]
DIRECTION_LIST = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]


class LocDiffusion:
    def __init__(self):
        self.node_value = {}
        self.unit_type = UnitType.EMPTY
        self.unit_owner = PlayerColor.NEUTRAL
        self.unit_dir_pref = {}
        for color in PLAYER_LIST:
            self.unit_dir_pref[color] = None
        self.unit_value = {}
        self.unit_lambda = {}
        for u in UNIT_LIST:
            self.unit_value[u] = {}
            self.unit_lambda[u] = {}
        self.reset()

    def reset(self):
        self.unit_type = UnitType.EMPTY
        self.unit_owner = PlayerColor.NEUTRAL
        for color in PLAYER_LIST:
            self.node_value[color] = float(0)
        for u in UNIT_LIST:
            for color in PLAYER_LIST:
                self.unit_value[u][color] = float(0)
                self.unit_lambda[u][color] = util.NEUTRAL_L

    def set_node_value(self, building, player):
        if building.is_empty():
            self.node_value[player] = util.EMPTY_OWNED_NODE_VALUE
        elif building.is_home():
            self.node_value[player] = util.HOME_NODE_VALUE
        else:
            self.node_value[player] = util.BUILDING_NODE_VALUE

    def set_unit_value(self, unit_type, player):
        self.unit_value[unit_type][player] = util.UNIT_VALUE
        self.unit_type = unit_type
        self.unit_owner = player
        for u in UNIT_LIST:
            for color in PLAYER_LIST:
                self.unit_lambda[u][color] = self.get_unit_lambda(u, color)

    def set_unit_dir_pref(self, direction, player):
        self.unit_dir_pref[player] = direction

    def get_node_value(self, player):
        return self.node_value[player]

    def get_unit_value(self, unit_type, player):
        return self.unit_value[unit_type][player]

    def get_unit_lambda(self, other_unit_type, other_player):
        if self.unit_owner is other_player:
            return util.NEUTRAL_L
        self_kills_other = unit.get_fight_result(other_unit_type, self.unit_type)
        other_kills_self = unit.get_fight_result(self.unit_type, other_unit_type)
        if self_kills_other and other_kills_self:
            return util.SAME_UNIT_L
        elif self_kills_other:
            return util.COUNTER_UNIT_L
        else:
            return util.ANTI_COUNTER_UNIT_L

    def spread_node(self, neighbors):
        for color in PLAYER_LIST:
            node_total = 0
            for d in DIRECTION_LIST:
                if neighbors.__contains__(d):
                    n = neighbors[d]
                    node_total += util.NODE_D * (n.node_value[color] - self.node_value[color])
                else:
                    node_total += util.EMPTY_D * (0 - self.node_value[color])
            self.node_value[color] = self.node_value[color] + node_total

    def spread_unit(self, neighbors):
        for color in PLAYER_LIST:
            for u in UNIT_LIST:
                unit_total = 0
                for d in DIRECTION_LIST:
                    if neighbors.__contains__(d):
                        n = neighbors[d]
                        diff = n.unit_value[u][color] - self.unit_value[u][color]
                        if d is n.unit_dir_pref[color]:
                            unit_total += util.UNIT_TO_PREF_DIR_D * diff
                        elif not n.unit_dir_pref[color]:
                            unit_total += util.UNIT_NO_PREF_DIR_D * diff
                        else:
                            unit_total += util.UNIT_FROM_PREF_DIR_D * diff
                    else:
                        unit_total += util.EMPTY_D * (0 - self.unit_value[u][color])
                self.unit_value[u][color] = self.unit_lambda[u][color] * (self.unit_value[u][color] + unit_total)

    # neighbors is a dictionary of directions to diffusion objects
    def spread(self, neighbors):
        self.spread_node(neighbors)
        self.spread_unit(neighbors)
