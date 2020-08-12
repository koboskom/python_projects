import src.mnist_loader as mnist_loader
import src.network as network

training_data, validation_data, test_data = mnist_loader.load_data_wrapper()
net = network.Network([784, 30, 10])
net.SGD(training_data, 30, 10, 9.0, test_data=test_data)
