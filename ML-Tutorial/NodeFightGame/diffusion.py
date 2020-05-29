from util import PlayerColor


class LocDiffusion:
    def __init__(self):
        self.value = [{}, {}]
        self.time = 0
        for t in range(len(self.value)):
            for color in PlayerColor:
                self.value[t][color] = float(0)

    def set_value(self, player_value, player):
        for t in range(len(self.value)):
            self.value[t][player] = player_value

    def get_value(self, player):
        return self.value[self.time][player]

    def spread(self, neighbors):
        t = self.time
        self.time = (self.time + 1) % len(self.value)
        for color in PlayerColor:
            neighbor_total = 0
            for n in neighbors:
                neighbor_total += n.value[t][color] - self.value[t][color]
            neighbor_total *= 0.25
            self.value[self.time][color] = max(0, min(1, (0.9 * self.value[t][color]) + neighbor_total))
