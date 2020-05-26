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
    command = ...  # type: PlayerCommands
    target_node = ...  # type: Node

    def update(self, global_map):
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
        is_rich = income > expenses * INCOME_TO_EXPENSE_RATIO or self.gold > util.STARTING_GOLD

        if random.random() < BUILD_CHANCE or empty_nodes >= MAX_EMPTY_NODES:
            # We want to build a building.
            for node in owned_nodes:
                if node.building.is_empty():
                    if is_rich:
                        self.command = PlayerCommands.BUILD_BARRACKS
                    else:
                        self.command = PlayerCommands.BUILD_MINE
                    self.target_node = node
                    return
        for node in owned_nodes:
            if not node.get_direction(self.color) or (is_rich and random.random() < CHANGE_DIRECTION_CHANCE):
                self.command = self.get_random_valid_direction(node)
                if self.command:
                    self.target_node = node
                    return
        self.command = None
        self.target_node = None

    def get_random_valid_direction(self, node):
        good_choices = []
        enemy_choices = []
        all_choices = []
        directions = [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST]
        for d in directions:
            is_valid_node, is_unfriendly_node, is_enemy_node, is_enemy_home = self.add_direction_command(node, d)
            command = util.get_command_from_direction(d)
            if is_enemy_home:
                return command
            if is_enemy_node:
                enemy_choices.append(command)
            if is_unfriendly_node:
                good_choices.append(command)
            if is_valid_node:
                all_choices.append(command)
        if len(enemy_choices) > 0:
            return random.choice(enemy_choices)
        if len(good_choices) > 0:
            return random.choice(good_choices)
        if len(all_choices) > 0:
            return random.choice(all_choices)
        return None

    # Returns three booleans:
    #    - If this is a valid direction
    #    - If this is an unfriendly node
    #    - If this is an enemy node
    #    - If this is an enemy home node
    def add_direction_command(self, node, direction):
        n = node.neighbors[direction]
        is_valid_node = False
        is_unfriendly_node = False
        is_enemy_node = False
        is_enemy_home = False
        if n:
            n = n.get_next_node(direction)
            is_valid_node = True
            is_unfriendly_node = self.color is not n.owner
            is_enemy_node = is_unfriendly_node and n.owner is not PlayerColor.NEUTRAL
            is_enemy_home = is_unfriendly_node and n.is_home_node(n.owner)
        return is_valid_node, is_unfriendly_node, is_enemy_node, is_enemy_home
