import pickle
import neat
import pygame
import os
import flappygame
from flappygame import Bird, Pipe, Base


def main():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.feedforward.txt")
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    pickle_in = open("best-flapper.pickle", "rb")
    winner = pickle.load(pickle_in)
    net = neat.nn.FeedForwardNetwork.create(winner, config)
    birds = [Bird(230, 350, winner, net)]

    base = Base(730)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((flappygame.WIN_WIDTH, flappygame.WIN_HEIGHT))
    clock = pygame.time.Clock()
    run = True

    score = 0

    while run:
        clock.tick(300)
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


main()