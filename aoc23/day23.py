from itertools import pairwise
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def compute_longest_path(grid, bad_shoes=True):
    n_rows = len(grid)
    n_cols = len(grid[0])

    # Path starts at starting square
    # Add path to stack
    paths = [[(0, 1)]]

    longest_path = []

    while paths:
        path = paths.pop()

        # Find neighbours of
        # last tile in path
        row, col = path[-1]
        possible_neighbours = [
            ((row - 1, col), "N"),
            ((row + 1, col), "S"),
            ((row, col - 1), "W"),
            ((row, col + 1), "E"),
        ]

        for new_tile, direction in possible_neighbours:
            if new_tile == (n_rows - 1, n_cols - 2):
                # New complete path found
                # but only add if longer
                if len(path) > len(longest_path):
                    longest_path = [*path, new_tile]
                continue

            # Continue if new tile outside of grid
            if not 0 <= new_tile[0] < n_rows:
                continue
            if not 0 <= new_tile[1] < n_cols:
                continue

            # Continue if new tile is a wall
            tile_type = grid[new_tile[0]][new_tile[1]]
            if tile_type == "#":
                continue

            # If wearing bad shoes and new tile
            # is directional, check direction
            if bad_shoes:
                match (tile_type, direction):
                    case ("v", "N"):
                        continue
                    case ("<", "E"):
                        continue
                    case (">", "W"):
                        continue
                    case ("^", "S"):
                        continue

            # Continue if new tile
            if new_tile in path:
                continue

            # Add new path to the stack
            new_path = [*path, new_tile]
            paths.append(new_path)

    return longest_path


def plot_path(grid, longest_path, **fig_kwargs):
    n_rows = len(grid)
    n_cols = len(grid[0])

    # Create a matrix with 1s along the path
    # and 0s everywhere else
    p = np.zeros([n_rows, n_cols])
    for tile in longest_path:
        p[tile[0], tile[1]] = 1

    # Plot the optimal path over the top of a heat map
    # showing the costs of each tile
    fig, ax = plt.subplots(**fig_kwargs)
    ax.matshow(
        np.maximum(
            2 * p, [[grid[i][j] == "#" for j in range(n_cols)] for i in range(n_rows)]
        )
    )
    ax.axis("off")
    return fig, ax


def compute_nodes(grid):
    n_rows = len(grid)
    n_cols = len(grid[0])

    # Track nodes (fork tiles), and
    # segments (paths between fork tiles)
    nodes = [(0, 1)]
    segments = {}
    paths = [[(0, 1), (1, 1)]]

    while paths:
        path = paths.pop()

        # For current path, find all
        # potential neighbours
        row, col = path[-1]
        possible_neighbours = [
            ((row - 1, col), "N"),
            ((row + 1, col), "S"),
            ((row, col - 1), "W"),
            ((row, col + 1), "E"),
        ]

        # Work out if the new tile is a fork
        actual_neighbours = []
        for new_tile, direction in possible_neighbours:
            # Skip if not in grid
            if not 0 <= new_tile[0] < n_rows:
                continue
            if not 0 <= new_tile[1] < n_cols:
                continue

            # Skip if path is self-intersecting
            if new_tile in path:
                continue

            # Skip if new tile is a wall
            tile_type = grid[new_tile[0]][new_tile[1]]
            if tile_type == "#":
                continue

            actual_neighbours.append(new_tile)

        # 3 different cases for tile type
        n_neighbours = len(actual_neighbours)
        if n_neighbours == 0:
            # Reached end tile
            segments[(path[0], (row, col))] = path
            nodes.append((row, col))

        elif n_neighbours > 1:
            # Reached fork - add to nodes
            # if not already added
            if (row, col) not in nodes:
                for n in actual_neighbours:
                    # Add new paths to stack
                    paths.append([(row, col), n])
                nodes.append((row, col))

            # Make record of segment
            segments[(path[0], (row, col))] = path

        elif n_neighbours == 1:
            # Continue along path
            for n in actual_neighbours:
                paths.append([*path, n])

    return nodes, {tuple(sorted(k)): v for k, v in segments.items()}


def compute_longest_graph_path(graph, start, end):
    # Create paths stack
    paths = [[start]]

    # Track longest path seen so far
    max_length = 0
    max_path = []

    while paths:
        path = paths.pop()

        if path[-1] == end:
            # Reached final node (end tile)
            # Find path length
            length = 0
            for n1, n2 in zip(path[:-1], path[1:]):
                length += graph.edges[(n1, n2)]["weight"]

            # Save path if longest so far
            if length > max_length:
                max_length = length
                max_path = path

            # Skip to next path in stack
            continue

        # Find neighbours from graph adjacency matrix
        neighbours = list(graph.adj[path[-1]])

        for n in neighbours:
            if n not in path:
                # Add path if not self-intersecting
                paths.append([*path, n])

    return max_path, max_length


def plot_path_from_segments(grid, path_nodes, segments, **fig_kwargs):
    # Create a matrix with 1s along the path
    # and 0s everywhere else
    n_rows = len(grid)
    n_cols = len(grid[0])
    p = np.zeros([n_rows, n_cols])

    # Loop over nodes in longest path
    for node_1, node_2 in pairwise(path_nodes):
        # Find tiles along segment
        # connecting these nodes
        key = tuple(sorted((node_1, node_2)))
        for row, col in segments[key]:
            p[row, col] = 1

    # Plot the optimal path over the top of a heat map
    # showing the costs of each tile
    fig, ax = plt.subplots(**fig_kwargs)
    ax.matshow(
        np.maximum(
            2 * p, [[grid[i][j] == "#" for j in range(n_cols)] for i in range(n_rows)]
        )
    )
    ax.axis("off")
    return fig, ax


def compute_longest_graph_path_with_perimeter(graph, start, end, perimeter_segments):
    # Stack of paths, represented as dicts
    paths = [{start: None}]

    # Track longest path seen so far
    max_length = 0
    max_path = []

    # Graph adjacency and edge information
    weights = {
        tuple(sorted(edge)): weight["weight"] for edge, weight in graph.edges.items()
    }
    adj = {node: list(nodes.keys()) for node, nodes in graph.adj.items()}

    while paths:
        path = paths.pop()
        path_keys = list(path.keys())

        if path_keys[-1] == end:
            # Reached final node (end tile)
            # Find path length
            length = 0
            for n1, n2 in zip(path_keys[:-1], path_keys[1:]):
                length += weights[tuple(sorted((n1, n2)))]

            # Save path if longest so far
            if length > max_length:
                max_length = length
                max_path = path_keys

            # Skip to next path in stack
            continue

        # Find neighbours from graph adjacency dict
        neighbours = adj[path_keys[-1]]

        for n in neighbours:
            # Add path if not self-intersecting
            # and not in wrong direction around perimeter
            if (n not in path) and ((n, path_keys[-1]) not in perimeter_segments):
                paths.append({**path, n: None})

    return max_path, max_length
