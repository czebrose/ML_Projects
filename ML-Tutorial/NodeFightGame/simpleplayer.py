from util import Direction, PlayerCommands, PlayerColor
from player import PlayerInput
from node import Node
import random


DIRECTION_THRESHOLD = 500
BARRACKS_THRESHOLD = 500


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
            if not node.building and random.random() < 0.5:
                if self.gold > BARRACKS_THRESHOLD:
                    self.target_command = PlayerCommands.BUILD_BARRACKS
                else:
                    self.target_command = PlayerCommands.BUILD_MINE
                return node
        for node in owned_nodes:
            if not node.exit_direction[self.color]:
                self.target_command = self.get_random_valid_direction(node)
                if self.target_command:
                    return node
        self.target_command = None
        return random.choice(owned_nodes)

    def get_command(self, global_map) -> object:
        if self.target_command:
            return self.target_command
        if self.gold > DIRECTION_THRESHOLD and self.highlight_node:
            return self.get_random_valid_direction(self.highlight_node)
        return None

    def get_random_valid_direction(self, node):
        choices = []
        if self.add_direction_command(node, Direction.NORTH):
            choices.append(PlayerCommands.DIRECTION_NORTH)
        if self.add_direction_command(node, Direction.WEST):
            choices.append(PlayerCommands.DIRECTION_WEST)
        if self.add_direction_command(node, Direction.EAST):
            choices.append(PlayerCommands.DIRECTION_EAST)
        if self.add_direction_command(node, Direction.SOUTH):
            choices.append(PlayerCommands.DIRECTION_SOUTH)
        if len(choices) > 0:
            return random.choice(choices)
        return None

    def add_direction_command(self, node, direction):
        n = node.neighbors[direction]
        if n:
            n = n.get_next_node(direction)
            return n and self.color is not n.owner
        else:
            return None
