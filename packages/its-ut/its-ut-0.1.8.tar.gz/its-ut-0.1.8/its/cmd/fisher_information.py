"""
This modules calculates the Fisher information. As we pointed out in the
help/description of the CLI tool, we only incorporate discrete and
pre-defined probabilities. The course material however only teaches how
to calculate the Fisher information based on the first/second derivative
of a PDF.

Implementing a full framework for generic mathematical functions and
their derivatives goes way beyond the expectations for this project.

Therefore, we looked into theory to calculate the Fisher information
based on accepted approximations in the academic field. We found a good
paper which suggests a multitude of potential candidates to calculate
the Fisher information for a well-defined discrete probability.

The mathematical expression is stated at the end of section 3:

J(p) = 4 \sum[i = 0, n -1] ( sqrt(p(x_i+1)) - sqrt(p(x_i)) )^2

Sánchez-Moreno, P., R. J. Yánez, and J. S. Dehesa.
"Discrete densities and Fisher information."
Proceedings of the 14th International Conference on Difference Equations
and Applications. Difference Equations and Applications.
Istanbul, Turkey: Bahçesehir University Press. 2009.


Note: We understand that this approximation of the Fisher information is
a bit far fetched. Generally, the Fisher information is an indicator, 
how much a random variable X carries about an unknown Theta. If someone
wants to calculate the Fisher information for a Theta, then they have to
estimate the distribution to a discrete probability, as we use it here.


Examples:
    its-ut --distribution distribution/mackay-example-4-6.csv fisher-information -n 1

    Calculates the Fisher information of an arbitrary distribution given by

"""

import math
import sys

from its import common

def partial_fi(px, py):
    x = math.sqrt(px)
    y = math.sqrt(py)
    return math.pow(y - x, 2)

def fn(args):
    n = args.n

    # Load the distribution and assign it to the subparser for the command
    # args.distribution = distribution
    # distribution = args.distribution
    distribution = common.load_distribution(args.distribution_file)

    if not type(n) is int:
        print("Failed to parse expression for n. Make sure it evaluates to an integer.", file=sys.stderr)
        sys.exit(1)

    combinations = common.combinations(distribution.keys(), n)
    probabilities = common.probabilities(distribution, combinations)
    p = list(map(lambda e: e[1], probabilities))

    # fi = 4 * sum([partial_fi(p[i], p[i + 1]) for i in range(len(pn) - 1)])
    fi = [partial_fi(*p[i:i+2]) for i in range(len(p) - 1)]
    fi = 4 * sum(fi)

    print(f"{fi:.12f}")

    print(f"Total number of combinations: {len(combinations)}", file=sys.stderr)
