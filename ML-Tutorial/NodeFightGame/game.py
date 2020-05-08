import pygame
import io
from node import Node
from road import Road
from location import Direction


WIN_WIDTH = 500
WIN_HEIGHT = 500


def check_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            return False
    return True


def collect_gold(global_map, player_gold):
    return player_gold


def fight():
    pass


def spawn_units():
    pass


def move_units():
    pass


def draw(global_map, win):
    for map_row in global_map:
        for location in map_row:
            if location:
                location.draw(win)
    pygame.display.update()


def build_map():
    new_map = [[]]
    map_file = open("map_1.txt", "r")
    map_file_contents = map_file.read()
    x_index = 0
    y_index = 0
    for c in map_file_contents:
        if c == 'N':
            node = Node(x_index, y_index)
            new_map[x_index].append(node)
            y_index += 1
        elif c == '+':
            road = Road(x_index, y_index)
            new_map[x_index].append(road)
            y_index += 1
        elif c == '\n':
            y_index = 0
            x_index += 1
            new_map.append([])
        else:
            new_map[x_index].append(None)
            y_index += 1
    for x, col in enumerate(new_map):
        for y, location in enumerate(col):
            if location:
                if y < len(col) - 1:
                    south_loc = new_map[x][y+1]
                    if south_loc:
                        location.add_neighbor(Direction.SOUTH, south_loc)
                if x < len(new_map) - 1:
                    east_loc = new_map[x+1][y]
                    if east_loc:
                        location.add_neighbor(Direction.EAST, east_loc)
    return new_map


global_map = build_map()
player_gold = [0, 0]
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()
run = True
while run:
    clock.tick(60)
    run = check_input()
    player_gold = collect_gold(global_map, player_gold)
    fight()
    spawn_units()
    move_units()
    draw(global_map, win)
