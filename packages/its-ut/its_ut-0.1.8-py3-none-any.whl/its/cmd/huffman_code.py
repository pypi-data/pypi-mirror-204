"""
This module of the framework defines the Huffman coding algorithm, which
is a lossless data compression technique used to reduce the size of data.
This file generates a binary code for each character in the input
distribution based on the frequency of occurrence. This module includes
functions for encoding data using the generated Huffman codes and
visualises the Huffman tree.
"""


import copy
import networkx as nx
import matplotlib.pyplot as plt
import math
import sys

from its import common

def fn(args):
    distribution = common.load_distribution(args.distribution_file)
    encode(distribution, print_graph_information=args.print_graph_information)


def encode(p: dict, print_graph_information: bool = False):

    if print_graph_information:
        print("Input probabilities", file=sys.stderr)
        print(p, file=sys.stderr)

    probabilities = copy.deepcopy(p)
    vertices = []
    edges = []

    while True:
        if len(probabilities) == 1:
            vertices.append(list(probabilities.keys())[0])
            break

        sorted_probabilities = sorted(probabilities.items(), key=lambda x: x[1])

        minimum_probability_1, minimum_probability_2 = sorted_probabilities[:2]

        del probabilities[minimum_probability_1[0]]
        del probabilities[minimum_probability_2[0]]

        combined_label = minimum_probability_1[0] + " + " + minimum_probability_2[0]
        combined_value = minimum_probability_1[1] + minimum_probability_2[1]
        probabilities[combined_label] = combined_value

        edges.append((combined_label, minimum_probability_1[0], 1))
        edges.append((combined_label, minimum_probability_2[0], 0))
        vertices.append(minimum_probability_1[0])
        vertices.append(minimum_probability_2[0])

    if print_graph_information:
        print("vertices:", file=sys.stderr)
        print(vertices, file=sys.stderr)
        print("edges:", file=sys.stderr)
        print(edges, file=sys.stderr)

    graph = nx.DiGraph()

    for from_edge, to_edge, weight in edges:
        graph.add_edge(from_edge, to_edge, weight=weight)

    graph.add_nodes_from(vertices)

    positions = {}

    k = 1
    def assign_positions(node, parent, depth, coordinate, k):
        positions[node] = (-depth, coordinate)

        children = [n for n in graph.neighbors(node) if n != parent]

        if len(children) > 0:
            spacing = 1 / len(children) + k

            start = coordinate - spacing / 2

            for i, child in enumerate(children):
                assign_positions(child, node, depth + 1, start + i * spacing, k-0.5)

    assign_positions(vertices[-1], None, 0, 0, 1)

    nx.draw(graph, pos=positions, with_labels=True, node_size=800, node_color='lightgreen', font_size=18, font_weight='bold')
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, positions, edge_labels=edge_labels, font_size=14)
    plt.show()

    dfs(graph, vertices[-1], [])


def generate_positions(num_vertices):
    positions = {}
    levels = math.floor(math.log(num_vertices, 2)) + 1
    spacing = 1 / (2 ** (levels - 1))

    for level in range(levels):
        y = -level
        nodes = 2 ** level

        start = -spacing * (nodes - 1) / 2
        for i in range(nodes):
            x = start + i * spacing

            vertex = nodes + i
            positions[vertex] = (x, y)
    return positions


def dfs(graph, node, path):
    if len(list(graph.successors(node))) == 0:
        print("Node: " + node + " Path: " + ''.join(path), file=sys.stderr)

    for successor in graph.successors(node):
        new_path = path.copy()
        new_path.append(str(graph[node][successor]['weight']))
        dfs(graph, successor, new_path)