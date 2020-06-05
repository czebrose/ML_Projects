import game
from util import PlayerColor
from simpleplayer import SimplePlayer
from smartplayer import SmartPlayer
from nnplayer import NNetPlayer
from humanplayer import HumanPlayerInput


blue_player = NNetPlayer.create_feedforward_from_pickle("best-vs-self-feedforward.pickle",
                                                        "config.feedforward.txt",
                                                        PlayerColor.BLUE)
red_player = SimplePlayer(PlayerColor.RED)

map_files = ["map_0.txt"]
show_window = True
run_count = 1
wins = {PlayerColor.BLUE: 0, PlayerColor.RED: 0}


def main():
    winning_players = []
    players = {
        PlayerColor.BLUE: blue_player,
        PlayerColor.RED: red_player
    }
    for map_iter in map_files:
        global_map, players, fights, winning_player = game.init_game(map_iter, players)
        for _ in range(run_count):
            winner, global_map = game.run_game(show_window, global_map, players, fights, winning_player)
            winning_players.append(winner)
            wins[winner] += 1
    print(wins)
    print(winning_players)


main()
