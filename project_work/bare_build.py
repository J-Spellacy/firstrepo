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
    
    