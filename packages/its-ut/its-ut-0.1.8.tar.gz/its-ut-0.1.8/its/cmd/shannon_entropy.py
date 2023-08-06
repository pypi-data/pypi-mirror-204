"""
The Shannon-entropy is a measurement how tilted a distribution is. It is
the input for various calculations in other commands/modules.

The formula is as follows:

    H(X) = - \sum ( P(X) log2 P(X) )

In our implementation the output is always in bits.

Examples:

    its-ut shannon-entropy -d distributions/english-alphabet.csv

        Calculates H(X) for the English alphabet

    its-ut shannon-entropy -d distributions/uniform-10.csv

        Calculates H(X) for a uniform distribution.

"""


from its import common

def fn(args):
    distribution = common.load_distribution(args.distribution_file)
    h = common.entropy(distribution)
    print(f"{h:.12f}")
