#!/usr/bin/env python3.10

import argparse
import sys
import traceback

from its import common

from its.cmd.channel_capacity import fn as fn_channel_capacity
from its.cmd.fisher_information import fn as fn_fischer_information
from its.cmd.help import fn as fn_help
from its.cmd.huffman_code import fn as fn_huffman_code
from its.cmd.kl_divergence import fn as fn_kl_divergence
from its.cmd.lempel_ziv import fn as fn_lempel_ziv
from its.cmd.print import fn as fn_print
from its.cmd.shannon_entropy import fn as fn_shannon_entropy
from its.cmd.smallest_sufficient_set import fn as fn_smallest_sufficient_set
from its.cmd.typical_set import fn as fn_typical_set


DESCRIPTION = """
Information Theory & Statistics framework

Project Group 28

The project aims to provide an easy way to verify some calculations
based on the theory we learned in this lecture.
"""


def main():
    # TODO: Add a better description
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Set output to verbose to prints exceptions and debug information",
    )

    cmd = parser.add_subparsers(
        title="commands",
        description="Commands implemented as part of this project.",
        dest="cmd",
        required=True,
    )

    # TODO: Perhaps remove the Bernoulli
    # Parser for the Bernoulli command
    # parser_bernoulli = cmd.add_parser("bernoulli", help="Bernoulli trials")
    # parser_bernoulli.set_defaults(func=fn_bernoulli)

    #
    # Parser: Channel capacity
    #
    parser_channel_capacity = cmd.add_parser("channel-capacity", help="Module to approximate channel capacity.")
    parser_channel_capacity.add_argument(
        "-j",
        "--joint-distribution",
        type=str,
        help="Path to the CSV-file which defines the discrete and finite joint distribution (X, Y)",
        dest="distribution_file",
        required=True,
    )
    parser_channel_capacity.add_argument(
        "--step",
        type=eval,
        help="Step size defines how granular approximation is"
             " (lower step size wil mean more distributions for input X tried). A lower step size increases computation"
             " time exponentially",
        default=1/10,
    )
    parser_channel_capacity.set_defaults(func=fn_channel_capacity)


    #
    # Parser: Fisher Information
    #
    parser_fisher_information = cmd.add_parser(
        "fisher-information",
        help="Command to calculate the Fisher information for a discrete probability",
    )
    parser_fisher_information.add_argument(
        "-d",
        "--distribution",
        type=str,
        help="Path to the CSV-file which defines the discrete distribution",
        dest="distribution_file",
        required=True,
    )
    parser_fisher_information.add_argument(
        "-n",
        type=eval,
        default=1,
    )
    parser_fisher_information.set_defaults(func=fn_fischer_information)

    #
    # Parser Help
    #
    parser_help = cmd.add_parser(
        "help",
        help="Print a text to understand how to use this tool and to understand certain assumptions we made in each of the modules.",
    )
    parser_help.add_argument(
        "module",
        help="Define a command for which you want to get more help.",
        nargs="?",
    )
    parser_help.set_defaults(func=fn_help)

    #
    # Parser: Huffman Code
    #
    parser_huffman_code = cmd.add_parser("huffman-code", help="Module to generate Huffman codes.")
    parser_huffman_code.add_argument(
        "-d",
        "--distribution",
        type=str,
        help="Path to the CSV-file which defines the discrete and finite distribution",
        dest="distribution_file",
        required=True,
    )
    parser_huffman_code.add_argument(
        "--print-graph-information",
        action="store_true",
        help="Print the edges and vertices of the graph.",
    )
    parser_huffman_code.set_defaults(func=fn_huffman_code)

    #
    # Parser KL Divergence
    #     
    parser_kl_divergence = cmd.add_parser("kl-divergence", help="this is the kl divergence command")
    parser_kl_divergence.add_argument(
        "-p",
        "--probability-p",
        type=str,
        help="Distribution P",
        dest="p",
        required=True,
    )
    parser_kl_divergence.add_argument(
        "-q",
        "--probability-q",
        type=str,
        help="Distribution Q",
        dest="q",
        required=True,
    )
    parser_kl_divergence.set_defaults(func=fn_kl_divergence)

    #
    # Parser: Lempel-Ziv
    #
    parser_lempel_ziv = cmd.add_parser(
        "lempel-ziv",
        help=""
    )
    parser_lempel_ziv.add_argument(
        "-i",
        "--input",
        type=str,
        dest="input",
        required=True,
    )
    parser_lempel_ziv.add_argument(
        "-d",
        "--decode",
        action="store_true",
        help="If the input is an encoded Lempel-Ziv string, use this flag to decode it again.",
    )
    parser_lempel_ziv.add_argument(
        "--print-table",
        action="store_true",
        help="Print the Lempel-Ziv table to be able to follow the encoding/decoding manually.",
    )
    parser_lempel_ziv.set_defaults(func=fn_lempel_ziv)

    #
    # Parser: print/debug
    # 
    parser_print = cmd.add_parser("print", help="Prints the evaluated distribution. Supports to debug.")
    parser_print.add_argument(
        "-d",
        "--distribution",
        type=str,
        help="Path to the CSV-file which defines the discrete distribution",
        dest="distribution_file",
        required=True,
    )
    parser_print.set_defaults(func=fn_print)

    #
    # Parser: Shannon Entropy
    #
    parser_shannon_entropy = cmd.add_parser(
        "shannon-entropy",
        help="Calculate the Shannon-Entropy for a defined distribution.",
    )
    parser_shannon_entropy.add_argument(
        "-d",
        "--distribtution",
        type=str,
        help="Path to the CSV-file which defines the discrete distribtion",
        dest="distribution_file",
        required=True,
    )
    parser_shannon_entropy.set_defaults(func=fn_shannon_entropy)

    #
    # Parser: Smallest sufficient set
    # 
    parser_smallest_sufficient_set = cmd.add_parser(
        "smallest-sufficient-set",
        help="Calculate the smallest sufficient set",
    )
    parser_smallest_sufficient_set.add_argument(
        "-n",
        type=eval,
        help="Expression to define the length of the combinations of the input set",
        default=1,
    )
    parser_smallest_sufficient_set.add_argument(
        "-d",
        "--distribution",
        type=str,
        help="Path to the CSV-file which defines the discrete distribution",
        dest="distribution_file",
        required=True,
    )
    parser_smallest_sufficient_set.add_argument(
        "-D",
        "--delta",
        type=eval,
        help="Expression to define delta-boundary for the smallest sufficient set.",
        required=True
    )
    parser_smallest_sufficient_set.add_argument(
        "--print-probabilities",
        dest="print_probabilities",
        action="store_true",
        help="Print the probabilities among with the combinations of the smallest sufficient set.",
    )
    parser_smallest_sufficient_set.set_defaults(func=fn_smallest_sufficient_set)

    # 
    # Parser: typical set
    #
    parser_typical_set = cmd.add_parser("typical-set", help="Command to test on typical set")
    parser_typical_set.add_argument(
        "-d",
        "--distribution",
        type=str,
        help="Path to the CSV-file which defines the discrete distribution",
        dest="distribution_file",
        required=True,
    )
    parser_typical_set.add_argument(
        "-n",
        type=eval,
        help="Expression to define length of combinations in typical set",
        default=1,
    )
    parser_typical_set.add_argument(
        "-b",
        "--beta",
        type=eval,
        help="Expression to define boundary of the beta value",
        required=True,
    )
    parser_typical_set.add_argument(
        "--print-probabilities",
        dest="print_probabilities",
        action="store_true",
        help="Print the probabilities among with the combinations of the typical set.",
    )
    parser_typical_set.set_defaults(func=fn_typical_set)


    #
    # Parse all the arguments
    #
    args = parser.parse_args()

    try:
        # Last but not least, call the function of the corresponding command.
        args.func(args)
    except common.DistributionValueError as e:
        print(str(e), file=sys.stderr)
    except KeyboardInterrupt:
        # Valid interrupt to cancel the program
        pass
    except Exception as e:
        print(f"Unknown Error: {str(e)}", file=sys.stderr)

        if args.verbose:
            print(f"{traceback.format_exc(e)}")


if __name__ == "__main__":
    main()

