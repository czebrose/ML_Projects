import util
from util import Direction, PlayerCommands, PlayerColor, SmartPlayerGoal, BuildingType
from player import PlayerInput
from node import Node
import unit
import pygame
pygame.font.init()


STAT_FONT = pygame.font.SysFont("comicsans", 25)

show_quality = True


def check_improvement(best_improvement, best_command, current_quality, test_quality, test_command):
    improvement = test_quality - current_quality
    if improvement > best_improvement:
        return improvement, test_command
    return best_improvement, best_command


class SmartPlayer(PlayerInput):
    command = ...  # type: PlayerCommands
    target_node = ...  # type: Node

    def __init__(self, color):
        PlayerInput.__init__(self, color)
        self.goal = SmartPlayerGoal.EXPLORE
        self.expected_gold = self.gold
        self.owned_nodes = []

    def update(self, global_map):
        # set target_node and command
        improvement, node, command = self.get_best_command()
        print("Best Command: ", command, " Improvement: ", improvement)
        if self.use_improvement(improvement):
            self.target_node = node
            self.command = command
        else:
            self.target_node = None
            self.command = None
        self.expected_gold = self.gold + 200
        self.owned_nodes = self.find_nodes(global_map)

    def find_nodes(self, global_map):
        self.owned_nodes = []
        for row in global_map:
            for loc in row:
                if isinstance(loc, Node) and loc.owner is self.color:
                    self.owned_nodes.append(loc)
        return self.owned_nodes

    def get_best_command(self):
        best_node = None
        best_command = None
        best_improvement = 0
        for loc in self.owned_nodes:
            improvement, command = self.best_command_for_node(loc)
            if improvement > best_improvement:
                best_node = loc
                best_improvement = improvement
                best_command = command
        return best_improvement, best_node, best_command

    def best_command_for_node(self, node):
        node_diffusion = node.diffusion
        neighbor_diffusion = node.get_neighbors_diffusion()
        exit_dir = node.exit_direction[self.color]
        building_type = node.building.type
        current_quality = self.get_node_quality(node_diffusion, neighbor_diffusion, exit_dir, building_type)
        best_command = None
        best_improvement = 0
        dir_commands = [PlayerCommands.DIRECTION_SOUTH, PlayerCommands.DIRECTION_WEST,
                        PlayerCommands.DIRECTION_EAST, PlayerCommands.DIRECTION_NORTH]
        for c in dir_commands:
            new_direction = util.get_direction_from_command(c)
            quality = self.get_node_quality(node_diffusion, neighbor_diffusion, new_direction, building_type)
            best_improvement, best_command = check_improvement(best_improvement, best_command, current_quality,
                                                               quality, c)

        quality = self.get_node_quality(node_diffusion, neighbor_diffusion, exit_dir, BuildingType.BARRACKS)
        best_improvement, best_command = check_improvement(best_improvement, best_command, current_quality,
                                                           quality, PlayerCommands.BUILD_BARRACKS)
        quality = self.get_node_quality(node_diffusion, neighbor_diffusion, exit_dir, BuildingType.MINE)
        best_improvement, best_command = check_improvement(best_improvement, best_command, current_quality,
                                                           quality, PlayerCommands.BUILD_MINE)
        if node.building.can_spawn_unit():
            best_improvement, best_command\
                = self.get_improvement_for_unit_change(best_improvement, best_command, node_diffusion)
        return best_improvement, best_command

    def get_node_quality(self, node_diffusion, neighbor_diffusion_dict, exit_dir, building_type):
        quality = 0
        # unit part of the quality
        ally_unit_type, ally_unit_value, ally_unit_lerp = node_diffusion.get_main_unit(self.color)
        neighbor_diffusion = None
        enemy_unit_type = None
        enemy_unit_value = 0
        enemy_unit_lerp = 0
        if neighbor_diffusion_dict.__contains__(exit_dir):
            neighbor_diffusion = neighbor_diffusion_dict[exit_dir]
            enemy_unit_type, enemy_unit_value, enemy_unit_lerp = neighbor_diffusion.get_max_enemy_unit_value(self.color)
        else:
            enemy_unit_type, enemy_unit_value, enemy_unit_lerp = node_diffusion.get_max_enemy_unit_value(self.color)
        if enemy_unit_lerp > 0.01:
            enemy_unit_lerp = 1
        if not neighbor_diffusion:
            # We aren't moving, which is okay as long as we don't have any units.
            max_node_value = 0.00
            min_node_value = -1.00
            lerp = 1 - ally_unit_lerp
        else:
            enemy_node_value, enemy_node_lerp = neighbor_diffusion.get_max_enemy_node_value(self.color)
            ally_node_value, ally_node_lerp = neighbor_diffusion.get_node_value(self.color)
            if enemy_unit_value > 0:
                # We are moving towards enemies
                compare_result = unit.compare_unit_types(ally_unit_type, enemy_unit_type)
                if compare_result == 0:
                    # quality can just be based on the higher unit value.
                    max_node_value = 0.25 - 0.0 * ally_node_lerp + 2.0 * enemy_node_lerp  # all allied units, no enemies
                    min_node_value = 0.10 - 0.0 * ally_node_lerp + 2.0 * enemy_node_lerp  # all enemy units, no allies
                    lerp = (ally_unit_lerp - enemy_unit_lerp + 1) / 2.0
                elif compare_result < 0:
                    # We're sending units in to die.
                    max_node_value = 0.20 - 0.0 * ally_node_lerp - 2.0 * enemy_node_lerp  # no allied units
                    min_node_value = 0.00 - 0.0 * ally_node_lerp - 2.0 * enemy_node_lerp  # lots of allied units
                    lerp = 1 - ally_unit_lerp
                else:
                    # We're advantaged here.
                    max_node_value = 0.50 - 0.0 * ally_node_lerp + 2.0 * enemy_node_lerp  # lots of enemies here
                    min_node_value = 0.20 - 0.0 * ally_node_lerp + 2.0 * enemy_node_lerp  # no enemies here
                    lerp = enemy_unit_lerp
            else:
                # We aren't moving towards enemy units
                max_node_value = 0.50 - 4.0 * ally_node_lerp + 4.0 * enemy_node_lerp  # lots of allied units
                min_node_value = 0.20 - 4.0 * ally_node_lerp + 4.0 * enemy_node_lerp  # no allied units
                lerp = ally_unit_lerp
        quality += (lerp * (max_node_value - min_node_value)) + min_node_value

        # node part of the quality
        if self.expected_gold > self.gold:
            profit_modifier = -0.2 * (self.expected_gold - self.gold) / 500
        else:
            profit_modifier = 0.1 * (self.gold - self.expected_gold) / 500
        if building_type is BuildingType.HOME:
            quality += 0.8
        elif building_type is BuildingType.MINE:
            quality += 0.4 + 0.2 * (1 - enemy_unit_lerp) - profit_modifier
        elif building_type is BuildingType.BARRACKS:
            quality += 0.6 + 0.1 * enemy_unit_lerp + profit_modifier
        else:
            quality += -1.0
        return quality

    def get_improvement_for_unit_change(self, best_improvement, best_command, node_diffusion):
        ally_unit_type, ally_unit_value, ally_unit_lerp = node_diffusion.get_main_unit(self.color)
        enemy_unit_type, enemy_unit_value, enemy_unit_lerp = node_diffusion.get_max_enemy_unit_value(self.color)
        if enemy_unit_lerp > 0.05:
            counter_unit_type = util.get_counter_unit_type(enemy_unit_type)
            counter_unit_command = util.get_command_from_unit_type(counter_unit_type)
            compare_result = unit.compare_unit_types(ally_unit_type, enemy_unit_type)
            if compare_result < 0:
                improvement = 0.8
                if improvement > best_improvement:
                    return improvement, counter_unit_command
            elif compare_result == 0:
                improvement = 0.4
                if improvement > best_improvement:
                    return improvement, counter_unit_command
        return best_improvement, best_command

    def use_improvement(self, improvement):
        threshold_max = 0.40
        threshold_min = 0.05
        threshold_lerp = min(1 - (float(self.gold) / 2000), 1)
        if self.expected_gold < self.gold:
            threshold_lerp = max(threshold_lerp - 0.1, 0)
        else:
            threshold_lerp = min(threshold_lerp + 0.1, 1)
        threshold = (threshold_lerp * (threshold_max - threshold_min)) + threshold_min
        return improvement > threshold

    def draw(self, win):
        PlayerInput.draw(self, win)
        for node in self.owned_nodes:
            color = (0, 0, 0)
            node_diffusion = node.diffusion
            neighbor_diffusion = node.get_neighbors_diffusion()
            exit_dir = node.exit_direction[self.color]
            building_type = node.building.type
            current_quality = self.get_node_quality(node_diffusion, neighbor_diffusion, exit_dir, building_type)
            value = "{:.2f}".format(current_quality)
            text = STAT_FONT.render(value, True, color)
            win.blit(text, node.get_pixel_pos())
