import pygame
import os


SPAWN_DELAY = 5
UNIT_COST = 10
BUILDING_COST = 300
UNIT_TYPE_CHANGE_COST = 100
DIRECTION_CHANGE_COST = 20
HOME_GOLD_PRODUCTION = 50
MIND_GOLD_PRODUCTION = 30

NODE_WIDTH = 50


def load_img(img_name):
    return pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", img_name)))