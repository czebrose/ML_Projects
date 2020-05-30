from util import PlayerColor, UnitType, BuildingType


class LocDiffusion:
    def __init__(self):
        self.node_value = {}
        self.unit_value = {}
        for u in UnitType:
            self.unit_value[u] = {}
        self.time = 0
        self.reset()

    def reset(self):
        for color in PlayerColor:
            self.node_value[color] = float(0)

    def set_node_value(self, building, player):
        if building.is_empty():
            self.node_value[player] = 500
        elif building.is_home():
            self.node_value[player] = 1000
        else:
            self.node_value[player] = 800

    def set_unit_value(self, unit_type, player):
        pass

    def get_node_value(self, player):
        return self.node_value[player]

    def spread(self, neighbors):
        for color in PlayerColor:
            neighbor_total = 0
            for n in neighbors:
                neighbor_total += n.node_value[color] - self.node_value[color]
            neighbor_total *= 0.25
            self.node_value[color] = self.node_value[color] + neighbor_total
