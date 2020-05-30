from util import PlayerColor, UnitType
import unit


UNIT_LIST = [UnitType.PIKEMAN, UnitType.KNIGHT, UnitType.ARCHER]
PLAYER_LIST = [PlayerColor.BLUE, PlayerColor.RED, PlayerColor.NEUTRAL]


class LocDiffusion:
    def __init__(self):
        self.node_value = {}
        self.unit_value = {}
        self.unit_type = UnitType.EMPTY
        self.unit_owner = PlayerColor.NEUTRAL
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
                self.unit_lambda[u][color] = float(1)

    def set_node_value(self, building, player):
        if building.is_empty():
            self.node_value[player] = 500
        elif building.is_home():
            self.node_value[player] = 1000
        else:
            self.node_value[player] = 800

    def set_unit_value(self, unit_type, player):
        self.unit_value[unit_type][player] = 1000
        self.unit_type = unit_type
        self.unit_owner = player
        for u in UNIT_LIST:
            for color in PLAYER_LIST:
                self.unit_lambda[u][color] = self.get_unit_lambda(u, color)

    def get_node_value(self, player):
        return self.node_value[player]

    def get_unit_value(self, unit_type, player):
        return self.unit_value[unit_type][player]

    def get_unit_lambda(self, other_unit_type, other_player):
        if self.unit_owner is other_player:
            return 1.0
        self_kills_other = unit.get_fight_result(other_unit_type, self.unit_type)
        other_kills_self = unit.get_fight_result(self.unit_type, other_unit_type)
        if self_kills_other and other_kills_self:
            return 0.5
        elif self_kills_other:
            return 0.0
        else:
            return 1.0

    def spread_node(self, neighbors):
        for color in PLAYER_LIST:
            node_total = 0
            for n in neighbors:
                node_total += n.node_value[color] - self.node_value[color]
            node_total *= 0.25
            self.node_value[color] = self.node_value[color] + node_total

    def spread_unit(self, neighbors):
        for color in PLAYER_LIST:
            for u in UNIT_LIST:
                unit_total = 0
                for n in neighbors:
                    unit_total += n.unit_value[u][color] - self.unit_value[u][color]
                unit_total *= 0.25
                self.unit_value[u][color] = self.unit_lambda[u][color] * (self.unit_value[u][color] + unit_total)

    def spread(self, neighbors):
        self.spread_node(neighbors)
        self.spread_unit(neighbors)


