"""
network2.py
~~~~~~~~~~~~~~
Ulepszona wersja network.py. W porównaniu do network py dodano
entropię krzyżową jako funkcję kosztu, regularyzację wag oraz efektywniejsze
inicjalizowanie wag. Mimo ulepszeń w porówaniu do network.py nie wykorzystano
wielu technik mogącyh poprawić wydajność sieci.
~~~~~~~~~~~~~~
"""

# Biblioteki
import json
import random
import sys
import numpy as np


class QuadraticCost(object):

    @staticmethod
    def fn(a, y):
        """Zwraca wartość funkcji kosztu dla wyniku sieci 'a'
        oraz pożądanego rezultatu 'y'.
        """
        return 0.5 * np.linalg.norm(a - y) ** 2

    @staticmethod
    def delta(z, a, y):
        """Zwraca błąd popełniany w wyjściowej warstwie sieci"""
        return (a - y) * sigmoid_prime(z)


class CrossEntropyCost(object):

    @staticmethod
    def fn(a, y):
        """Zwraca wartość funkcji kosztu dla wyniku sieci 'a'
        oraz pożądanego rezultatu 'y'.  Funckja np.nan_to_num
        jest używana żeby zapobiegać błędom (w niektórych przypadkach
        wyrażenie '1 - y' lub '1-a' może zwrócić NaN zamiast 0,
        funkcja nan_to_num zamienia NaN na 0.0)
        """
        return np.sum(np.nan_to_num(-y * np.log(a) - (1 - y) * np.log(1 - a)))

    @staticmethod
    def delta(z, a, y):
        """Zwraca błąd popełniany w wyjściowej warstwie sieci.
        Argument z, mimo tego iż nie jest używany, jest podawany
        aby wywoływanie funkcji delta było uniwersalne (patrz funkcja
        delta w klasie QuadraticCost.
        """
        return (a - y)


