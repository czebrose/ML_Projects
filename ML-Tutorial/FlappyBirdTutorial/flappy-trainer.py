import pygame
import neat
import time
import os
import random
import pickle
import flappygame
from flappygame import Bird, Pipe, Base


def main(genomes, config):
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        g.fitness = 0
        birds.append(Bird(230, 350, g, net))

    base = Base(730)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((flappygame.WIN_WIDTH, flappygame.WIN_HEIGHT))
    clock = pygame.time.Clock()
    run = True

    score = 0

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        if len(birds) <= 0:
            run = False
            break
        else:
            for bird in birds:
                bird.update(pipes)

        pipe_added = flappygame.update_pipes(pipes, birds)
        if pipe_added:
            score += 1

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() > 730 or bird.y < 0:
                birds.pop(x)

        if score > 500:
            break

        base.move()
        flappygame.draw_window(win, birds, pipes, base, score)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)

    with open("best-flapper.pickle", "wb") as f:
        pickle.dump(winner, f)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.feedforward.txt")
    run(config_path)