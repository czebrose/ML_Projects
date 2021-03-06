from util import PlayerColor, UnitType
from location import Location
import pygame
pygame.font.init()


STAT_FONT = pygame.font.SysFont("comicsans", 25)

player = PlayerColor.NEUTRAL
unit_type = UnitType.EMPTY
show_diffusion_values = False
print_player_thoughts = False


def check_input():
    global player, show_diffusion_values, unit_type
    keys = pygame.key.get_pressed()
    if keys[pygame.K_0]:
        player = PlayerColor.RED
    elif keys[pygame.K_9]:
        player = PlayerColor.NEUTRAL
    elif keys[pygame.K_8]:
        player = PlayerColor.BLUE
    elif keys[pygame.K_p]:
        unit_type = UnitType.PIKEMAN
    elif keys[pygame.K_o]:
        unit_type = UnitType.ARCHER
    elif keys[pygame.K_i]:
        unit_type = UnitType.KNIGHT
    elif keys[pygame.K_u]:
        unit_type = UnitType.EMPTY
    elif keys[pygame.K_MINUS]:
        show_diffusion_values = True
    elif keys[pygame.K_EQUALS]:
        show_diffusion_values = False


def draw(win, global_map):
    if not show_diffusion_values:
        return
    for row in global_map:
        for loc in row:
            if isinstance(loc, Location):
                color = (0, 0, 0)
                if unit_type is UnitType.EMPTY:
                    node_value, node_lerp = loc.diffusion.get_node_value(player)
                    diff_value = "{:.0f}".format(node_value)
                else:
                    diff_value = "{:.0f}".format(loc.diffusion.get_unit_value(unit_type, player))
                text = STAT_FONT.render(diff_value, True, color)
                win.blit(text, loc.get_pixel_pos())
