from util import PlayerColor
from simpleplayer import SimplePlayer
from node import Node
import neat
import os
import pickle
import game
from nnplayer import NNetPlayer
import nnutil


neural_net_type = neat.nn.FeedForwardNetwork
config_filename = "config.feedforward.txt"
map_filename = "map_0.txt"
pickle_save_file = "best-vs-self-feedforward.pickle"
max_generations = 50
max_game_time = 100


def train_net_vs_simple(net_player):
    net_player.color = PlayerColor.BLUE
    players = {
        PlayerColor.BLUE: net_player,
        PlayerColor.RED: SimplePlayer(PlayerColor.RED)
    }
    global_map, players, fights, winning_player = game.init_game(map_filename, players)
    winner, global_map = game.run_game(False, global_map, players, fights, winning_player)

    owned_nodes = 0
    owned_buildings = 0
    owned_units = 0
    for row in global_map:
        for loc in row:
            if loc and loc.unit_in_loc and loc.unit_in_loc.owner is net_player.color:
                owned_units += 1
            if isinstance(loc, Node):
                if loc.owner is net_player.color:
                    owned_nodes += 1
                    if not loc.building.is_empty():
                        owned_buildings += 1
    net_player.g.fitness = owned_units + 10 * owned_nodes + 20 * owned_buildings
    if winner is net_player.color:
        net_player.g.fitness += 10000
    print("Genome: ", net_player.g.key, " Fitness: ", net_player.g.fitness)


def train_net_vs_other(net_player, other_net_player):
    net_player.color = PlayerColor.BLUE
    other_net_player.color = PlayerColor.RED
    players = {
        PlayerColor.BLUE: net_player,
        PlayerColor.RED: other_net_player
    }
    global_map, players, fights, winning_player = game.init_game(map_filename, players)
    winner, global_map = game.run_game(False, global_map, players, fights, winning_player, max_game_time)

    for row in global_map:
        for loc in row:
            if loc and loc.unit_in_loc:
                if loc.unit_in_loc.owner is net_player.color:
                    net_player.g.fitness += 1
                elif loc.unit_in_loc.owner is other_net_player.color:
                    other_net_player.g.fitness += 1
            if isinstance(loc, Node):
                if not loc.building.is_empty():
                    if loc.owner is net_player.color:
                        net_player.g.fitness += 100
                    elif loc.owner is other_net_player.color:
                        other_net_player.g.fitness += 100
    if players.__contains__(winner):
        players[winner].g.fitness += 1000
    print("Genome: ", net_player.g.key, " Fitness: ", net_player.g.fitness,
          "\tOther Genome: ", other_net_player.g.key, " Fitness: ", other_net_player.g.fitness)
    return winner


def play_league(net_players):
    while len(net_players) > 1:
        first_nn = net_players.pop(0)
        second_nn = net_players.pop(0)
        print("First Genome: ", first_nn.g.key, " Second Genome: ", second_nn.g.key)
        first_winner = train_net_vs_other(first_nn, second_nn)
        second_winner = train_net_vs_other(second_nn, first_nn)
        if first_winner is second_winner:
            # No one wins
            if first_nn.g.fitness > second_nn.g.fitness:
                print("Tie goes to First Genome Key #", first_nn.g.key)
                net_players.append(first_nn)
            elif second_nn.g.fitness > first_nn.g.fitness:
                print("Tie goes to Second Genome Key #", second_nn.g.key)
                net_players.append(second_nn)
            else:
                print("Tie, no one wins")
        elif first_winner is PlayerColor.BLUE or second_winner is PlayerColor.RED:
            print("First Genome Won Key #", first_nn.g.key)
            net_players.append(first_nn)
        else:
            print("Second Genome Won Key #", second_nn.g.key)
            net_players.append(second_nn)


def main(genomes, config):
    net_players = []
    for _, g in genomes:
        net = neural_net_type.create(g, config)
        g.fitness = 0
        net_players.append(NNetPlayer(g, net))
    play_league(net_players)


def run(config_path):
    config = nnutil.get_config(config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(main, max_generations)
    with open(pickle_save_file, "wb") as f:
        pickle.dump(winner, f)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_filepath = os.path.join(local_dir, config_filename)
    run(config_filepath)
