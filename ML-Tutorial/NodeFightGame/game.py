import pygame
import io
import util
from player import PlayerColor, PlayerInput
from node import Node, Building
from road import Road
from location import Direction


WIN_WIDTH = 500
WIN_HEIGHT = 500

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
    for col in global_map:
        for location in col:
            if isinstance(location, Node):
                players = location.collect_gold(players)
    return players


def fight(global_map):
    return global_map


def spawn_units(global_map, players):
    for col in global_map:
        for location in col:
            if isinstance(location, Node):
                player_gold = location.attempt_spawn(players)
    return global_map, players


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
    players = {
        PlayerColor.NEUTRAL: PlayerInput(PlayerColor.NEUTRAL),
        PlayerColor.BLUE: PlayerInput(PlayerColor.BLUE),
        PlayerColor.RED: PlayerInput(PlayerColor.RED)
    }
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(2)
        run, global_map, players = check_input(global_map, players)
        players = collect_gold(global_map, players)
        global_map = fight(global_map)
        global_map = move_units(global_map)
        global_map, players = spawn_units(global_map, players)
        draw(global_map, win, players)


main()