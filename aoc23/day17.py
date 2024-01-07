import math
from itertools import product
from heapq import heapify, heappop, heappush
import matplotlib.pyplot as plt
import numpy as np


class PathFinder:
    def __init__(self, grid: list[str], min_step: int = 1, max_step: int = 3):
        self.grid = grid
        self.min_step = min_step
        self.max_step = max_step

        self.n_rows = len(grid)
        self.n_cols = len(grid[0])

        # Initialise f-scores and g-scores to infinity
        # Also initialise for the starting node
        self.g_score = {
            (row, col, parity): math.inf
            for row, col, parity in product(
                range(self.n_rows), range(self.n_cols), [0, 1]
            )
        }
        self.g_score[(0, 0, 0)] = 0
        self.g_score[(0, 0, 1)] = 0

        self.f_score = {
            (row, col, parity): math.inf
            for row, col, parity in product(
                range(self.n_rows), range(self.n_cols), [0, 1]
            )
        }
        self.f_score[(0, 0, 0)] = self.n_rows + self.n_cols - 2
        self.f_score[(0, 0, 1)] = self.n_rows + self.n_cols - 2

        # Create node heap
        self.nodes = []
        heapify(self.nodes)

        # Help to track the optimal paths
        self.came_from = {}
        self.optimal_came_from = {}
        self.optimal_path_found = False

    def compute_path(self):
        # Add the start node to the heap
        # One for each possible starting parity
        # Store as (f(n), n), so that natural ordering is
        # used by heap to order by f-score
        heappush(self.nodes, (self.f_score[(0, 0, 0)], (0, 0, 0)))
        heappush(self.nodes, (self.f_score[(0, 0, 1)], (0, 0, 1)))

        while len(self.nodes) > 0:
            # Pop the node with the best fscore
            _, (row, col, parity) = heappop(self.nodes)

            if row == self.n_rows - 1 and col == self.n_cols - 1:
                # Reached final node - terminate
                self.optimal_path_found = True
                return None

            # Defines the range of steps the crucible can take (see part 2)
            step_range = [
                *range(-self.max_step, -self.min_step + 1),
                *range(self.min_step, self.max_step + 1),
            ]

            for i in step_range:
                # Check if this is a valid neighbouring node
                if parity % 2 == 0:
                    if not 0 <= row + i < self.n_rows:
                        continue
                    if i < 0:
                        d = sum([int(self.grid[row + k][col]) for k in range(i, 0)])
                    else:
                        d = sum([int(self.grid[row + k][col]) for k in range(1, i + 1)])

                    neighbour = (row + i, col, (parity + 1) % 2)
                else:
                    if not 0 <= col + i < self.n_cols:
                        continue
                    if i < 0:
                        d = sum([int(self.grid[row][col + k]) for k in range(i, 0)])
                    else:
                        d = sum([int(self.grid[row][col + k]) for k in range(1, i + 1)])

                    neighbour = (row, col + i, (parity + 1) % 2)

                # Compute tentative g-score, and compare to current g-score
                tent_gscore = self.g_score[(row, col, parity)] + d
                if tent_gscore < self.g_score[neighbour]:
                    # Update came_from, g_score and f_score using heuristic h
                    self.came_from[neighbour] = (row, col)
                    self.g_score[neighbour] = tent_gscore
                    self.f_score[neighbour] = (
                        tent_gscore
                        + (self.n_rows - 1)
                        - neighbour[0]
                        + (self.n_cols - 1)
                        - neighbour[1]
                    )
                    # Push new node to heap
                    if neighbour not in self.nodes:
                        heappush(self.nodes, (self.f_score[neighbour], neighbour))

        # If heap is emptied before reaching final node, there is no valid path
        raise ValueError("A* algorithm failed!")

    def find_best(self):
        assert self.optimal_path_found, "Find optimal path first!"

        # There are 2 ways to reach the final tile (with each of the possible parities)
        # Find the one with the minimal g-score
        final_tiles = [
            self.g_score[(self.n_rows - 1, self.n_cols - 1, 0)],
            self.g_score[(self.n_rows - 1, self.n_cols - 1, 1)],
        ]
        print(f"Best final total: {min(final_tiles)}")

        self.optimal_came_from = {}

        if final_tiles[0] < final_tiles[1]:
            parity = 0
        else:
            parity = 1

        # Construct the optimal path, without the irrelevant parity
        node = (self.n_rows - 1, self.n_cols - 1)
        while node != (0, 0):
            prev_node_parity = self.came_from[(node[0], node[1], parity)]
            self.optimal_came_from[node] = (prev_node_parity[0], prev_node_parity[1])
            node = self.optimal_came_from[node]
            parity = (parity + 1) % 2

        return self.optimal_came_from

    def plot_path(self, **fig_kwargs):
        assert self.optimal_path_found, "Find optimal path first!"

        # Create a matrix with 1s along the optimal path
        # and 0s everywhere else
        p = np.zeros([self.n_rows, self.n_cols])
        p[self.n_rows - 1, self.n_cols - 1] = 1
        node = (self.n_rows - 1, self.n_cols - 1)

        # Traverse path from node to node
        while node != (0, 0):
            new_node = self.optimal_came_from[node]
            if new_node[0] < node[0]:
                for i in range(new_node[0], node[0] + 1):
                    p[i, node[1]] = 1

            elif new_node[0] > node[0]:
                for i in range(node[0], new_node[0] + 1):
                    p[i, node[1]] = 1

            elif new_node[1] < node[1]:
                for j in range(new_node[1], node[1] + 1):
                    p[node[0], j] = 1

            elif new_node[1] > node[1]:
                for j in range(node[1], new_node[1] + 1):
                    p[node[0], j] = 1

            node = new_node

        # Plot the optimal path over the top of a heat map
        # showing the costs of each tile
        fig, ax = plt.subplots(**fig_kwargs)
        ax.matshow(
            np.maximum(
                9 * p,
                np.array(
                    [
                        [int(self.grid[i][j]) for j in range(self.n_cols)]
                        for i in range(self.n_rows)
                    ]
                ),
            )
        )

        return fig, ax
