import pygame
import neat
import time
import os
import random
import pickle
import game
from nnplayer import NNetPlayer


def main(genomes, config):
    net_players = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        g.fitness = 0
        net_players.append(NNetPlayer(g, net))

    for np in net_players:
        game.train_net(np)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 5)

    with open("best-node-net.pickle", "wb") as f:
        pickle.dump(winner, f)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_filepath = os.path.join(local_dir, "config.feedforward.txt")
    run(config_filepath)