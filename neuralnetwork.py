# Install necessary libraries:
# pip install scikit-learn numpy
# Uncommment above line and Run it in the terminal window, if you are using jupyter notebook then use !pip install scikit-learn numpy and then run rest of the code

import numpy as np

class NeuralNetwork:
    def __init__(self, input_size, hidden_sizes, output_size):
        """
        Initialize the neural network.

        Parameters:
        - input_size: Number of input features
        - hidden_sizes: List containing the number of neurons in each hidden layer
        - output_size: Number of output classes
        """
        self.input_size = input_size
        self.hidden_sizes = hidden_sizes
        self.output_size = output_size
        self.weights = []
        self.biases = []
        self.activations = []
        
        layer_sizes = [input_size] + hidden_sizes + [output_size]
        
        # Initialize weights and biases for each layer
        for i in range(len(layer_sizes) - 1):
            weight_matrix = np.random.randn(layer_sizes[i], layer_sizes[i+1])
            self.weights.append(weight_matrix)
            bias_vector = np.zeros((1, layer_sizes[i+1]))
            self.biases.append(bias_vector)
            
            # Activation function (using ReLU for hidden layers and softmax for output layer)
            if i < len(layer_sizes) - 2:
                self.activations.append(self.relu)
            else:
                self.activations.append(self.softmax)
                
    def relu(self, x):
        """
        ReLU activation function.
        """
        return np.maximum(0, x)
    
    def softmax(self, x):
        """
        Softmax activation function for output layer.
        """
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)
    
    def forward(self, x):
        """
        Perform forward pass through the neural network.

        Parameters:
        - x: Input data (batch)

        Returns:
        - Output of the neural network
        """
        activations = []
        for i in range(len(self.weights)):
            x = np.dot(x, self.weights[i]) + self.biases[i]
            x = self.activations[i](x)
            activations.append(x)
        return activations[-1]  # Return output layer activation

# Generate synthetic data
num_samples = 1000
input_size = 9
output_size = 4
hidden_sizes = [20, 15, 10]

# Randomly generate input data and labels
X = np.random.randn(num_samples, input_size)

# Create and initialize the neural network
nn = NeuralNetwork(input_size, hidden_sizes, output_size)

# Perform forward pass on a sample input
output = nn.forward(X[0])

print("Sample input:")
print(X[0])
print("Sample output:")
print(output)
