import numpy as np
from matplotlib import pyplot as pl
from train_dataset import M
from pprint import pprint
from tqdm import tqdm

input_count = len(M[0]['input'])
output_count = len(M[0]['output'])


def print_len(x):
    for i in x:
        print(len(i))


M_with_bias = []
for symb in M:
    symb_with_bias = {}
    symb_with_bias['input'] = symb['input']
    symb_with_bias['output'] = symb['output']
    symb_with_bias['input'] = np.append(symb_with_bias['input'], 1)
    M_with_bias.append(symb_with_bias)


def sigma(x):
    return 1 / (1 + np.exp(-x))


def d_sigma(x):
    return sigma(x) * (1 - sigma(x))


def mse(y_true, y_result):
    return ((y_true - y_result) ** 2).mean()


class Model():
    def __init__(self):
        self.hidden_weight = np.zeros((int(input_count / 2), input_count + 1))
        self.output_weight = np.zeros((output_count, int(input_count / 2) + 1))

    def train(self, epoch_count=1000, norm=0.1):
        def n(x):
            return norm * x

        self.hidden_weight = np.random.rand(int(input_count / 2) + 1, input_count + 1)
        self.output_weight = np.random.rand(output_count, int(input_count / 2) + 1)

        train_plot_data = []

        for step in tqdm(range(epoch_count)):
            mse_epoch = []
            for symb in M_with_bias:
                # Forward pass
                hidden_output_P = self.hidden_weight.dot(symb['input'])
                hidden_output = sigma(hidden_output_P)
                # Adding bias
                output_P = self.output_weight.dot(hidden_output)
                output = sigma(output_P)
                # Calculating mean squared error

                mse_epoch.append(mse(symb['output'], output))

                # Backward pass
                output_error = symb['output'] - output
                output_layer_error = self.output_weight.T.dot(output_error)
                hidden_layer_error = self.hidden_weight.T.dot(output_layer_error)

                for i, neuron in enumerate(self.output_weight):
                    t = norm * output_error[i] * d_sigma(output_P[i])
                    for j, weight in enumerate(neuron):
                        self.output_weight[i][j] += t * hidden_output[j]

                for i, neuron in enumerate(self.hidden_weight):
                    t = norm * output_layer_error[i] * d_sigma(hidden_output_P[i])
                    for j, weight in enumerate(neuron):
                        self.hidden_weight[i][j] += t * symb['input'][j]

            train_plot_data.append(np.array(mse_epoch).mean())

        pl.plot(train_plot_data)
        pl.show()

    def test(self, input):
        # Adding bias
        input = np.append(input, 1)
        hidden_output_P = self.hidden_weight.dot(input)
        hidden_output = sigma(hidden_output_P)
        # Adding bias
        output_P = self.output_weight.dot(hidden_output)
        output = sigma(output_P)
        pprint(output)
        return output

    def print_weight(self):
        pprint(self.hidden_weight)
        pprint(self.output_weight)
