# Utilty functions to process images for the network

from PIL import Image
from numpy import array
import matplotlib.pyplot as plt

from idx2numpy import convert_from_file

# Function to change image format for the network
def process_image(filename):
    with Image.open(filename) as img:
        img.load()
        img = img.resize((28,28)) 
        img = img.convert("L") # Convert to grayscale
        img_matrix = array(img) # Convert to numpy array
        img_matrix = (1/255)*img_matrix # Change from 0-255 to 0-1
        img_matrix = 1 - img_matrix # Invert color values
        img_matrix = img_matrix.flatten() # Turn 2d matrix into 1d vector

        return img_matrix.reshape((784,1))


# Function to get the images from MNIST database
def process_mnist(test=False):
    # Choose between big and small dataset
    if test:
        imagefile = 'training/MNIST/small/t10k-images-idx3-ubyte'
        labelsfile = 'training/MNIST/small/t10k-labels-idx1-ubyte'
    else:
        imagefile = 'training/MNIST/big/train-images.idx3-ubyte'
        labelsfile = 'training/MNIST/big/train-labels.idx1-ubyte'
    
    # Retrieve data from ubyte file
    imagearray = convert_from_file(imagefile)
    labelsarray = convert_from_file(labelsfile)

    # Change data format (Range 0-255) to decimal (Range 0-1)
    processed_imagearray = (1/255)*imagearray

    # List of 784*1 numpy arrays (vector) containing number data
    images = list()
    for i in processed_imagearray:
        images.append(i.flatten().reshape((-1,1)))

    # Final training data
    training_data = list()

    # Transfrom to the following data structure: (np.array(784*1), int)
    for i in range(0, len(images)):
        training_data.append((images[i],labelsarray[i]))

    return training_data

# Function to read netowrk output vector and show index of maximum value
def interpret(input_array):
    input_array = list(input_array)
    answer = input_array.index(max(input_array))
    return answer

# Funciton to show MNIST/Image with matplotlib
def show(img_vector):
    img_matrix = img_vector.reshape((28,28))
    plt.imshow(img_matrix, cmap=plt.cm.binary) # Show matplotlib 
    plt.show()