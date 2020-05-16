import pygame
import io
import util
from util import Direction
from player import PlayerColor, PlayerInput
from humanplayer import HumanPlayerInput
from node import Node, Building
from road import Road


WIN_WIDTH = 1000
WIN_HEIGHT = 1000

BACKGROUND_IMG = util.load_img("background.png")


def check_input(global_map, players):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            return False, global_map, players
    for p in players:
        global_map = players[p].check_input(global_map)
    return True, global_map, players


def collect_gold(global_map, players):
    for row in global_map:
        for location in row:
            if isinstance(location, Node):
                players = location.collect_gold(players)
    return players


def fight(global_map):
    for row in global_map:
        for location in row:
            if isinstance(location, Node):
                location.fight()
    for row in global_map:
        for location in row:
            if location:
                location.fight()
    return global_map


def spawn_units(global_map, players):
    for row in global_map:
        for location in row:
            if isinstance(location, Node):
                player_gold = location.attempt_spawn(players)
    return global_map, players


def move_units(global_map):
    for row in global_map:
        for location in row:
            if location is not None:
                location.notify_move_target()
    for row in global_map:
        for location in row:
            if location is not None:
                location.resolve_move_conflicts()
    for row in global_map:
        for location in row:
            if location is not None:
                location.accept_unit()
    return global_map


def draw(global_map, win, players):
    win.blit(BACKGROUND_IMG, (0,0))
    for map_row in global_map:
        for location in map_row:
            if location:
                location.draw(win)
    for p in players:
        players[p].draw(win)
    pygame.display.update()


def build_map():
    new_map = [[]]
    map_file = open("map_1.txt", "r")
    map_file_contents = map_file.read()
    x_index = 0
    y_index = 0
    for c in map_file_contents:
        if c == 'N' or c == 'B' or c == 'R':
            node = Node(x_index, y_index, c)
            new_map[y_index].append(node)
            x_index += 1
        elif c == '+':
            road = Road(x_index, y_index)
            new_map[y_index].append(road)
            x_index += 1
        elif c == '\n':
            x_index = 0
            y_index += 1
            new_map.append([])
        else:
            new_map[y_index].append(None)
            x_index += 1
    for y, row in enumerate(new_map):
        for x, location in enumerate(row):
            if location:
                if x < len(row) - 1:
                    east_loc = new_map[y][x+1]
                    if east_loc:
                        location.add_neighbor(Direction.EAST, east_loc)
                if y < len(new_map) - 1:
                    south_loc = new_map[y+1][x]
                    if south_loc:
                        location.add_neighbor(Direction.SOUTH, south_loc)
    return new_map


def main():
    global_map = build_map()
    players = {
        PlayerColor.BLUE: HumanPlayerInput(PlayerColor.BLUE),
        PlayerColor.RED: HumanPlayerInput(PlayerColor.RED)
    }
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    run = True
    tick_counter = 0
    while run:
        clock.tick(60)
        run, global_map, players = check_input(global_map, players)
        tick_counter += clock.get_time()
        if tick_counter > 500:
            tick_counter = 0
            players = collect_gold(global_map, players)
            global_map = fight(global_map)
            global_map = move_units(global_map)
            global_map, players = spawn_units(global_map, players)
        draw(global_map, win, players)


main()