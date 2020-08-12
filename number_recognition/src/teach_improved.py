import src.mnist_loader as mnist_loader
import src.network2 as network2

training_data, validation_data, test_data = mnist_loader.load_data_wrapper()
net = network2.Network([784, 30, 10], cost=network2.CrossEntropyCost)
net.SGD(training_data, 5, 10, 0.1, lmbda=0, evaluation_data=list(validation_data)[:100], monitor_evaluation_accuracy=True,
            monitor_training_cost=True)
#net.save('../data/network_params')