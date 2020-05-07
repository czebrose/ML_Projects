import pygame
from node import Node
from road import Road
from location import Direction


def check_input():
    pass


def collect_gold():
    pass


def fight():
    pass


def spawn_units():
    pass


def move_units():
    pass


def draw():
    pass


def build_map():
    map = []
    # Create nodes
    for x in range(3):
        map.append([])
        for y in range(3):
            map[x].append(Node(x, y))
    # Create north-south roads
    for x in range(3):
        for y in range(2):
            north_node = map[x][y]
            south_node = map[x][y+1]
            north_road = Road()
            mid_road = Road()
            south_road = Road()

            north_node.add_neighbor(Direction.SOUTH, north_road)
            north_road.add_neighbor(Direction.SOUTH, mid_road)
            mid_road.add_neighbor(Direction.SOUTH, south_road)
            south_road.add_neighbor(Direction.SOUTH, south_node)

    for x in range(2):
        for y in range(3):
            west_node = map[x][y]
            east_node = map[x+1][y]
            west_road = Road()
            mid_road = Road()
            east_road = Road()

            west_node.add_neighbor(Direction.EAST, west_road)
            west_road.add_neighbor(Direction.EAST, mid_road)
            mid_road.add_neighbor(Direction.EAST, east_road)
            east_road.add_neighbor(Direction.EAST, east_node)

    return map


global_map = build_map()
run = True
while run:
    check_input()
    collect_gold()
    fight()
    spawn_units()
    move_units()
    draw()
    run = False