class Network(object):

    def __init__(self, sizes, cost=CrossEntropyCost):
        """Lista `sizes` zawiera liczby neuronów w kolejnych warstwach.
        Przykładowo, jeśli ta lista to [2, 3, 1]
        powstanie wtedy sieć neuronowa o 3 wastwach, z 2 neuronami w warswie
        wejściowej, 3 w warstwie ukrytej oraz 1 neuronem w warstwie wyjściowej.
        """
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.default_weight_initializer()
        self.cost = cost

    def default_weight_initializer(self):
        """Metoda losowo inicjalizująca wagi w sieci z rozkładem gaussowskim
        o wartości średniej 0 oraz odchyleniu standardowym 1 podzielonym
        przez pierwiastek z liczby krawędzi wchodzących do jednego neuronu.
        Progi inicjalizowane są losowo z rozkładem gaussowskim
        o wartości średniej 0 oraz odchyleniu standardowym 1.
        """
        self.biases = [np.random.randn(y, 1) for y in self.sizes[1:]]
        self.weights = [np.random.randn(y, x) / np.sqrt(x)
                        for x, y in zip(self.sizes[:-1], self.sizes[1:])]

    def large_weight_initializer(self):
        """Metoda inicjalizująca wagi oraz progi dokładnie w ten sam sposób
        co w module network.py. Została tutaj dodana aby łatwo można było
        porównac skuteczność sieci w zależności od użytego sposobu inicjalizacji
        wag.
        """
        self.biases = [np.random.randn(y, 1) for y in self.sizes[1:]]
        self.weights = [np.random.randn(y, x)
                        for x, y in zip(self.sizes[:-1], self.sizes[1:])]

    def feedforward(self, a):
        """Metoda zwracająca wynik sieci neuronowej, gdzie 'a' to dane wejściowe"""
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a) + b)
        return a

    def SGD(self, training_data, epochs, mini_batch_size, eta,
            lmbda=0.0,
            evaluation_data=None,
            monitor_evaluation_cost=False,
            monitor_evaluation_accuracy=False,
            monitor_training_cost=False,
            monitor_training_accuracy=False,
            early_stopping_n=0):
        """Metoda ta służy do nauczenia sieci neuronowej z wykorzystaniem
        stochastycznego spadku wzdłuż gradientu. Dane wejściowe dzielone są
        na mniejsze porcje o rozmiarze określonym przez atrybut mini_batch_size
        Training_data to lista zawierająca dwuelementowe krotki (x,y), gdzie x
        to piksele z obrazka wyjściowego, a y to spodziewany rezultat.
        Argument epochs określa przez ile epok sieć neuronowa będzie się uczyć,
        natomiast eta to współczynnik uczenia się. Parametr lmbda to parametr
        regulacji. Metoda może przyjąć dane sprawdzające- 'evaluation data'
        (mogą to być validation_data lub test_data z modułu  mnist_loader_py).
        Możemy monitorować funkcje kosztu, a także skuteczność sieci
        dla danych treningowych oraz sprawdzających ustawiając odpowiednie flagi.
        Argument 'early_stopping_n' służy do zatrzymania uczenia się sieci jeśli od
        n epok nie nastąpiła poprawa skuteczności sieci, np. jeśli przy wywołaniu metody
        podamy early_stopping_n=5 to sieć przestanie się uczyć niezależnie od liczby
        zadeklarowanych początkowo epok, jeśli przez 5 kolejnych epok sieć nie osiągnie
        lepszego rezultatu niż obecny najlepszy wynik.
        """

        training_data = list(training_data)
        n = len(training_data)

        if evaluation_data:
            evaluation_data = list(evaluation_data)
            n_data = len(evaluation_data)

        for j in range(epochs):
            random.shuffle(training_data)
            mini_batches = [
                training_data[k:k + mini_batch_size]
                for k in range(0, n, mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch(
                    mini_batch, eta, lmbda, len(training_data))

            print("Trening w epoce %s skończony" % j)

            if monitor_training_cost:
                cost = self.total_cost(training_data, lmbda)
                print("Koszt dla danych treningowych: {}".format(cost))
            if monitor_training_accuracy:
                accuracy = self.accuracy(training_data, convert=True)
                print("Poprawność dla danych treningowych: {} / {}".format(accuracy, n))
            if monitor_evaluation_cost:
                cost = self.total_cost(evaluation_data, lmbda, convert=True)
                print("Koszt dla danych testowych: {}".format(cost))
            if monitor_evaluation_accuracy:
                accuracy = self.accuracy(evaluation_data)
                print("Poprawność dla danych testowych: {} / {}".format(self.accuracy(evaluation_data), n_data))

            # Early stopping:
            best_accuracy = 0
            no_accuracy_change = 0
            if early_stopping_n > 0:
                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    no_accuracy_change = 0
                    print("Wczesne zatrzymywanie: Najlepsza skuteczność do tej pory {}".format(best_accuracy))
                else:
                    no_accuracy_change += 1

                if no_accuracy_change == early_stopping_n:
                    print("Wczesne zatrzymywanie: brak poprawy skuteczności w ostatnich {} epokach".format(early_stopping_n))
                    return

    def update_mini_batch(self, mini_batch, eta, lmbda, n):
        """Metoda aktualizująca wagi i progi w sieci na podstawie jednej porcji danych
        z wykorzystaniem stochastycznego spadku wzdłuż gradientu i algorytmu wstecznej
        propagacji błędów. Argument mini_batch to lista krotek (x, y) - część danych
        wejściowych podanych w funkcji SGD. Parametr 'lmbda' to współczynnik regularyzacji,
        a 'n' to całkowita liczba danych wejściowych.
        """
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weights = [(1 - eta * (lmbda / n)) * w - (eta / len(mini_batch)) * nw
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
        delta = (self.cost).delta(zs[-1], activations[-1], y)
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l + 1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l - 1].transpose())
        return (nabla_b, nabla_w)

    def accuracy(self, data, convert=False):
        """Metoda zwraca liczbę przypadków testowych, w których sieć neuronowa
        dała poprawny wynik. Jako wynik sieci jest brany indeks neuronu z warstwy
        wyjściowej, który ma największą wartość aktywacji.
        Flaga 'convert' obecna jest z powodu różnic w przedstawieniu pożądanych
        rezultatów w różnych zestawach danych. Więcej informacji w
        metodzie mnist_loader.load_data_wrapper.
        """
        if convert:
            results = [(np.argmax(self.feedforward(x)), np.argmax(y))
                       for (x, y) in data]
        else:
            results = [(np.argmax(self.feedforward(x)), y)
                       for (x, y) in data]

        result_accuracy = sum(int(x == y) for (x, y) in results)
        return result_accuracy

    def network_result(self, test_data):
        """Zwraca wynik"""
        test_results = [np.argmax(self.feedforward(x)) for x in test_data]
        return test_results

    def total_cost(self, data, lmbda, convert=False):
        """Zwraca całkowity koszt sieci neuronowej dla konkretnych danych.
        Warto zauważyć, że całkowity koszt na ogół rośnie wraz z kolejnymi
        epokami - naszym celem było znalezienie minimum funkcji kosztu!
        Nie przejmuj się tym problemem, wszystko jest w porządku :)
        Rośnie całkowita funkcja kosztu (zawierająca człon regulująca wagi),
        ale faktyczna, domyślna funkcja kosztu (czyli kwadratowa lub krzyżowej entopii)
        maleje. Człon regulujący wagi (którym mozesz manipulować za pomocą
        parametru lmbda) rośnie wraz ze wzrostem wag - a w naszej sieci wagi
        z reguły rosną wraz z kolejnymi epokami.
        """
        cost = 0.0
        for x, y in data:
            a = self.feedforward(x)
            if convert: y = vectorized_result(y)
            cost += self.cost.fn(a, y) / len(data)
            """wykomentuj poniższą linię, a printować będzie się 'czysta'
            funkcja kosztu, bez członu regulującego wagi."""
            cost += 0.5 * (lmbda / len(data)) * sum(
                np.linalg.norm(w) ** 2 for w in self.weights)

        return cost

    def save(self, filename):
        """Zapisz parametry sieci do pliku `filename`."""
        data = {"sizes": self.sizes,
                "weights": [w.tolist() for w in self.weights],
                "biases": [b.tolist() for b in self.biases],
                "cost": str(self.cost.__name__)}
        f = open(filename, "w")
        json.dump(data, f)
        f.close()


def load(filename):
    """Wczytaj nauczoną już sieć z pliku `filename`.
    """
    f = open(filename, "r")
    data = json.load(f)
    f.close()
    cost = getattr(sys.modules[__name__], data["cost"])
    net = Network(data["sizes"], cost=cost)
    net.weights = [np.array(w) for w in data["weights"]]
    net.biases = [np.array(b) for b in data["biases"]]
    return net


def vectorized_result(j):
    """Funkcja zwracająca wektor o długości 10, gdzie element o indeksie j
     ma wartość 1.0, a pozostałe elementy 0.0. Funkcja używana jest do
     konwersji pojedynczej cyfry (0...9) do odpowiedniego formatu
     oczekiwanego rezultatu sieci neuronowej - neuronów w ostatniej
     powinno być 10.
    """
    e = np.zeros((10, 1))
    e[j] = 1.0
    return e


def sigmoid(z):
    """Funkcja sigmoidalna."""
    return 1.0 / (1.0 + np.exp(-z))


def sigmoid_prime(z):
    """Pochodna funkcji sigmoidalnej."""
    return sigmoid(z) * (1 - sigmoid(z))
