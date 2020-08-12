"""
network.py
~~~~~~~~~~
Moduł implementujący jednokierunkową sieć neuronową. Do uczenia się sieci
wykorzystywane są neurony sigmoidalne, stochastyczny spadek wzdłuż gradientu,
kwadratowa funkcja kosztu oraz algorytm wstecznej propagacji błędów.
Implementacja sieci w tym module jest dosyć prosta, więc jest idealnym
punktem wejścia dla osoby niezaznajomionej z sieciami neuronowymi.
Ulepszoną sieć neuronową, wykorzystującą nowe i bardziej efektywne techniki
znajdziesz w module network2.py
~~~~~~~~~~
"""

#Biblioteki
import random
import numpy as np


class Network(object):

    def __init__(self, sizes):
        """Lista `sizes` zawiera liczby neuronów w kolejnych warstwach.
        Przykładowo, jeśli ta lista to [2, 3, 1]
        powstanie wtedy sieć neuronowa o 3 wastwach, z 2 neuronami w warswie
        wejściowej, 3 w warstwie ukrytej oraz 1 neuronem w warstwie wyjściowej.
        """
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x)
                        for x, y in zip(sizes[:-1], sizes[1:])]

    def feedforward(self, a):
        """Metoda zwracająca wynik sieci neuronowej, gdzie 'a' to dane wejściowe"""
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a) + b)
        return a

    def SGD(self, training_data, epochs, mini_batch_size, eta, app=False,
            test_data=None):
        """Metoda ta służy do nauczenia sieci neuronowej z wykorzystaniem
        stochastycznego spadku wzdłuż gradientu. Dane wejściowe dzielone są
        na mniejsze porcje o rozmiarze określonym przez atrybut mini_batch_size
        Training_data to lista zawierająca dwuelementowe krotki (x,y), gdzie x
        to piksele z obrazka wyjściowego, a y to spodziewany rezultat.
        Argument epochs określa przez ile epok sieć neuronowa będzie się uczyć,
        natomiast eta to współczynnik uczenia się. Jeśli podano test_data
        program wypisze trafność działania sieci po każdej epoce. Jest to dobry sposób
        na śledzenie postępów sieci, ale zwalnia działanie programu."""

        training_data = list(training_data)
        n = len(training_data)

        if test_data:
            test_data = list(test_data)
            n_test = len(test_data)

        for j in range(epochs):
            random.shuffle(training_data)
            mini_batches = [
                training_data[k:k + mini_batch_size]
                for k in range(0, n, mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)
            if test_data:
                if app:
                    return self.network_result(test_data)
                else:
                    print("Epoka {} : {} / {}".format(j, self.evaluate(test_data), n_test))
            else:
                print("Epoka {} complete".format(j))

    def update_mini_batch(self, mini_batch, eta):
        """Metoda aktualizująca wagi i progi w sieci na podstawie jednej porcji danych
        z wykorzystaniem stochastycznego spadku wzdłuż gradientu i algorytmu wstecznej
        propagacji błędów. Argument mini_batch to lista krotek (x, y) - część danych wejściowych
        podanych w funkcji SGD."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weights = [w - (eta / len(mini_batch)) * nw
                        for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b - (eta / len(mini_batch)) * nb
                       for b, nb in zip(self.biases, nabla_b)]

    def backprop(self, x, y):
        """Metoda zwracająca krotkę (nabla_b, nabla_w), która reprezentuje
        gradient funkcji kosztu. Nabla_b oraz nabla_w to listy zawierające
        tablice numpy dla każdej warstwy i odpowiadające wagom i progom w sieci."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # feedforward
        activation = x
        activations = [x]  # lista przechowująca wszystkie wektory aktywacji, warstwa po warstwie
        zs = []  # lista przechowująca wszystkie wektory wejść ważonych, warstwa po warstwie
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        # backward pass
        delta = self.cost_derivative(activations[-1], y) * \
                sigmoid_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l + 1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l - 1].transpose())
        return (nabla_b, nabla_w)

    def evaluate(self, test_data):
        """Metoda zwraca liczbę przypadków testowych, w których sieć neuronowa
        dała poprawny wynik. Jako wynik sieci jest brany indeks neuronu z warstwy
        wyjściowej, który ma największą wartość aktywacji"""
        test_results = [(np.argmax(self.feedforward(x)), y)
                        for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)

    def network_result(self, test_data):
        """Zwraca wynik sieci"""
        test_results = [np.argmax(self.feedforward(x)) for x in test_data]
        return test_results

    def cost_derivative(self, output_activations, y):
        """Metoda zwracająca pochodną funkcji kosztu."""
        return (output_activations - y)


def sigmoid(z):
    """Funkcja sigmoidalna."""
    return 1.0 / (1.0 + np.exp(-z))


def sigmoid_prime(z):
    """Pochodna funkcji sigmoidalnej."""
    return sigmoid(z) * (1 - sigmoid(z))