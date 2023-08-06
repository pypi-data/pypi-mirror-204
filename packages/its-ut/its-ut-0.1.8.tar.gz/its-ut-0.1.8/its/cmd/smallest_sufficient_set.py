"""
The smallest sufficient set is yet another piece of theory which defines
a subset of elements out of words with similar length. To construct the
smallest sufficient set, you first need to generate all different
combinations for a given set. Afterwards, you have to calculate the
probabilities for each combination and order the combinations by it's
probabilities in decreasing order. Lastly, simply take as many elements
until you pass the probability (1 - delta):

    P(x in S) >= (1 - d)

Examples:

    its-ut smallest-sufficient-set -d distributions/english-alphabet.csv -n 2 -D 0.1 --print-probabilities

        Prints the smallest sufficient set of the English alphabet with
        a delta=0.1, a word-length n=2 and inclues the probabilities in
        the output

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
    delta = args.delta
    distribution = common.load_distribution(args.distribution_file)
    # distribution = args.distribution
    print_probabilities = args.print_probabilities

    if not all([type(n) is int, type(delta) is float]):
        print("Failed to parse expression for n or delta. Make sure they evaluate to numerical values", file=sys.stderr)
        sys.exit(1)

    # First, we get all combinations and calculate the probabilities for each combination.
    combinations = common.combinations(distribution.keys(), n)
    probabilities = common.probabilities(distribution, combinations)

    # Now, we order the combinations in descending probability.
    probabilities = sorted(probabilities, key=lambda x: x[1], reverse=True)

    i = 0
    p_total = 0

    # Lastly, we cumulate the probabilities of the combinations and add the elements to the smallest sufficient set.
    # As soon as we reached the defined delta, we stop adding elements and we have our smallest sufficient set.
    for x, p in probabilities:
        i += 1
        p_total += p
        x = "".join(x)
        print(f"{x},{p:.12f},{p_total:.12f}" if print_probabilities else f"{x}")

        # Break, if we have reached the previously defined delta
        if p_total >= 1 - delta:
            break

    print(f"Size of set: {len(combinations)}", file=sys.stderr)
    print(f"Size of smallest sufficient subset: {i}", file=sys.stderr)
    print(f"Total probability of smallest sufficient subset: {p_total:.5f}", file=sys.stderr)

