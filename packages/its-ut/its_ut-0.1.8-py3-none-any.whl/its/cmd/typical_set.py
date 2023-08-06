"""
A typical set is a feature of combinatorics based on a given probability
distribution. 

Our framework allows to read a finite and well-defined distribution from
a CSV file.

The file has the format:
    x, P(X=x)

A typical set however requires a sequence of symbols. In our case, the
input distribution builds the set of symbols plus their corresponding
probabilities. As an example, if you want to define a Bernoulli
distribution, you could do this as follows:

    a, 0.4
    b, 0.6

This assigns the probability of P(X=a) = 0.4 and P(X=b) = 0.6

The typical set requires then a sequence of combinations of those
symbols. If we want to calculate the typical set with the parameters:

    N = 3 and beta=0.1

Then we should call the module as follows:

    its-ut typical-set -d distributions/bernoulli.csv -n 3 -b 0.1

The output will print all elements part of the typical set:

011
101
110

At the end, the output adds a short summary:

Size of set: 8
Size of typical set: 3

Furthermore, the output can be adjusted to include the probabilities.
Just add the `--print-probabilities` to the command:

    its-ut typical-set -d distributions/bernoulli.csv -n 3 -b 0.1 --print-probabilities

011,0.144000000000
101,0.144000000000
110,0.144000000000
Size of set: 8
Size of typical set: 3

Examples:

    its-ut typical-set --distribution distributions/english-alphabet.csv -n 4 -b 0.001

        Prints the typical set of the English alphabet for words with
        the length 4 and beta=0.001

    its-ut typical-set -d distributions/english-alphabet.csv -n 4 -b 0.001 --print-probabilities

        Adds additionally the probabilities to the output as described
        above.

"""


import math
import sys

from its import common

def is_in_t_bn(n: int, beta: float, entropy: float, p: float) -> bool:
    """Checks if the condition for a calculated probability fits the
    requirements of an element of the typical set.
    """
    x = (1 / n) * math.log2(1 / p) - entropy
    return abs(x) < beta


def fn(args):
    n = args.n
    beta = args.beta

    # distribution = args.distribution
    distribution = common.load_distribution(args.distribution_file)
    print_probabilities = args.print_probabilities

    # Since we accept evaluated values for n and beta, we need to assure the types are correct.
    if not all([type(n) is int, type(beta) is float]):
        print("Failed to parse expression for n or beta. Make sure they evaluate to numerical values", file=sys.stderr)
        sys.exit(1)


    h = common.entropy(distribution)
    combinations = common.combinations(distribution.keys(), n)
    probabilities = common.probabilities(distribution, combinations)

    # typicallity_test = functools.partial(is_in_t_bn, n, beta, h)
    typical_set = list(filter(lambda x: is_in_t_bn(n, beta, h, x[1]), probabilities))

    for x, p in typical_set:
        x = "".join(x)
        p = f"{p:.12f}"
        print(f"{x},{p}" if print_probabilities else x)

    print(f"Size of set: {len(combinations)}", file=sys.stderr)
    print(f"Size of typical set: {len(typical_set)}", file=sys.stderr)

