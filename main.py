import matplotlib.pyplot as plt
from lloyd_max_scalar_quantization import *

cmap = plt.get_cmap("tab10")

if __name__ == '__main__':
    l = 1  # rate parameter
    k = 8  # number of the levels
    max_range = 10
    thres = 1e-3
    timeout = 1e-2

    x = range(0, max_range + 1)
    y = [pdf(l, i) for i in x]

    # quantization
    levels, b, MSE_8 = quantize(l, k, thres, x, timeout)

    print(str(len(b)) + " Boundaries:", b)
    print(str(len(levels)) + " Quantization levels:", levels)

    bar_y = [pdf(l, i) for i in levels]

    # plot
    fig, axs = plt.subplots(1, 2)
    axs[0].plot(x, y, color=cmap(0))
    axs[0].scatter(levels, [0] * len(levels), color=cmap(1), marker=".", label="Quantization levels")
    axs[0].scatter(b, [0] * len(b), color=cmap(2), marker='x', label="Boundaries")

    # axs[0].hlines(0, 0, max_range, colors="black")
    for i in range(len(levels)):
        axs[0].vlines(b[i], 0, bar_y[i], colors=cmap(2))
        axs[0].vlines(b[i + 1], 0, bar_y[i], colors=cmap(2))

        axs[0].vlines(levels[i], 0, bar_y[i], colors=cmap(1), linestyles="dashed")
        axs[0].hlines(bar_y[i], b[i], b[i + 1], colors=cmap(2))

    axs[0].set_xlim(0, max_range)
    axs[0].set_ylabel("PDF")
    axs[0].set_xlabel("t")

    axs[0].legend(title="k=" + str(k))

    # quantization
    k = 5
    levels, b, MSE_5 = quantize(l, k, thres, x, timeout)

    # quantization
    k = 10
    levels, b, MSE_10 = quantize(l, k, thres, x, timeout)

    max_len = max(len(MSE_5), len(MSE_8), len(MSE_10))

    if len(MSE_5) < max_len:
        MSE_5.extend([MSE_5[-1]] * (max_len - len(MSE_5)))

    if len(MSE_8) < max_len:
        MSE_8.extend([MSE_8[-1]] * (max_len - len(MSE_8)))

    if len(MSE_10) < max_len:
        MSE_10.extend([MSE_10[-1]] * (max_len - len(MSE_10)))

    axs[1].plot(range(len(MSE_5)), MSE_5, label="k=5")
    axs[1].plot(range(len(MSE_8)), MSE_8, label="k=8")
    axs[1].plot(range(len(MSE_10)), MSE_10, label="k=10")
    # axs[1].plot(range(len(MSE)), MSE, marker='x')
    axs[1].set_xlabel("Iterations")
    axs[1].set_ylabel("MSE")
    axs[1].legend()

    plt.tight_layout()
    plt.show()
