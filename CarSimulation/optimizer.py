import data as d
import random
import math
from utility import clamp
from neural_net import NeuralNetWork
from car import Car
import main
import copy

def evolve():
    """ Generate a new population based on the result of the earlier one """
    d.next_gen = []

    """ Keep the best car """
    net_best = copy.deepcopy(d.best_car.neural_net)
    d.next_gen.append(Car(net_best))

    """ Make strong mutations from the best car """
    for _ in range(d.BEST_CAR_MUTATION_HIGH):
        net = copy.deepcopy(d.best_car.neural_net)
        net = mutate(net, True)
        d.next_gen.append(Car(net))

    """ Make small mutation from the best car """
    for _ in range(d.BEST_CAR_MUTATION_LOW):
        net = copy.deepcopy(d.best_car.neural_net)
        net = mutate(net, False)
        d.next_gen.append(Car(net))
        
    """ Make mutations from the shitty cars """
    for i in range(d.SHITTY_CAR_COUNT):
        net = copy.deepcopy(d.shitty_cars[i].neural_net)
        net = mutate(net, True)
        d.next_gen.append(Car(net))

    """ Make a few randoms """
    for i in range(d.RANDOM_CAR_COUNT):
        # A new instance of a NN is always random
        net = NeuralNetWork(d.SENSOR_COUNT, d.HIDDEN_LAYERS, 1)
        d.next_gen.append(Car(net))

    """ Cross-Breed the rest of the population """
    children = []
    breed_count = d.POPULATION_COUNT - len(d.next_gen)
    for _ in range(breed_count):
        # Find parents
        mom = d.fittest_cars[random.randint(0, len(d.fittest_cars)-1)]
        dad = mom
        # Make sure the two parent are different
        while dad == mom:
            dad = d.fittest_cars[random.randint(0, len(d.fittest_cars)-1)] 

        # Make children
        net = breed(mom.neural_net, dad.neural_net)
        children.append(net)

    # Mutate half of the crossed children
    for i in range(int(len(children)/2)):
        children[i] = mutate(children[i], True)
    
    # Add the children to the population
    for i in range(len(children)):
        d.next_gen.append(Car(children[i]))

    """ Start a new simulation with the new population """
    main.reset()

def breed(mom, dad):
    """ Breed two neural networks """
    child = NeuralNetWork(d.SENSOR_COUNT, d.HIDDEN_LAYERS, 1)

    """ weights """
    for i in range(len(child.weights)):
        for j in range(len(child.weights[i])):
            for k in range(len(child.weights[i][j])):
                # Every weight of the child is a random value between
                # the corresponding weight of its mom and dad
                child.weights[i][j][k] = random.uniform(mom.weights[i][j][k], dad.weights[i][j][k])

    """ biases """
    for i in range(len(child.biases)):
        # Bias of the child is a random value between
        # the corresponding bias of its mom and dad
        child.biases[i] = random.uniform(mom.biases[i], dad.biases[i])

    return child

def mutate(net, strong):
    """ Mutate a neural network\n
        Parameters: \n
        \tnet = the neural net to mutate
        \tstrong = whether or not the mutation should be strong"""
    b = net.biases
    w = net.weights

    """ weights """
    w_new = net.weights
    for _ in range(d.MUTATED_WEIGHTS_COUNT):
        # Find a random weight
        layer_i = random.randint(0, len(w)-1)
        input_i = random.randint(0, len(w[layer_i])-1)
        weigth_i = random.randint(0, len(w[layer_i][input_i])-1)
        _w = w[layer_i][input_i][weigth_i]

        # How strong should the weight be mutated
        if(strong):
            mut_strength = d.MUTATION_STRENGTH_HIGH
        else:
            mut_strength = d.MUTATION_STRENGTH_LOW

        # Mutate the weight (weights are always clamped between -1.5 and 1.5)
        rd = random.uniform(-mut_strength, mut_strength)
        w_new[layer_i][input_i][weigth_i] = clamp(-1.5, 1.5, (_w + rd))

    net.weights = w_new

    """ biases """
    index = random.randint(0, len(b)-1)
    b[index] += random.uniform(-mut_strength, mut_strength)
    net.biases = b

    return net