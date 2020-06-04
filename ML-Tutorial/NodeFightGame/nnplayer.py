from util import PlayerColor
from player import PlayerInput


class NNetPlayer(PlayerInput):
    def __init__(self, g, net):
        PlayerInput.__init__(self, PlayerColor.NEUTRAL)
        self.g = g
        self.net = net

    def update(self, global_map):
        # update target_node and command
        pass
