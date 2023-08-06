"""
This module of the framework defines the Lempel-Ziv coding algorithm,
which is a lossless data compression technique used to reduce the size
of data.
It works by finding repeating patterns in the input data and replacing
them with shorter codes. 

The example input for decoding may be: 1011010100010

Example:

    its-ut lempel-ziv -i 1011010100010

        Encodes the input string to a Lempel-Ziv code.
        Produces: 100011101100001000010

    its-ut lempel-ziv -i 100011101100001000010 --decode

        Decodes an already encoded Lempel-Ziv code.
        Produces: 1011010100010 

"""

import sys

from its import common

def fn(args):
    """
    """
    input = args.input
    code = decode(input) if args.decode else encode(input)

    print(f"{code}")

    print(f"Input Length: {len(input)}", file=sys.stderr)
    print(f"Code Length: {len(code)}", file=sys.stderr)


def encode(input: str , print_table: bool = False):
    source_substrings = ['lambda']

    current_substring = ''
    for character in input:
        current_substring += character
        if current_substring not in source_substrings:
            source_substrings.append(current_substring)
            current_substring = ''

    table = []
    table.append(source_substrings)

    indexes_decimal = []
    indexes_binary = []
    for index, substring in enumerate(source_substrings):
        indexes_decimal.append(str(index))
        indexes_binary.append(str(bin(index)[2:]))

    table.append(indexes_decimal)
    table.append(indexes_binary)

    pointer_bit = []
    for index, substring in enumerate(source_substrings):
        if substring == 'lambda':
            pointer_bit.append("-")
        else:
            if index == 1:
                pointer_bit.append("," + substring)
            else:
                index_found_substring = first_substring(source_substrings, substring, index)
                binary_index_found_substring = indexes_binary[index_found_substring]

                binary_index_found_substring_len = len(binary_index_found_substring)
                binary_index_needed_substring_len = len(indexes_binary[index - 1])
                binary_dif = binary_index_needed_substring_len - binary_index_found_substring_len

                pointer_bit.append("".join(["0"] * binary_dif) + binary_index_found_substring + "," + substring[-1])

    table.append(pointer_bit)
    for row in table:
        row_str = " | ".join(
            "{0:{1}}".format(cell, max(len(str(cell)) for row in table for cell in row)) for cell in row)
        
        if print_table:
            print(f"{row_str}", file=sys.stderr)

    encoding = ""
    for index, pointer_bit_comb in enumerate(pointer_bit):
        if index > 0:
            encoding += "".join(pointer_bit_comb.split(","))
    return encoding


def first_substring(source_substrings, substring, index_substring):
    for index, substring_to_find in enumerate(source_substrings):
        if index == index_substring:
            return 0
        if substring_to_find == substring[:-1]:
            return index


def decode(input: str, print_table: bool=False):
    index = 0
    source_substrings = []
    indexes_decimal = []
    indexes_binary = []
    pointer_bit = []

    while input != "":
        if index == 0:
            source_substrings.append("lambda")
            indexes_decimal.append(str(index))
            indexes_binary.append(str(bin(index)[2:]))
            pointer_bit.append('-')
        elif index == 1:
            source_substrings.append(input[0])
            indexes_decimal.append(str(index))
            indexes_binary.append(str(bin(index)[2:]))
            pointer_bit.append(',' + input[0])
            input = input[1:]
        else:
            indexes_decimal.append(str(index))
            prev_index_binary = indexes_binary[-1]
            indexes_binary.append(str(bin(index)[2:]))
            prev_index_binary_length = len(prev_index_binary)
            pointer = input[:prev_index_binary_length]
            bit = input[prev_index_binary_length:prev_index_binary_length + 1]
            pointer_bit.append(pointer + "," + bit)
            while True:
                if len(pointer) > 1 and pointer[0] == "0":
                    pointer = pointer[1:]
                else:
                    break
            pointer_decimal = indexes_binary.index(pointer)

            if source_substrings[pointer_decimal] == "lambda":
                source_substrings.append(bit)
            else:
                source_substrings.append(source_substrings[pointer_decimal] + bit)

            input = input[prev_index_binary_length + 1:]

        index += 1

    table = []
    table.append(source_substrings)
    table.append(indexes_decimal)
    table.append(indexes_binary)
    table.append(pointer_bit)

    for row in table:
        row_str = " | ".join(
            "{0:{1}}".format(cell, max(len(str(cell)) for row in table for cell in row)) for cell in row)
        if print_table:
            print(f"{row_str}", file=sys.stderr)

    decoding = ""
    for index, source_substring in enumerate(source_substrings):
        if index > 0:
            decoding += "".join(source_substring)
    return decoding
