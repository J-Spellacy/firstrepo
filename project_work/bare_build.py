## imports

import numpy as np

## to do

# create classes in order to contribute to final class of NN


## bugs


## classes and functions

class Neuron:
    def __init__(self):
        self.activation = None
        self.weight_prev = None
        self.bias_prev = None
        self.weight_next = None
        self.bias_next = None
        

class Layer:
    def __init__(self, size: int):
        self.nodes =  np.zeros((size, 1))
        for i in range(size):
            self.nodes[i][0] = Neuron
        self.output = None
        
    # computes Y of a layer for a given X at that layer
    def forward_prop(self, input):
        # matrix multiply with weights and biases from previous layer
        output = None
        return output
    
    # computes dE/dX for a given DE/dY and updates parameters
    def backward_prop(self, output_error, learning_rate):
        raise NotImplementedError
    
## main function

def main():
    pass

## running code
if __name__ == 'main':
    main()