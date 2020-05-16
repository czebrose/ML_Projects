import pygame
from player import PlayerInput, PlayerColor, PlayerCommands


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
        if self.color == PlayerColor.BLUE:
            if keys[pygame.K_LEFT]:
                command = PlayerCommands.DIRECTION_WEST
            elif keys[pygame.K_RIGHT]:
                command = PlayerCommands.DIRECTION_EAST
            elif keys[pygame.K_UP]:
                command = PlayerCommands.DIRECTION_NORTH
            elif keys[pygame.K_DOWN]:
                command = PlayerCommands.DIRECTION_SOUTH
            elif keys[pygame.K_KP0]:
                command = PlayerCommands.CLEAR_DIRECTION
        elif self.color == PlayerColor.RED:
            if keys[pygame.K_a]:
                command = PlayerCommands.DIRECTION_WEST
            elif keys[pygame.K_d]:
                command = PlayerCommands.DIRECTION_EAST
            elif keys[pygame.K_w]:
                command = PlayerCommands.DIRECTION_NORTH
            elif keys[pygame.K_s]:
                command = PlayerCommands.DIRECTION_SOUTH
            elif keys[pygame.K_x]:
                command = PlayerCommands.CLEAR_DIRECTION
        return command
