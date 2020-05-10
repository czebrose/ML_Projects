import pygame
import io
import util
from node import Node, Player, Building
from road import Road
from location import Direction


WIN_WIDTH = 500
WIN_HEIGHT = 500

BACKGROUND_IMG = util.load_img("background.png")


def check_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            return False
    return True


def collect_gold(global_map, player_gold):
    for col in global_map:
        for location in col:
            if isinstance(location, Node):
                player_gold = location.collect_gold(player_gold)
    return player_gold


def fight(global_map):
    return global_map


def spawn_units(global_map, player_gold):
    for col in global_map:
        for location in col:
            if isinstance(location, Node):
                player_gold = location.attempt_spawn(player_gold)
    return global_map, player_gold


def move_units(global_map):
    for col in global_map:
        for location in col:
            if location is not None:
                location.notify_move_target()
    for col in global_map:
        for location in col:
            if location is not None:
                location.resolve_move_conflicts()
    for col in global_map:
        for location in col:
            if location is not None:
                location.resolve_passing_conflicts()
    for col in global_map:
        for location in col:
            if location is not None:
                location.accept_unit()
    return global_map


def draw(global_map, win, player_gold):
    win.blit(BACKGROUND_IMG, (0,0))
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
        if c == 'N' or c == 'B' or c == 'R':
            node = Node(x_index, y_index, c)
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


def main():
    global_map = build_map()
    player_gold = {Player.NEUTRAL: 0, Player.BLUE: 10, Player.RED: 10}
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(2)
        run = check_input()
        player_gold = collect_gold(global_map, player_gold)
        global_map = fight(global_map)
        global_map = move_units(global_map)
        global_map, player_gold = spawn_units(global_map, player_gold)
        draw(global_map, win, player_gold)


main()