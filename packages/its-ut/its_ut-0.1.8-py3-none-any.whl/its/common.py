import itertools
import math


class DistributionValueError(ValueError):
    pass

def seq(start=1):
    """Generates a sequence of integers. Useful for the line number
    generation in the `parse_p` call.
    """
    i = start

    while True:
        yield i
        i += 1

seq_line_no = seq(1)

def _parse_p(s: str) -> tuple:
    """Parses a single line from the input distribution. The input
    distribution format has to be a comma-separated list of numeric
    values:

        x:int, p:float

    Raises a value error if x is not an integer, or p is not a float.
    """
    global seq_line_no
    i = next(seq_line_no)
    s = s.strip()       # 0, 0.4
    if not len(s) or s[0] == "#":
        return None

    if "," not in s:
        raise DistributionValueError(f"Distribution invalid: [Line {i: 2}] {s} is not a valid entry. Requires the format `x:string, p(x):[float, expression]`")

    x, remainder = s.split(",", maxsplit=1)
    p_xs = remainder.split(",")

    try:
        if len(p_xs) == 1:
            p_x = p_xs[0]
            x = str(x)
            p_x = float(eval(p_x))
            # assert p_x >= 0.0 and p_x <= 1.0
        else:
            p_x = [float(eval(x)) for x in p_xs]

    except Exception:
        raise DistributionValueError(f"Distribution invalid: [Line {i: 2}] Either x, or P(x) is not in interval [0, 1]")

    return x, p_x


def load_distribution(file_path: str) -> dict:
    """Loads the distribution from a file, removes the comment lines and
    creates a dictionary with <int>:<float> mapping, where the integer
    is the label and the float is the probability as part of the
    interval [0, 1]

    Passes on the value error from parse_p, if some entry in the
    """
    with open(file_path, "r") as f:
        values = map(_parse_p, f.readlines())
        values = filter(bool, values)
        distribution = dict(values)

        # Note: Total probability does not strictly line up to `1.0` due to floating point error margins
        acceptance_margin = 1 / 2**12

        is_valid = True
        dist_values = list(distribution.values())

        if isinstance(dist_values[0], list):
            for sub_list in dist_values:
                p = sum(sub_list)
                if not (1.0 - acceptance_margin <= p <= 1 + acceptance_margin):
                    is_valid = False
        else:
            p = sum(dist_values)
            if not (1.0 - acceptance_margin <= p <= 1 + acceptance_margin):
                is_valid = False

        if is_valid:
            return distribution
        else:
            delta = sum(distribution.values()) - 1.0
            raise DistributionValueError(f"Distribution invalid: Probabilty of distribution does not add up to 1: (Error of {delta})")


def combinations(labels: list, n: int) -> list:
    """Generates all possible combinations for a given input set of
    labels of the length `n`.
    """
    return list(itertools.product(labels, repeat=n))


def entropy(distribution: dict) -> float:
    """Calculates the Shannon entropy for a given distribution."""
    values = distribution.values()
    # We set p=0.0 to p=1.0 to not run into domain errors for log2(0)
    return sum(map(lambda p: -1 * p * math.log2(1.0 if p == 0.0 else p), values))

def entropy_from_list(distribution: list) -> float:
    """Calculates the Shannon entropy for a given distribution."""
    # We set p=0.0 to p=1.0 to not run into domain errors for log2(0)
    return sum(map(lambda p: -1 * p * math.log2(1.0 if p == 0.0 else p), distribution))

def probabilities(distribution: dict, combinations: list) -> list:
    """Generates all combinations for a given input distribution and
    calculates the corresponding probabilities. Returns a list as
    follows

        [(label_1, label_2, ..., label_n), P(label)] 
    """
    # combinations = combinations(distribution.keys(), n)
    probabilities = [math.prod(map(distribution.get, c)) for c in combinations]
    return list(zip(combinations, probabilities))