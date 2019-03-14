""" User settings """
solo = False


""" Car Settings """
CAR_WIDTH = 15
CAR_HEIGHT = 25
VELOCITY = 3                    # Speed of the cars
TURN_SPEED = 8                  # How fast the cars turn
ROTATION_THRESHOLD = 500        # How much is the car allowed to rotate without checkpoints

# Sensor settings
SENSOR_LENGTH = 100     # Max length of the sensors
SENSOR_COUNT = 5        # Amount of sensors


""" Colors """
WHITE = (255, 255, 255)
GRAY = (70, 70, 70)
RED = (255, 25, 44)
BLUE = (53, 192, 252)
GREEN = (64, 255, 61)
DARK_GREEN = (31, 84, 36)


""" Text Components """
FONT = None
TXT_ALIVE = "Cars alive : 30"
TXT_ALIVE_RDR = None
TXT_DEAD = "Cars dead : 0"
TXT_DEAD_RDR = None
TXT_GEN = "Generation : 0"
TXT_GEN_RDR = None


""" Population optimizer settings """
POPULATION_COUNT = 15           # Total amount of cars per population

FIT_CARS_COUNT = 3
BEST_CAR_MUTATION_HIGH = 2
BEST_CAR_MUTATION_LOW = 5
SHITTY_CAR_COUNT = 1
RANDOM_CAR_COUNT = 1

# Weight settings
MUTATED_WEIGHTS_COUNT = 40      # Amount of weights to be mutated (single car)

MUTATION_STRENGTH_HIGH = 0.5    # Mutation strength for high mutations
MUTATION_STRENGTH_LOW = 0.2     # Mutation strength for low mutations


""" Neural network settings """
# Amount of input neurons is equal to the amount of sensors each car has

# Hidden layer construction:
#  - Every new integer represents a new hidden layer
#  - with the integer being the amount of neurons e.g. [5, 3] --> 2 hidden layers
HIDDEN_LAYERS = [5]


""" Pygame variables """
SURFACE = None
SCREEN_SIZE = 800       # Screen size is fixed since the imported json file has data of the same dimension
CLOCK = None


""" In-game updated """
paused = False

# Updated after the track import
WALL_IN = None              # Positions of the inner wall
WALL_OUT = None             # Positions of the outer wall
CHECKPOINTS = None          # Positions of the checkpoints
START_POSITION = (0, 0)     # Start positions of the cars

next_gen = []           # List with new cars for the next generation
active_checkp = None
cars = []
best_car = None
fittest_cars = []
shitty_cars = []

gen_count = 0           # What generation the simulation is at
active_car_count = POPULATION_COUNT


""" General """
RESTART_WAIT_TIME = 0.5     # Time to wait after every car died (seconds)