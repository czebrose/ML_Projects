import pygame
import util


FIGHT_IMGS = [util.load_img("fight_1.png"), util.load_img("fight_2.png")]


class Fight:
    def __init__(self, pos):
        self.x, self.y = pos
        self.frame_count = 2

    def update(self):
        self.frame_count = self.frame_count - 1

    def should_remove(self):
        return self.frame_count <= 0

    def draw(self, win):
        if self.frame_count > 0:
            pixel_x = self.x * util.NODE_SIZE
            pixel_y = self.y * util.NODE_SIZE
            win.blit(FIGHT_IMGS[self.frame_count - 1], (pixel_x, pixel_y))
