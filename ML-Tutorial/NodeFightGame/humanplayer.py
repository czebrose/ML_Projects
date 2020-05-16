import pygame
from player import PlayerInput
from util import PlayerColor, PlayerCommands


class HumanPlayerInput(PlayerInput):
    def get_highlight_node(self, global_map):
        (button1, button2, button3) = pygame.mouse.get_pressed()
        if button1:
            (x, y) = pygame.mouse.get_pos()
            for col in global_map:
                for loc in col:
                    if loc is not None and loc.check_click(x, y):
                        return loc
        return self.highlight_node

    def get_command(self, global_map):
        keys = pygame.key.get_pressed()
        command = None
        if keys[pygame.K_a]:
            command = PlayerCommands.DIRECTION_WEST
        elif keys[pygame.K_d]:
            command = PlayerCommands.DIRECTION_EAST
        elif keys[pygame.K_w]:
            command = PlayerCommands.DIRECTION_NORTH
        elif keys[pygame.K_s]:
            command = PlayerCommands.DIRECTION_SOUTH
        elif keys[pygame.K_r]:
            command = PlayerCommands.CLEAR_DIRECTION
        elif keys[pygame.K_q]:
            command = PlayerCommands.BUILD_MINE
        elif keys[pygame.K_e]:
            command = PlayerCommands.BUILD_BARRACKS
        elif keys[pygame.K_z]:
            command = PlayerCommands.UNIT_PIKEMAN
        elif keys[pygame.K_x]:
            command = PlayerCommands.UNIT_ARCHER
        elif keys[pygame.K_c]:
            command = PlayerCommands.UNIT_KNIGHT
        return command
