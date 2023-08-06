# Network object file
#See explanation.txt for code explanations

# SOURCE 
# Math and explanations -->     https://www.3blue1brown.com/topics/neural-networks
# Math and explanati9ns for everything, specifically gradient descent --> http://neuralnetworksanddeeplearning.com/chap1.html
# Numpy documentation -->     https://numpy.org/doc/stable/
# Progress bar  --> https://github.com/rsalmei/alive-progress

import numpy as np 
from alive_progress import alive_bar

class Network():

    # Generate random weights and biases in specific format 
    def generate_data(self, layers_nodes):
        data = list()
        layer_number = 0
        input_layer = layers_nodes.pop(0)
        for layer in layers_nodes:
            layer_data = tuple()
            if layer_number == 0:
                layer_data = (np.random.random((layer, input_layer)), np.random.random((layer, 1)))
            else:
                layer_data = (np.random.random((layer, layers_nodes[layer_number-1])), np.random.random((layer, 1)))
            data.append(layer_data)
            layer_number += 1
        return data


    # Initialization function. Generate all the data weights and biases randomly on object creation and store shape in object if generate argument = true
    def __init__(self, node_structure, generate = True):
        self.input_layer = node_structure[0]
        self.structure = node_structure.copy()
        self.__last_run_activations = list()
        self.__last_run_z = list()
        if generate == True:
            self.data = self.generate_data(node_structure)
            #logging.info("\n\n------------------------------\n\nNETWORK OBJECT CREATED WITH RANDOM WEIGHTS AND BIASES")
        else:
            self.data = None
            #logging.info("NETWORK OBJECT CREATED WITHOUT RANDOM WEIGHTS AND BIASES")
        #logging.info("NETWORK STRUCTURE: \n\tINPUT LAYER: " + str(self.input_layer) + "\n\tHIDDEN LAYERS: " + str(self.structure) + "\n\tOUTPUT LAYER: " + str(node_structure[-1]))


    # Define the sigmoid function
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))


    # Define the derivative of the sigmoid function for Back Propagation
    def sigmoid_derivative(self, x):
        return (self.sigmoid(x) * (1-self.sigmoid(x)))


    # Flatten all data from dictionary format into a vector. (Flatten out data)
    def data_to_vector(self):
        input = self.data
        output = np.empty(0)

        # Flatten the data and append to the vector
        for element in input:
            output = np.append(output, element[0].flatten())

        # Append all biases to the vector
        for element in input:
            output = np.append(output, element[1])
        return output


    # Turn 1 dimensional vector into format used by Network class 
    def vector_to_data(self, vector):
        weights = list()
        layer_number = 0

        # Layer structure without first layer info
        structured = self.structure[1:]

        # For each layer except the first one
        for element in structured:
            if layer_number == 0:
                
                # Get first layer weights
                weights.append(vector[:(self.input_layer*element)].reshape(element,self.input_layer))
                # Remove them from original vector
                vector = vector[(self.input_layer*element):]

            else:
                weights.append(vector[:(structured[layer_number-1]*element)].reshape(element,structured[layer_number-1]))
                vector = vector[(structured[layer_number-1]*element):]
            layer_number += 1
        
        biases = list()

        # Change biases shape
        for element in structured:
            biases.append((vector[:element].reshape(element,1)))
            vector = vector[(element):]

        data = list()
        # Arrange all weights and biases into normal data format. [(weights, biases), (weights, biases), (weights, biases)]
        #                                                               layer1              layer2              layer3
        for layer in range(0, len(weights)):
            data.append((weights[layer], biases[layer]))
        return data

    # Save current (weights and biases) data to a .txt file
    def save_to_file(self, file_name):
        np.savetxt(file_name, self.data_to_vector())
        #logging.info("DATA SAVED TO " + file_name + "\n-----------------------\n")


    # Load data (weights and biases) from specified .txt file
    def load_from_file(self, file_name):
        self.data = self.vector_to_data(np.loadtxt(file_name))
        #logging.info("DATA LOADED FROM " + file_name + "\n------------------------\n")

    # Check the input format of the data (more information in explanation.txt)
    def check(self, weights, values, biases):
        if weights.shape[0] == biases.shape[0]: 
            if weights.shape[1] == values.shape[0]:
                #logging.debug("CHECK OK")
                #logging.debug("\n\n---------------------------\n")
                return True
            else:
                #logging.critical("CHECK FAILED: (weights and values don't match)")
                #logging.debug("\n\n---------------------------\n")
                raise ValueError("Format Check Failed")
        else: 
            #logging.critical("CHECK FAILED: (weights and biases don't match)")
            #logging.debug("\n\n---------------------------\n")
            raise ValueError("Format Check Failed")


    # Run individual layer 
    def layer(self, weights, values, biases):

        # Log process
        #logging.debug("LAYER INFO: \n    Input-Nodes: " + str(weights.shape[1]) + "\n    Output-Nodes:" + str(biases.shape[0]) +"\n")
        #logging.debug("weights: \n" + str(weights) + "\n    values: \n" + str(values) +  "\n    biases: \n" + str(biases))

        # Multiply the matrices and add the biases
        calc = np.add((weights @ values), biases)

        # Store z (activation before sigmoid function) of each layer for back propagation
        self.__last_run_z.append(calc)

        # Apply to sigmoid function to all elementes of matrix
        sigfunc = np.vectorize(self.sigmoid)
        ans = sigfunc(calc)
        
        #logging.debug("ANSWER: \n" + str(ans))
        #logging.debug("\n\n---------------------------\n")
        return ans


    # Main function to run all layers of the network. Only takes input values as argument, and gets others (weights and biases) from self.data
    # Data has the following structure:     [(weights, biases), (weights, biases), (weights, biases)]
    #                                               layer1          layer2              layer3
    def run(self, initial_values):

        self.__last_run_activations = list()
        self.__last_run_z = list()

        data = self.data
        #logging.debug("\n\n ------------------------------------ RUN " + "-------------------------------------------\n")

        # current_values variable is given the first time as user input (activations of the first layer). Then the values are stored from the previous layer. (activations of layers > 1 that are generated by previous layer)
        current_values = initial_values
        layer_number = 0
        layer_outputs = list()

        # Store first layer activations for back propagation
        self.__last_run_activations.append(initial_values)

        # Iterate through each layer of the network
        for layer_data in data:
            layer_number += 1
            # Check and run each layer
            #logging.debug("RUNNING FORMAT CHECK ON LAYER: " + str(layer_number))
            self.check(layer_data[0], current_values, layer_data[1])

            #logging.debug("RUNNING LAYER: " + str(layer_number))
            current_values = self.layer(layer_data[0],  current_values, layer_data[1])
            
            # Store the output of each layer and print the last one (output layer)
            layer_outputs.append(current_values)  

        # Append all activations except for the first layer that is already in list
        self.__last_run_activations = self.__last_run_activations + layer_outputs
        return layer_outputs[-1]


    # Calculate cost of individual run/example. More information in explanation.txt
    def error_for_run(self, expected, output):
        error = output - expected
        
        error = np.sum(np.square(error))
        #logging.debug("COST CALCULATION: \n    Expected:    " + str(expected) + "\n    Output:    " + str(output) + "\n    Error:     " + str(error) + "\n\n---------------------------\n")
        
        return error


    # Cost function of the network
    def cost(self, training_data):
        # Create empty vector to store the error on every run
        error_vector = np.empty(0)

        # Get error for each training example
        for element in training_data:

            # Get vector with output shape to compare. If number is 7 --> (0,0,0,0,0,0,0,1,0,0)
            #                                                       0 1 2 3 4 5 6 7 8 9
            """
            THIS METHOD SHOULD BE CHANGED IF THE OUTPUT FORMAT IS DIFFERENT
            """
            expected = np.zeros(shape=(10, 1))
            np.put(expected, element[1]-1, 1)
            expected.reshape(1,10)
            # Get error of one example
            run_error = self.error_for_run(expected, self.run(element[0].reshape((784,1))))
            # Append error on individual example to total error vector
            error_vector = np.append(error_vector, run_error)
            
        # Average out every element in error vector
        total_error = np.average(error_vector)
        return total_error


    # Back Propagation
    def back_propagation(self, expected_values):

        # Store gradient info from previous layer for backprop
        delta = np.ndarray(0)

        weights_derivatives = np.ndarray(0)
        biases_derivatives = np.ndarray(0)

        # In backporpagation program thinks about the layers backwards
        # Reverse list for backpropagation to start with last layers
        current_data = self.data.copy()
        current_data.reverse()


        # Reverse activations and z for backpropagation
        self.__last_run_activations.reverse()
        self.__last_run_z.reverse()


        # Keep track of layer number BACKWARDS
        layer_number = 0
        
        # First calculate all weights derivatives
        for layer in current_data:
            #print("\n\nLAYER NUMBER: " + str(layer_number))
            # First layer is the base of the rest of the layers and gets calculated differently --> Caluclation of first layer partial derivatives
            if layer_number == 0:
                # Find the DELTA in the first layer derivatives
                for neuron, z, y in zip(self.__last_run_activations[0], self.__last_run_z[0], expected_values):
                    #print("NEURON: " + str(neuron))
                    #print("Z: " + str(z))
                    deriv = (self.sigmoid(z)*(1-self.sigmoid(z)))*2*(neuron-y)
                    delta = np.append(delta, deriv)
                    # Weights are the same as THE NUMBER, so they get stored directly
                    biases_derivatives = np.append(biases_derivatives, deriv)
                    #print("TOTAL: " + str(deriv))
                    # Find the weights
                    for last_layer_neuron in self.__last_run_activations[1]:
                        partial_deriv = deriv * last_layer_neuron
                        weights_derivatives = np.append(weights_derivatives, partial_deriv)
                    
            else:

                current_weights = current_data[layer_number-1][0]
                transposed_weights = np.transpose(current_weights)
                

                
                last_layer_z = self.__last_run_z[layer_number]
                sigfunc_prime = np.vectorize(self.sigmoid_derivative)
                ans = sigfunc_prime(last_layer_z)

                """print("TRANSPOSED WEIGHTS: " + str(transposed_weights.shape))
                print("DELTAS: " + str(delta.reshape(1,-1).shape))
                print(delta.reshape(1,-1))"""


                calc = np.matmul(transposed_weights, delta.reshape(transposed_weights.shape[1],1))
                new_deltas = np.multiply(calc, ans)
                """
                print("FIRST MATRIX MULTIPLICATION: " + str(calc.shape))

                print("FINAL MATRIX MULTIPLICATION: " + str(new_deltas.shape))
                print(new_deltas)"""

                biases_derivatives = np.append(biases_derivatives, new_deltas)

                # Calculate weights
                for neuron in self.__last_run_activations[layer_number+1]:
                    for delta_element in new_deltas:
                        weights_derivatives = np.append(weights_derivatives, (neuron*delta_element))

                # Make the current delta the deltas calculated in this layer
                delta = new_deltas

            # Iterate through layers
            layer_number += 1
        #print(biases_derivatives.shape)
        """print("WEIGHTS CALCULATED: ")
        print(weights_derivatives.shape)
        print("BIASES CALCULATED: ")
        print(biases_derivatives.shape)"""

        # Vector that represesnts the gradient
        gradient_vector = np.append(np.flip(weights_derivatives), np.flip(biases_derivatives))

        return gradient_vector


    # Main function to train the AI
    def train_iterations(self, iterations, training_data, learning_rate):
        #logging.info("NETOWRK TRAINING FOR " + str(iterations) + " ITERATIONS")
        # Use progress bar library
        #print("COST: " + str(self.cost(training_data)))
        with alive_bar(iterations, title="Iterations: ") as bar:
            for iter_number in range(iterations):
                #print("ITERATION: " + str(iter_number))
                #print("COST: " + str(self.cost(training_data)))

                gradient_sum = np.zeros(len(self.data_to_vector()))

                # Run back propagation with every training example and average the gradients
                for training_example in training_data:
                    self.run(training_example[0].reshape((784,1)))
                    expected = list(np.zeros((10,)))
                    expected[training_example[1]] = 1

                    grad_for_example = self.back_propagation(expected)
                    #print(grad_for_example.shape)
                    gradient_sum = gradient_sum + grad_for_example
                   
                # Calculate average gradient
                grad = gradient_sum/len(training_data)
                
                # Gradient descent and save new weights and biases to file every iteration
                self.data = self.vector_to_data(self.data_to_vector() - learning_rate*grad)
            
                bar()
            self.save_to_file("mydata.txt")
            #print("COST: " + str(self.cost(training_data)))
        #logging.info("NETWORK TRAINING FINISHED")