import data as d
import random
import math
from utility import clamp
from neural_net import NeuralNetWork
from car import Car
import main
import copy

def evolve():
    d.NEXT_GEN = []

    # Keep the best car
    net_best = copy.deepcopy(d.best_car.neural_net)
    d.NEXT_GEN.append(Car(net_best))

    # Make strong mutations from the best car
    for _ in range(d.BEST_CAR_MUTATION_HIGH):
        net = copy.deepcopy(d.best_car.neural_net)
        net = mutate(net, True)
        d.NEXT_GEN.append(Car(net))

    # Make small mutation from the best car
    for _ in range(d.BEST_CAR_MUTATION_LOW):
        net = copy.deepcopy(d.best_car.neural_net)
        net = mutate(net, False)
        d.NEXT_GEN.append(Car(net))
        
    # Make mutations from the shitty cars
    for i in range(d.SHITTY_CAR_COUNT):
        net = copy.deepcopy(d.shitty_cars[i].neural_net)
        net = mutate(net, True)
        d.NEXT_GEN.append(Car(net))

    # Make a few randoms
    for i in range(d.RANDOM_CAR_COUNT):
        net = NeuralNetWork(d.SENSOR_COUNT, d.HIDDEN_LAYERS, 1)
        d.NEXT_GEN.append(Car(net))

    # Cross-Breed the rest of the population
    children = []
    breed_count = d.POPULATION_COUNT - len(d.NEXT_GEN)
    for _ in range(breed_count):
        mom = d.fittest_cars[random.randint(0, len(d.fittest_cars)-1)]
        dad = mom
        # Make sure the two parent are different
        while dad == mom:
            dad = d.fittest_cars[random.randint(0, len(d.fittest_cars)-1)] 

        net = breed(mom.neural_net, dad.neural_net)
        children.append(net)

    # Mutate half of the crossed children
    for i in range(int(len(children)/2)):
        children[i] = mutate(children[i], True)
    
    # Add the children to the population
    for i in range(len(children)):
        d.NEXT_GEN.append(Car(children[i]))

    d.cars = d.NEXT_GEN
    d.gen_count += 1
    main.reset()

def breed(mom, dad):
    # Make the child an empty neural network
    child = NeuralNetWork(d.SENSOR_COUNT, d.HIDDEN_LAYERS, 1)
    # weights
    for i in range(len(child.weights)):
        for j in range(len(child.weights[i])):
            for k in range(len(child.weights[i][j])):
                # Random value between mom's and dad's weights
                child.weights[i][j][k] = random.uniform(mom.weights[i][j][k], dad.weights[i][j][k])
    # biases
    for i in range(len(child.biases)):
        child.biases[i] = random.uniform(mom.biases[i], dad.biases[i])

    return child

def mutate(net, _strong):
    b = net.biases
    w = net.weights
    #weights
    w_new = net.weights
    for _ in range(d.MUTATED_WEIGHTS_COUNT):
        layer_i = random.randint(0, len(w)-1)
        input_i = random.randint(0, len(w[layer_i])-1)
        weigth_i = random.randint(0, len(w[layer_i][input_i])-1)
        _w = w[layer_i][input_i][weigth_i]

        if(_strong):
            mut_strength = d.MUTATION_STRENGTH_HIGH
        else:
            mut_strength = d.MUTATION_STRENGTH_LOW

        w_new[layer_i][input_i][weigth_i] = clamp(-1.5, 1.5, (_w + random.uniform(-mut_strength, mut_strength)))
    net.weights = w_new
    #biases
    b_index = random.randint(0, len(b)-1)
    b[b_index] += random.uniform(-mut_strength, mut_strength)
    net.biases = b

    return net