import pygame
import os


def load_img(img_name):
    return pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", img_name)))