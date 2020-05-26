import util
from util import Direction, PlayerCommands, PlayerColor, SmartPlayerGoal
from player import PlayerInput
from node import Node
import random


class SmartPlayer(PlayerInput):
    def __init__(self, color):
        PlayerInput.__init__(self, color)
        self.goal = SmartPlayerGoal.EXPAND

    def update(self, global_map):
        # set target_node and command
        pass

    def determine_goal(self):
        pass

    def pick_node(self):
        pass

    def pick_command(self):
        pass
