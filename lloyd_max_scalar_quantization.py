import numpy as np
import time


def pdf(l, x):
    return l * np.exp(-l * x)


def cdf(l, x):
    return 1 - np.exp(-l * x)


def interval_error(l, interval, y):
    (a, b) = interval
    bracket = l * a * np.exp(-l * a) + np.exp(-l * a) - l * b * np.exp(-l * b) - np.exp(-l * b)
    return -y ** 2 * np.exp(-l * b) + y ** 2 * np.exp(-l * a) - 2 * y * bracket / l - b ** 2 * np.exp(
        -l * b) + a ** 2 * np.exp(
        -l * a) + (-2 * b * np.exp(-l * b) + 2 * a * np.exp(-l * a)) / l + (
                   -2 * np.exp(-l * b) + 2 * np.exp(-l * a)) / l ** 2


def error(l, b, y):
    running_sum = 0
    for i in range(len(y)):
        running_sum += interval_error(l, (b[i], b[i + 1]), y[i])
    return running_sum


def update_quantization_levels(l, b):
    y = []
    for i in range(1, len(b)):
        upper = (-l * b[i] * np.exp(-l * b[i]) - np.exp(-l * b[i]) + l * b[i - 1] * np.exp(-l * b[i - 1]) + np.exp(
            -l * b[i - 1])) / l
        lower = cdf(l, b[i]) - cdf(l, b[i - 1])
        y.append(upper / lower)
    return y


def update_quantization_boundaries(y, x):
    b = [x[0]]
    res = []
    for i in range(len(y) - 1):
        res.append((y[i] + y[i + 1]) / 2)
    b.extend(res)
    b.append(x[-1])
    return b


def quantize(l, k, thres, x, timeout):
    # initialize
    start = time.time()

    MSE, counter = [np.infty], 0

    b = np.linspace(x[0], x[-1], num=k + 1, endpoint=True)

    while MSE[-1] > thres and time.time() - start < timeout:
        y = update_quantization_levels(1, b)
        b = update_quantization_boundaries(y, x)
        MSE.append(error(l, b, y))
        counter += 1

    return y, b, MSE
