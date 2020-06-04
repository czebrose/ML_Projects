import game
import json


class LocationEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            return o.name
        return json.JSONEncoder.default(self, o)


def reward(state):
    return 0


class State:
    def __init__(self, global_map_arg, players_arg, fights_arg, winning_player_arg):
        self.global_map = global_map_arg
        self.players = players_arg
        self.fights = fights_arg
        self.winning_player = winning_player_arg
        self.json_dump = json.dumps([global_map_arg], cls=LocationEncoder)


class Transition:
    pass


class Action:
    pass


def add_next_states(s):
    if states.__contains__(s.json_dump):
        return
    else:
        states[s.json_dump] = 0
        run, gm, p = game.check_input(s.global_map, s.players)
        gm, p, f, wp = game.update_game(gm, p, s.fights, s.winning_player)
        new_state = State(gm, p, f, wp)
        add_next_states(new_state)


states = {}
global_map, players, fights, winning_player = game.init_game("map_0.txt")
init_state = State(global_map, players, fights, winning_player)
add_next_states(init_state)
for state in states:
    print(state)
