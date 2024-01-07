import networkx as nx


def process_input(input_list):
    g = nx.Graph()

    # Define and add all the edges from each line
    for line in input_list:
        node1, conns = line.split(": ")
        for conn in conns.split():
            g.add_edge(node1, conn, name=f"{node1} -> {conn}")

    return g
