import pygame
import os
import random
pygame.font.init()


WIN_WIDTH = 600
WIN_HEIGHT = 800


def load_img(img_name):
    return pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", img_name)))


BIRD_IMGS = [load_img("bird1.png"), load_img("bird2.png"), load_img("bird3.png")]
PIPE_IMG = load_img("pipe.png")
BASE_IMG = load_img("base.png")
BG_IMG = load_img("bg.png")

STAT_FONT = pygame.font.SysFont("comicsans", 50)


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y, ge, nn):
        self.x = x
        self.y = y
        self.ge = ge
        self.nn = nn
        self.pipe_x = 0
        self.pipe_height = 0
        self.pipe_bottom = 0
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        if d >= 16:
            d = 16
        if d < 0:
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def update(self, pipes):
        self.move()
        self.ge.fitness += 0.1

        for pipe in pipes:
            if pipe.x > self.x:
                self.pipe_x = pipe.x
                self.pipe_height = pipe.height
                self.pipe_bottom = pipe.bottom
                break

        dist_to_top_pipe = abs(self.y - self.pipe_height)
        dist_to_bottom_pipe = abs(self.y - self.pipe_bottom)
        output = self.nn.activate((self.y, dist_to_top_pipe, dist_to_bottom_pipe))

        if output[0] > 0.5:
            self.jump()

    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)
        pygame.draw.line(win, (255, 0, 0), (self.x, self.y), (self.pipe_x, self.pipe_height), 5)
        pygame.draw.line(win, (255, 0, 0), (self.x, self.y), (self.pipe_x, self.pipe_bottom), 5)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        return bool(t_point or b_point)


class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
        self.x3 = self.WIDTH*2

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        self.x3 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x3 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

        if self.x3 + self.WIDTH < 0:
            self.x3 = self.x2 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
        win.blit(self.IMG, (self.x3, self.y))


def draw_window(win, birds, pipes, base, score):
    win.blit(BG_IMG, (0, 0))
    win.blit(BG_IMG, (BG_IMG.get_width(), 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)

    for bird in birds:
        bird.draw(win)
    pygame.display.update()


def update_pipes(pipes, birds):
    add_pipe = False
    rem = []
    for pipe in pipes:
        for x, bird in enumerate(birds):
            if pipe.collide(bird):
                bird.ge.fitness -= 1
                birds.pop(x)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if pipe.x + pipe.PIPE_TOP.get_width() < 0:
            rem.append(pipe)

        pipe.move()

    if add_pipe:
        for bird in birds:
            bird.ge.fitness += 5
        pipes.append(Pipe(700))

    for pipe in rem:
        pipes.remove(pipe)

    return add_pipe
