## from https://medium.com/towards-data-science/math-neural-network-from-scratch-in-python-d6da9f29ce65
# Base Class

class layer:
    def __init__(self):
        self.input = None
        self.output = None
        
    # computes Y of a layer for a given X at that layer
    def forward_prop(self, input):
        raise NotImplementedError
    
    # computes dE/dX for a given DE/dY and updates parameters
    def backward_prop(self, output_error, learning_rate):
        raise NotImplementedError
    

import numpy as np

# inherit from base class Layer
class FCLayer(Layer):
    # input_size = number of input neurons
    # output_size = number of output neurons
    def __init__(self, input_size, output_size):
        self.weights = np.random.rand(input_size, output_size) - 0.5
        self.bias = np.random.rand(1, output_size) - 0.5
        
    # returns output for a given input
    def forward_prop(self, input_data):
        self.input = input_data
        self.output = np.dot(self.input, self.weights) + self.bias
        return self.output
    
    # computes dE/dW, dE/dB for a given output_error=dE/dY. Returns input_error=dE/dX.
    def backward_prop(self, output_error, learning_rate):
        input_error = np.dot(output_error, self.weights.T)
        weights_error = np.dot(self.input.T, output_error)
        
        # update parameters
        self.weights -= learning_rate * weights_error
        self.bias -= learning_rate * output_error
        return input_error