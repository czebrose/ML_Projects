import util
from util import Direction, PlayerCommands, PlayerColor
from player import PlayerInput
from node import Node
import random


INCOME_TO_EXPENSE_RATIO = 2
BUILD_CHANCE = 0.8
CHANGE_DIRECTION_CHANCE = 0.1
MAX_EMPTY_NODES = 3


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
        expenses = 0
        income = 0
        empty_nodes = 0
        for node in owned_nodes:
            if node.building.can_spawn_unit():
                expenses = expenses + util.UNIT_COST
            income = income + (node.building.generate_gold() * util.SPAWN_DELAY)
            if node.building.is_empty():
                empty_nodes = empty_nodes + 1
        is_rich = income > expenses * INCOME_TO_EXPENSE_RATIO

        if random.random() < BUILD_CHANCE or empty_nodes >= MAX_EMPTY_NODES:
            # We want to build a building.
            for node in owned_nodes:
                if node.building.is_empty():
                    if is_rich:
                        self.target_command = PlayerCommands.BUILD_BARRACKS
                    else:
                        self.target_command = PlayerCommands.BUILD_MINE
                    return node
        for node in owned_nodes:
            if not node.exit_direction[self.color] or (is_rich and random.random() < CHANGE_DIRECTION_CHANCE):
                self.target_command = self.get_random_valid_direction(node)
                if self.target_command:
                    return node
        self.target_command = None
        return None

    def get_command(self, global_map) -> object:
        return self.target_command

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
