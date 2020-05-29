import pygame
import util
import debug
import os
from util import Direction, PlayerColor
from humanplayer import HumanPlayerInput
from simpleplayer import SimplePlayer
from node import Node, Building
from road import Road
pygame.font.init()


WIN_WIDTH = 1800
WIN_HEIGHT = 1000

FPS = 60
# The time between game updates in milliseconds.
GAME_UPDATE_TIME = 500

BACKGROUND_IMG = util.load_img("background.png")

VICTORY_FONT = pygame.font.SysFont("comicsans", 50)


def check_input(global_map, players):
    if pygame.get_init():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                return False, global_map, players
    debug.check_input()
    thoughts = ""
    for p in players:
        global_map, thought = players[p].check_input(global_map)
        thoughts = thoughts + thought
    print(thoughts)
    return True, global_map, players


def collect_gold(global_map, players):
    for row in global_map:
        for location in row:
            if isinstance(location, Node):
                players = location.collect_gold(players)
    return players


def diffuse(global_map):
    for row in global_map:
        for location in row:
            if location:
                location.diffuse()
    return global_map


def fight(global_map, fights):
    for row in global_map:
        for location in row:
            if isinstance(location, Node):
                fights.extend(location.fight())
    for row in global_map:
        for location in row:
            if location:
                fights.extend(location.fight())
    return global_map, fights


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


def update_fights(fights):
    index = 0
    while index < len(fights):
        fights[index].update()
        if fights[index].should_remove():
            fights.pop(index)
        else:
            index = index + 1
    return fights


def get_existing_homes(global_map, players):
    home_exists = {}
    for p in players:
        home_exists[p] = False

    for map_row in global_map:
        for location in map_row:
            if location:
                for p in players:
                    home_exists[p] = home_exists[p] or location.is_home_node(p)
    for p in players:
        if not home_exists[p]:
            home_exists.pop(p)
    return home_exists


def draw(global_map, win, players, fights, update=True):
    bg_x = 0
    bg_y = 0
    while bg_y < WIN_HEIGHT:
        while bg_x < WIN_WIDTH:
            win.blit(BACKGROUND_IMG, (bg_x, bg_y))
            bg_x = bg_x + util.BG_WIDTH
        bg_x = 0
        bg_y = bg_y + util.BG_HEIGHT
    for map_row in global_map:
        for location in map_row:
            if location:
                location.draw(win)
    for map_row in global_map:
        for location in map_row:
            if location:
                location.draw_unit(win)
    for p in players:
        players[p].draw(win)
    for f in fights:
        f.draw(win)
    debug.draw(win, global_map)
    if update:
        pygame.display.update()


def draw_victory(winning_player, win):
    color = (255, 255, 255)
    if winning_player == PlayerColor.BLUE:
        color = (0, 0, 255)
    elif winning_player == PlayerColor.RED:
        color = (255, 0, 0)
    text = VICTORY_FONT.render("Winner: " + str(winning_player), 1, color)
    x = (WIN_WIDTH / 2) - (text.get_width() / 2)
    y = (WIN_HEIGHT / 2) - (text.get_height() / 2)
    win.blit(text, (x, y))
    pygame.display.update()


def build_map():
    new_map = [[]]
    map_file = open("map_1.txt", "r")
    map_file_contents = map_file.read()
    x_index = 0
    y_index = 0
    for c in map_file_contents:
        if c == 'N' or c == 'M' or c == 'B' or c == 'R':
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
                if y < len(new_map) - 1 and new_map[y+1]:
                    south_loc = new_map[y+1][x]
                    if south_loc:
                        location.add_neighbor(Direction.SOUTH, south_loc)
    return new_map


def update_game(global_map, players, fights, winning_player):
    players = collect_gold(global_map, players)
    fights = update_fights(fights)
    global_map = diffuse(global_map)
    global_map, fights = fight(global_map, fights)
    global_map = move_units(global_map)
    global_map, players = spawn_units(global_map, players)
    home_exists = get_existing_homes(global_map, players)
    if len(home_exists) == 1:
        winning_player, _ = home_exists.popitem()
    elif len(home_exists) <= 0:
        winning_player = PlayerColor.NEUTRAL
    return global_map, players, fights, winning_player


def run_with_window(global_map, players, fights, winning_player):
    pygame.init()
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (30, 30)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    tick_counter = 0
    run = True
    while not winning_player and run:
        clock.tick(FPS)
        run, global_map, players = check_input(global_map, players)
        tick_counter += clock.get_time()
        if tick_counter > GAME_UPDATE_TIME:
            tick_counter = 0
            global_map, players, fights, winning_player = update_game(global_map, players, fights, winning_player)
        draw(global_map, win, players, fights)
    return win, clock, run, winning_player


def show_win_screen(win, clock, run, global_map, players, fights, winning_player):
    while run:
        clock.tick(FPS)
        run, global_map, players = check_input(global_map, players)
        draw(global_map, win, players, fights, False)
        draw_victory(winning_player, win)


def main(show_window):
    global_map = build_map()
    players = {
        PlayerColor.BLUE: SimplePlayer(PlayerColor.BLUE),
        PlayerColor.RED: SimplePlayer(PlayerColor.RED)
    }
    fights = []
    winning_player = None
    run = True
    if show_window:
        win, clock, run, winning_player = run_with_window(global_map, players, fights, winning_player)
        show_win_screen(win, clock, run, global_map, players, fights, winning_player)
    else:
        while not winning_player and run:
            run, global_map, players = check_input(global_map, players)
            global_map, players, fights, winning_player = update_game(global_map, players, fights, winning_player)
    return winning_player


winning_players = []
show_window = True
for _ in range(1):
    winning_players.append(main(show_window))
print(winning_players)
