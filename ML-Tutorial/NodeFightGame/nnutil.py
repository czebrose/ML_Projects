import pickle
import neat
import os


def get_config(config_filename):
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, config_filename)
    return neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                              neat.DefaultSpeciesSet, neat.DefaultStagnation,
                              config_path)


def get_genome(pickle_filename):
    pickle_in = open(pickle_filename, "rb")
    pickle_ge = pickle.load(pickle_in)
    return pickle_ge
