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
        self.analyze_map(global_map)
        self.determine_goal()
        self.pick_node()
        self.pick_command()

    def analyze_map(self, global_map):
        pass

    def determine_goal(self):
        pass

    def pick_node(self):
        if self.goal is SmartPlayerGoal.EXPAND:
            # find the ideal mine location
            pass
        elif self.goal is SmartPlayerGoal.ATTACK:
            # this is
            pass
        elif self.goal is SmartPlayerGoal.DEFEND:
            pass
        else:
            pass

    def pick_command(self):
        pass
