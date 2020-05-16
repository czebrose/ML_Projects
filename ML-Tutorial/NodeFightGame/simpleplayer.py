from util import Direction, PlayerCommands
from player import PlayerInput
from node import Node
import random


DIRECTION_THRESHOLD = 500


def get_random_valid_direction(node):
    choices = []
    if node.neighbors[Direction.NORTH]:
        choices.append(PlayerCommands.DIRECTION_NORTH)
    elif node.neighbors[Direction.WEST]:
        choices.append(PlayerCommands.DIRECTION_WEST)
    if len(choices) > 0:
        return random.choice(choices)
    return None


class SimplePlayer(PlayerInput):
    def __init__(self, color):
        PlayerInput.__init__(self, color)
        self.target_command = None

    def get_highlight_node(self, global_map) -> object:
        owned_nodes = []
        for row in global_map:
            for loc in row:
                if isinstance(loc, Node) and loc.owner is self.color:
                    owned_nodes.append(loc)
        if len(owned_nodes) <= 0:
            return None
        for node in owned_nodes:
            if not node.exit_direction[self.color]:
                self.target_command = get_random_valid_direction(node)
                if self.target_command:
                    return node
        for node in owned_nodes:
            if not node.building:
                choices = [PlayerCommands.BUILD_MINE, PlayerCommands.BUILD_BARRACKS]
                self.target_command = random.choice(choices)
                return node
        self.target_command = None
        return random.choice(owned_nodes)

    def get_command(self, global_map) -> object:
        if self.target_command:
            return self.target_command
        if self.gold > DIRECTION_THRESHOLD and self.highlight_node:
            return get_random_valid_direction(self.highlight_node)
        return None
