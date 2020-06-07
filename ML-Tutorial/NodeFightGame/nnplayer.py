import util
import nnutil
from util import PlayerColor, PlayerCommands, UnitType, BuildingType, Direction
from player import PlayerInput
from node import Node
import os
import neat
import pickle


def get_unit_input(unit):
    if unit:
        return float(unit.unit_type.value) / UnitType.MAX.value
    else:
        return 0


def get_exit_dir_input(direction):
    if direction:
        return float(direction.value) / Direction.MAX.value
    else:
        return 0


def get_building_input(building):
    if building:
        return float(building.type.value) / BuildingType.MAX.value
    else:
        return 0


class NNetPlayer(PlayerInput):
    command = ...  # type: PlayerCommands
    target_node = ...  # type: Node

    def __init__(self, g, net, color=PlayerColor.NEUTRAL):
        PlayerInput.__init__(self, color)
        self.g = g
        self.net = net

    @classmethod
    def create_feedforward_from_pickle(cls, pickle_filename, config_filename, color=PlayerColor.NEUTRAL):
        pickle_ge = nnutil.get_genome(pickle_filename)
        net = neat.nn.FeedForwardNetwork.create(pickle_ge, nnutil.get_config(config_filename))
        return cls(pickle_ge, net, color)

    @classmethod
    def create_recurrent_from_pickle(cls, pickle_filename, config_filename, color=PlayerColor.NEUTRAL):
        pickle_ge = nnutil.get_genome(pickle_filename)
        net = neat.nn.RecurrentNetwork.create(pickle_ge, nnutil.get_config(config_filename))
        return cls(pickle_ge, net, color)

    def update(self, global_map):
        # update target_node and command
        nodes = []
        for row in global_map:
            for loc in row:
                if isinstance(loc, Node):
                    nodes.append(loc)

        input_vals = [float(self.gold) / util.STARTING_GOLD]
        for n in nodes:
            # owner, unit, building, direction
            input_vals.append(self.get_owner_input(n.owner))
            input_vals.append(get_unit_input(n.unit_in_loc))
            input_vals.append(get_exit_dir_input(n.get_direction(self.color)))
            input_vals.append(float(n.spawn_timer) / util.SPAWN_DELAY)

        output = self.net.activate(tuple(input_vals))
        i = 0
        max_command = None
        max_command_value = -1
        for c in PlayerCommands:
            if output[i] > max_command_value:
                max_command_value = output[i]
                max_command = c
            i += 1
        self.command = max_command
        max_node = None
        max_node_value = -1
        for n in nodes:
            if output[i] > max_node_value:
                max_node_value = output[i]
                max_node = n
            i += 1
        self.target_node = max_node

    def execute_command(self):
        PlayerInput.execute_command(self)

    def get_owner_input(self, owner):
        if owner is self.color:
            return 1
        else:
            return 0
