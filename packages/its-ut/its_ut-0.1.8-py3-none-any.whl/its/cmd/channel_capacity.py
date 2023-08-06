"""
This module approximates the channel capacity. As we pointed out in the
help/description of the CLI tool, we only incorporate discrete and
pre-defined joint distributions, similar to that which has been done in
an exact/non-approximating way during the course.

For the approximation, all possible distributions for a random variable
X are tried on which variable Y is dependent. All possible distributions
here is defined as all possible combinations of:

    p(x1)...p(xn) for which p(x1) + ... + p(xn) = 1
    
Every p(x_i) can take on exactly 1 / step_size values, with exactly
`step_size` space in between.

As part of calculating the channel capacity, the mutual information is
calculated as follows:

    I(X;Y) = H(X) - H(X|Y)
    = H(X) - Sum_{y in Y}( p(y) H(X|Y=y) )
    = H(X) - Sum_{y in Y} p(y) Sum{x in X}( p(x|y) log p(x|y) )

    We know p(y|x) and p(x)

    For the calculation of I(X;Y), we need p(x|y)

    Using Bayes' rule:
    p(y|x) = ( p(x|y) p(y) ) / p(x)

    p(y|x) / p(y) = p(x|y) / p(x)

    ( p(x) p(y|x) ) / p(y) = p(x|y)


Examples:

    its-ut channel-capacity --joint-distribution distributions/channel-1.csv

        Approximates the Channel Capacity for an arbitrary channel
        defined by a discrete joint probability distribution

"""

import numpy as np
from its import common
import copy
import itertools
import sys

def calculateMutualInfo(px, pygx):
    pygx = np.array(pygx)

    X, Y = pygx.shape

    # Find joint distribution p(xy) ( p(x)p(y|x) )
    pxy = np.multiply(np.tile(px, (Y, 1)).T, pygx)

    # Calculate p(y)
    py = np.sum(pxy, axis=0)

    # Calculate p(x|y) = ( p(x) p(y|x) ) / p(y)
    py_tiled = np.tile(py.T, (pxy.shape[1], 1))
    pxgy = np.divide(pxy, py_tiled, where=py_tiled != 0).T

    # Compute entropy of x
    HX = common.entropy_from_list(px)

    # Compute p(x|y)log p(x|y)
    pxgy_hxgy = copy.deepcopy(pxgy)
    for idx_row, row in enumerate(pxgy_hxgy):
        for idx_el, el in enumerate(row):
            if el != 0:
                pxgy_hxgy[idx_row][idx_el] = -el * np.log2(el)

    # Compute - Sum_{y in Y} p(y) Sum{x in X}( p(x|y) log p(x|y) ), note p(x|y) log p(x|y) = pxgy_hxgy
    HXgY = np.sum(np.sum(pxgy_hxgy, axis=1) * py)

    # Compute I(X;Y) = H(X) - H(X|Y)
    I = HX - HXgY
    return I

def generate_tuples(n, d):
    # Generate all possible combinations of values for each element
    possible_values = [[i * d for i in range(int(1 / d) + 1)] for j in range(n)]
    tuples = []

    # Generate tuples for all possible combinations
    for values in itertools.product(*possible_values):
        if abs(sum(values) - 1) < 1e-9:  # Check if sum of values is approximately 1
            tuples.append(values)

    return tuples

def fn(args):
    # Load the joint distribution and assign it to the subparser for the command
    # args.joint-distribution = joint distribution
    # joint-distribution = args.joint-distribution
    joint_distribution = list(common.load_distribution(args.distribution_file).values())

    step_size = args.step

    if not type(step_size) is float:
        print("Failed to parse expression for step. Make sure it evaluates to a float.", file=sys.stderr)
        sys.exit(1)

    pygx = np.array(joint_distribution).T

    depth = len(pygx[0])

    # Generate tuples
    x_tuples = generate_tuples(depth, step_size)

    max_I = 0
    bestXdist = []
    IOutcomes = []

    # Compute I(X;Y) for all probability distributions of x
    for combination in x_tuples:
        mutual_info = calculateMutualInfo(combination, pygx)
        IOutcomes.append(mutual_info)
        # Store the maximum mutual information together with its associated distribution of x
        if mutual_info > max_I:
            max_I = mutual_info
            bestXdist = combination
    print(max_I, file=sys.stderr)
    print('with', file=sys.stderr)
    print(bestXdist, file=sys.stderr)
