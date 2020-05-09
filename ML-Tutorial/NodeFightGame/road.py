import pygame
import util
from location import Location, Direction


NORTH_SOUTH_ROAD_EMPTY_IMG = util.load_img("road_northsouth.png")
EAST_WEST_ROAD_EMPTY_IMG = util.load_img("road_eastwest.png")


class Road(Location):
    def draw(self, win):
        pixel_x = self.x * 50
        pixel_y = self.y * 50
        if self.neighbors[Direction.NORTH] is not None:
            win.blit(NORTH_SOUTH_ROAD_EMPTY_IMG, (pixel_x, pixel_y))
        else:
            win.blit(EAST_WEST_ROAD_EMPTY_IMG, (pixel_x, pixel_y))
