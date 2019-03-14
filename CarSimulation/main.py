import pygame as pg
import car
from utility import Vector2, Algs, Import
import data as d
import math
import optimizer
import os


def reload():
    """ Start the new generation """
    optimizer.evolve()


def reset():
    """ Reset the population """

    d.cars = d.next_gen
    d.gen_count += 1

    d.fittest_cars = []
    d.shitty_cars = []    
    d.active_car_count = d.POPULATION_COUNT
    d.active_checkp = d.CHECKPOINTS[:]

    d.TXT_ALIVE = "Cars alive : %s" %d.POPULATION_COUNT
    d.TXT_DEAD = "Cars dead : 0"


def draw_text():
    """ Draw the text on the screen """
    d.TXT_ALIVE_RDR = d.FONT.render(d.TXT_ALIVE, 0, d.WHITE)
    d.TXT_DEAD_RDR = d.FONT.render(d.TXT_DEAD, 0, d.WHITE)

    d.TXT_GEN = "Generation : %s" %d.gen_count
    d.TXT_GEN_RDR = d.FONT.render(d.TXT_GEN, 0, d.WHITE)
    d.SURFACE.blit(d.TXT_ALIVE_RDR, (50, 50))
    d.SURFACE.blit(d.TXT_DEAD_RDR, (50, 70))
    d.SURFACE.blit(d.TXT_GEN_RDR, (50, 20))
    pg.display.update()


class Main:
    """ The main class that controls everything """
    def __init__(self):
        pg.init()

        # Update pygame variables
        d.SURFACE = pg.display.set_mode((d.SCREEN_SIZE*2, d.SCREEN_SIZE))
        d.CLOCK = pg.time.Clock()

        if os.path.exists('ExoFont.otf'):
            d.FONT = pg.font.Font("ExoFont.otf", 18)
        else:
            d.FONT = pg.font.Font(None, 18)

        Import.import_json_track('Track.json')

        d.cars = [car.Car() for i in range(d.POPULATION_COUNT)]


    def draw(self):
        """ Draw all the active objects on the screen """
        d.SURFACE.fill((0, 0, 0))

        self.draw_track()
        for car in d.cars:
            car.draw()

        draw_text()        


    def update(self):
        """ Update all the active objects """
        for car in d.cars:
            if not car.dead:
                car.update()
        

    def draw_track(self):
        """ Draw the track """
        pg.draw.aalines(d.SURFACE, d.WHITE, True, d.WALL_IN)
        pg.draw.aalines(d.SURFACE, d.WHITE, True, d.WALL_OUT)
        for checkpoint in d.active_checkp:
            pg.draw.line(d.SURFACE, d.BLUE, checkpoint[0], checkpoint[1])


    def main(self):
        """ Main loop """

        # In what stage the space_key press is
        space_stage = 0

        while True:
            d.CLOCK.tick(60)

            if not d.paused:
                self.update()
            self.draw()

            keys = pg.key.get_pressed()
            if keys[pg.K_ESCAPE]:
                pg.quit()

            # Space = pause
            if keys[pg.K_SPACE]:
                # Space is pressed
                if space_stage == 0:
                    d.paused = not d.paused
                    space_stage = 1

            for event in pg.event.get():
                if event.type == pg.KEYUP:
                    # Space is not pressed anymore
                    if event.key == pg.K_SPACE:            
                        space_stage = 0
                if event.type == pg.QUIT:
                    pg.quit()

        pg.QUIT
