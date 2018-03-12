"""
Integration test; uses a plot.
"""

import numpy as np
import matplotlib.pyplot as plt

from sidefit import Fitter

def get_true_data():
    """
    Gets the data for a step function.
    """

    x = np.arange(-1.0, 1.0, 0.001)

    y = np.array([0.]*1000 + [1.0]*1000)

    return x, y


def sigmoid(x, norm):
    """
    Sigmoid function that looks like a smooth step
    """
    return np.exp(x/norm) / (np.exp(x/norm) + 1)


def get_smoothed_data():
    """
    Gets the smoothed data (there is some smoothing over the step function).
    """

    x = np.arange(-1.0, 1.0, 0.001)
    y = np.array([0.]*1000 + [1.0]*1000)

    y[900:1100] = sigmoid(x[900:1100], 0.01)

    return x, y


def simple(x, y, interp):
    y_i = interp(x)
    
    return abs(y_i - y)


def test_integration_heaviside():
    """
    Integration test with the smoothed heavyside step function.
    """
    
    true = get_true_data()
    smooth = get_smoothed_data()

    fit = Fitter(*true, *smooth, 0.1)

    interp = fit.interpolate_function()
    r = fit.brute_force()

    fig, ax = plt.subplots(2, 1)

    ax[0].plot(true[0], interp(true[0]))
    ax[0].scatter(*smooth)

    ax[0].set_xlim(-0.05, 0.05)
    ax[1].set_xlim(-0.05, 0.05)

    #ax[1].plot(true[0], simple(smooth[0], smooth[1], interp), alpha=0.5)
    ax[1].plot(true[0], r)

    plt.savefig("test_integration_heaviside.png")

    x = r[100]

    assert not np.isclose(r, x, 1e-2).all()


def test_plot_heaviside():
    """
    Do a test plot
    """
    true = get_true_data()
    smooth = get_smoothed_data()

    fit = Fitter(*true, *smooth, 0.1)

    interp = fit.interpolate_function()

    def r(x, px, py):
        return (x - px)**2 + (interp(x) - py)**2

    px = -0.009
    py = 0.4

    x = np.arange(-0.01, 0.01, 0.0001)

    y = r(x, px, py)

    fig, ax = plt.subplots(2, 1, sharex=True)

    ax[0].plot(x, y)
    ax[1].scatter(px, py)
    ax[1].plot(x, interp(x))
    plt.savefig("test_plot_heaviside.png")


if __name__ == "__main__":
    test_integration_heaviside()
    test_plot_heaviside()

