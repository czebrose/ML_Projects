from util import Direction
from player import PlayerInput, PlayerCommands
from node import Node
import random


DIRECTION_THRESHOLD = 100

class SimplePlayer(PlayerInput):
    def get_highlight_node(self, global_map) -> object:
        owned_nodes = []
        for row in global_map:
            for loc in row:
                if isinstance(loc, Node) and loc.owner is self.color:
                    owned_nodes.append(loc)
        return owned_nodes[random.randrange(0, len(owned_nodes))]

    def get_command(self, global_map) -> object:
        if not self.highlight_node:
            return None
        if self.gold > DIRECTION_THRESHOLD:
            choices = []
            if self.highlight_node.neighbors[Direction.NORTH]:
                choices.append(PlayerCommands.DIRECTION_NORTH)
            if self.highlight_node.neighbors[Direction.WEST]:
                choices.append(PlayerCommands.DIRECTION_WEST)
            if len(choices) > 0:
                return random.choice(choices)
        return None
