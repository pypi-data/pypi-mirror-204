from network import Network
from utils import process_image, process_mnist, interpret, show


net = Network([784,16,16,10])
net.load_from_file("trained_data.txt")

example = process_image("example.jpeg")
#example = process_mnist()[13][0]
#print(process_mnist()[13][1])

show(example)

answer = net.run(example)

print(interpret(answer))