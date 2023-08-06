"""
The Kullback-Leibner Divergence is a distance measure between two
probability distributions on the same Alphabet. It's definition:

    D(P || Q) = \sum_x P(X) * log2 ( P(X) / Q(X) )

Both distributions P and Q need to have the same alphabet/set of symbols
defined.

To calculate the KL divergence, you have to define two distributions as
input, defined as CSV-files with the flags `-p` and `-q`. The result is
printed to the screen.

Assumptions:
To work properly, we assume that both files have the same input symbols
in exactly the same order. The easiest way to be compliant is to first
define the first distribution with symbols and probabilities, then copy
the distribution file and just alter the expressions for the 
probabilities.

Example:

    its-ut kl-divergence -p distributions/bernoulli.csv -q distributions/bernoulli-uniform.csv

        Calculates the KL Divergence between these two distributions.
        For instance:
            D( P~Bernoulli(0.4) || Q~Bernoulli(0.5) ) = 0.020135513551

"""

import numpy as np

from its import common

def fn(args):
    # print("this is the KL divergence")

    p1 = common.load_distribution(args.p)
    p2 = common.load_distribution(args.q)

    p1 = np.array(list(p1.values()))
    p2 = np.array(list(p2.values()))

    x = np.sum(p1 * np.log(p1 / p2))
    print(f"{x:.12f}")

