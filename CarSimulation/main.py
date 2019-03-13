import pygame
import car
from utility import Vector2, Algs, Import
import data as d
import math
import optimizer
import os

update = True

def reload():
    update = False
    optimizer.evolve()

def reset():
    d.cars = d.next_gen
    d.gen_count += 1

    d.fittest_cars = []
    d.shitty_cars = []    
    d.active_car_count = d.POPULATION_COUNT
    d.active_checkp = d.CHECKPOINTS[:]

    d.TXT_ALIVE = "Cars alive : %s" %d.POPULATION_COUNT
    d.TXT_DEAD = "Cars dead : 0"

    update = True

def update_text():
    d.TXT_ALIVE_RDR = d.FONT.render(d.TXT_ALIVE, 0, d.WHITE)
    d.TXT_DEAD_RDR = d.FONT.render(d.TXT_DEAD, 0, d.WHITE)

    d.TXT_GEN = "Generation : %s" %d.gen_count
    d.TXT_GEN_RDR = d.FONT.render(d.TXT_GEN, 0, d.WHITE)
    d.SURFACE.blit(d.TXT_ALIVE_RDR, (50, 50))
    d.SURFACE.blit(d.TXT_DEAD_RDR, (50, 70))
    d.SURFACE.blit(d.TXT_GEN_RDR, (50, 20))
    pygame.display.update()

class Main:
    def __init__(self):
        pygame.init()
        d.SCREEN_SIZE = 800
        d.SURFACE = pygame.display.set_mode((d.SCREEN_SIZE, d.SCREEN_SIZE))

        if os.path.exists('ExoFont.otf'):
            d.FONT = pygame.font.Font("ExoFont.otf", 18)
        else:
            d.FONT = pygame.font.Font(None, 18)

        Import.import_json_track('Track.json')

        self.clock = pygame.time.Clock()
        d.cars = [car.Car() for i in range(d.POPULATION_COUNT)]

    def draw(self):
        d.SURFACE.fill((0, 0, 0))

        self.draw_track()
        for car in d.cars:
            if not car.dead:
                car.update()
                car.move()
            car.draw()

        update_text()

    def draw_track(self):
        pygame.draw.aalines(d.SURFACE, d.WHITE, True, d.WALL_IN)
        pygame.draw.aalines(d.SURFACE, d.WHITE, True, d.WALL_OUT)
        for checkpoint in d.active_checkp:
            pygame.draw.line(d.SURFACE, d.BLUE, checkpoint[0], checkpoint[1])

    def main(self):
        while update:
            self.clock.tick(60)
            self.draw()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

        pygame.QUIT
