import random
from utility import sigmoid, sum_matrix_float,clamp
import numpy as np
import data as d

class NeuralNetWork:
    def __init__(self, input, h_layers, output):
        self.input_len = input
        self.output_len = output
        self.h_layers = h_layers
        self.weights = []
        self.biases = []
        self.setup_weights()
        self.setup_biases()

    def setup_weights(self):
        # Add for every layer their length
        layers_len = [self.input_len]
        for i in range(len(self.h_layers)):
            layers_len.append(self.h_layers[i])
        layers_len.append(self.output_len)

        for i in range(len(layers_len)-1):
            # Add layers
            self.weights.append([])
            for _ in range(layers_len[i]):
                # Add inputs with weights
                self.weights[i].append([random.uniform(-1, 1) for _ in range(layers_len[i+1])])

    def setup_biases(self):
        # There is a bias for every hidden layer and for the input layer
        self.biases = [random.uniform(-1, 1) for _ in range(len(self.h_layers) + 1)]

    def forward_prop(self, inputs):
        layers = [inputs]
        for i in range(len(self.h_layers)+1):
            # Calculate the input * weights + bias
            z = sum_matrix_float(np.dot(layers[i], self.weights[i]), self.biases[i])
            # Apply activation function
            o = [sigmoid(clamp(-20, 20, z[j])) for j in range(len(z))]
            layers.append(o)
        # Return the output
        final_output = layers[len(layers)-1][0]
        return final_output
        