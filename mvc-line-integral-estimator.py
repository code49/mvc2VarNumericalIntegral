# ----- import important libraries -----

from cmath import pi
import math
import pprint
import argparse

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as ptch

# ----- define helpful built-in functions -----


def __sumList__(input_list: list):
    """

    sums the numerical values of a list

    Parameters:
    -----------

    input_list: list
        list containing the numbers to be summed

    Returns:
    --------

    sum: number (int, float, etc.)
        sum of the numbers in the input_list

    """

    sum = 0
    for element in input_list:
        sum += element

    return sum

# ----- define a two-variable integral estimation function -----


def estimateDefinedIntegral(function, lower, upper, steps):
    """

    a numerical method of estimating the value of a defined integral (hopefully one that is unsolvable symbollically)

    Parameters:
    -----------

    function: function reference (use lambda)
        lambda expression representing what the function is integrating for (the integrand). must be formatted in the numpy style (https://www.geeksforgeeks.org/numpy-mathematical-function/) with variable x.

    lower: number (int, float, etc.)
        number representing the lower bound for definite integration.

    upper: number (int, float, etc.)
        number representing the upper bound for definite integration.

    step_size: number (int, float, etc.)
        number representing the step count to use for estimation of definite integration.

    Returns:
    --------

    sum: number (int, float, etc.)
        number representing the numerical estimation of the definite integral.

    step_values: list
        list containing the x values at which rectangular approximations are calculated, mostly for the purpose of creating a pretty plot.

    step_heights: list
        list containing the y values derived from the step_values, mostly for the purpose of creating a pretty plot.

    step_width: number (int, float, etc.)
        number representing the distance between x-steps used for numerical integration, mostly for the purposes of creating a pretty plot.

    """

    # ----- calculate the size of steps needed in the range -----

    step_size = (upper - lower)/steps

    # ----- calculate the height of each step in the range, calculated on the lower bound -----

    step_values = []
    for i in range(0, steps):
        step_values.append((step_size * i) + lower)

    step_heights = []
    for value in step_values:
        step_heights.append(function(value))

    # ----- sum the step_heights * step_values, then return it as a numerical estimation -----
    areas_list = []
    for i in range(0, len(step_values)):
        areas_list.append(step_size * step_heights[i])

    # # for debugging purposes
    # pprint.pprint(step_values)
    # pprint.pprint(step_heights)
    # pprint.pprint(areas_list)

    # return the sum and plot
    return __sumList__(areas_list), step_values, step_heights, step_size

# ----- define a two-variable numerical integration grapher function -----


def graphDefinedIntegralEstimation(function, step_values, step_heights, step_size, graph_x_offset=100, graph_y_offset=100):
    """

    creates a pretty graph of a numerical integration estimation using matplotlib

    Parameters:
    -----------

    function: function reference (use lambda)
        lambda expression representing what the function is integrating for (the integrand). must be formatted in the numpy style (https://www.geeksforgeeks.org/numpy-mathematical-function/) with variable x.

    step_values: list
        list containing the x values at which rectangular approximations are calculated.

    step_heights: list
        list containing the y values derived from the step_values.

    step_width: number (int, float, etc.)
        number representing the distance between x-steps used for numerical integration.

    graph_x_offset: int (optional)
        integer representing the offset to be used for the graph in the x direction. defaults to 100.

    graph_y_offset: int (optional)
        integer representing the offset to be used for the graph in the y direction. defaults to 100.

    Returns:
    --------

    plot: matplotlib plot object
        plot object from matplotlib, containing the graph of the numerical integration estimation.

    """

    fig, ax = plt.subplots()

    # plot settings
    plt.title('two-variable numerical integral estimation')
    plt.ylabel('f(x)')
    plt.xlabel('x')

    plt.axhline(0, color='grey')  # x = 0
    plt.axvline(0, color='grey')  # y = 0

    # plot rectangle approximations
    for i in range(0, len(step_values)):

        # for values >= 0:
        if step_heights[i] >= 0:
            ax.add_patch(ptch.Rectangle(
                (step_values[i], 0), step_size, step_heights[i], alpha=0.5, ec="black"))

        # for values < 0:
        else:
            ax.add_patch(ptch.Rectangle(
                (step_values[i], step_heights[i]), step_size, -step_heights[i], alpha=0.5, ec="black"))

    # ensure correct x-y axis, according to the given offsets
    x_range = (step_values[0] - graph_x_offset,
               step_values[-1] + step_size + graph_x_offset)
    y_range = (step_heights[0] - graph_y_offset,
               step_heights[-1] + graph_y_offset)

    plt.xlim(x_range)
    plt.ylim(y_range)

    # plot function approximation as a curve/line
    x_curve_values = np.linspace(x_range[0]*10000, x_range[1]*10000, 10000000)
    y_curve_values = function(x_curve_values)
    plt.plot(x_curve_values, y_curve_values, color="red")

    # plot points used to calculate rectangle approximation areas
    plt.scatter(step_values, step_heights, marker='o', color="black", s=10)

    return plt

# ----- for using these functions on a problem -----


print()
# this represents the function (integrand) you are integrating across
function_string = "(np.sin(x) * np.cos(x**2) + 5) * (np.sqrt(1 + 4*x**2))"
# remember that it must be formatted in the numpy style, but in a string! (https://www.geeksforgeeks.org/numpy-mathematical-function/)


# change these variables depending on the problem too
lower = 0
upper = 2*pi
steps = 100000

x_offset = 1
y_offset = 10

# run the estimator/grapher


def f(x): return eval(function_string)


# estimator
print(
    f"numerically integrating {function_string}, from {str(lower)} to {str(upper)}, using {str(steps)} rectangles.")
sum, step_values, step_heights, step_size = estimateDefinedIntegral(
    f, lower, upper, steps)
print(f"result: {str(sum)} \n")

# grapher, using the results from the estimator
print("creating plot of the integration... \n")
plot = graphDefinedIntegralEstimation(
    f, step_values, step_heights, step_size, graph_x_offset=x_offset, graph_y_offset=y_offset)
print("plot not looking right? here are some tips for things to check:")
print("     - check your offsets; it's possible you forgot to set them properly")
print("     - everything under the curve look black? probably because you integrated across a large number of rectangles, but it doesn't change the calculation any.")
plot.show()
