import pygame
import math
import json
import utility

WALL_IN = None
WALL_OUT = None
WALL_I_EXT = None
WALL_O_EXT = None
CHECKPOINTS = None
START_POSITION = (0, 0)

POPULATION_COUNT = 30
BEST_CAR_MUTATION_HIGH = 7
BEST_CAR_MUTATION_LOW = 7
SHITTY_CAR_COUNT = 5
RANDOM_CAR_COUNT = 3

RESTART_WAIT_TIME = 0.5

MUTATED_WEIGHTS_COUNT = 40
MUTATION_STRENGTH_HIGH = 0.5
MUTATION_STRENGTH_LOW = 0.2

# Amount of cars that will be used to breed
FIT_CARS_COUNT = 8

next_gen = []

active_checkp = None
cars = []
best_car = None
fittest_cars = []
shitty_cars = []

gen_count = 0
active_car_count = POPULATION_COUNT

SURFACE = None
SCREEN_SIZE = None

CAR_WIDTH = 15
CAR_HEIGHT = 25
SENSOR_LENGTH = 100

SENSOR_COUNT = 5
HIDDEN_LAYERS = [5]

VELOCITY = 3
TURN_SPEED = 8

ROTATION_THRESHOLD = 500

WHITE = (255, 255, 255)
GRAY = (70, 70, 70)
RED = (255, 25, 44)
BLUE = (53, 192, 252)
GREEN = (64, 255, 61)
DARK_GREEN = (31, 84, 36)

FONT = None
TXT_ALIVE = "Cars alive : 30"
TXT_ALIVE_RDR = None
TXT_DEAD = "Cars dead : 0"
TXT_DEAD_RDR = None
TXT_GEN = "Generation : 0"
TXT_GEN_RDR = None