import pygame
from player import PlayerInput
from util import PlayerColor, PlayerCommands


class HumanPlayerInput(PlayerInput):
    command = ...  # type: PlayerCommands
    target_node = ...  # type: Node

    def update(self, global_map):
        (button1, button2, button3) = pygame.mouse.get_pressed()
        if button1:
            (x, y) = pygame.mouse.get_pos()
            for col in global_map:
                for loc in col:
                    if loc is not None and loc.check_click(x, y):
                        self.target_node = loc
        keys = pygame.key.get_pressed()
        self.command = None
        if keys[pygame.K_a]:
            self.command = PlayerCommands.DIRECTION_WEST
        elif keys[pygame.K_d]:
            self.command = PlayerCommands.DIRECTION_EAST
        elif keys[pygame.K_w]:
            self.command = PlayerCommands.DIRECTION_NORTH
        elif keys[pygame.K_s]:
            self.command = PlayerCommands.DIRECTION_SOUTH
        elif keys[pygame.K_r]:
            self.command = PlayerCommands.CLEAR_DIRECTION
        elif keys[pygame.K_q]:
            self.command = PlayerCommands.BUILD_MINE
        elif keys[pygame.K_e]:
            self.command = PlayerCommands.BUILD_BARRACKS
        elif keys[pygame.K_1]:
            self.command = PlayerCommands.UNIT_PIKEMAN
        elif keys[pygame.K_2]:
            self.command = PlayerCommands.UNIT_ARCHER
        elif keys[pygame.K_3]:
            self.command = PlayerCommands.UNIT_KNIGHT
