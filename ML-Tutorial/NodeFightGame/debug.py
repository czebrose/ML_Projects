from util import PlayerColor
from location import Location
import pygame
pygame.font.init()


STAT_FONT = pygame.font.SysFont("comicsans", 25)

player = PlayerColor.BLUE
show = True


def check_input():
    global player, show
    keys = pygame.key.get_pressed()
    if keys[pygame.K_0]:
        player = PlayerColor.RED
    elif keys[pygame.K_9]:
        player = PlayerColor.NEUTRAL
    elif keys[pygame.K_8]:
        player = PlayerColor.BLUE
    elif keys[pygame.K_MINUS]:
        show = True
    elif keys[pygame.K_EQUALS]:
        show = False


def draw(win, global_map):
    if not show:
        return
    for row in global_map:
        for loc in row:
            if isinstance(loc, Location):
                color = (0, 0, 0)
                diff_value = "{:.0f}".format(loc.diffusion.get_node_value(player))
                text = STAT_FONT.render(diff_value, True, color)
                win.blit(text, loc.get_pixel_pos())