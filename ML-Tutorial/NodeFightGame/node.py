import pygame
import util
from location import Location, Direction


HOME_NODE_EMPTY_IMG = util.load_img("home_node_empty.png")


class Node(Location):
    def draw(self, win):
        pixel_x = self.x * 50
        pixel_y = self.y * 50
        win.blit(HOME_NODE_EMPTY_IMG, (pixel_x, pixel_y))
