import math
import numpy as np
from itertools import combinations


def compute_sum_distances(puzzle_input, factor):
    # Array size
    n_rows = len(puzzle_input)
    n_cols = len(puzzle_input[0])

    # Track the empty rows/columns - initialise lists
    col_tracker = n_cols * [1]
    row_tracker = n_rows * [0]

    # Also record the locations of the galaxies
    galaxy_locs = []

    for row in range(n_rows):
        is_row_empty = 1
        for col, val in enumerate(puzzle_input[row]):
            if val == "#":
                # Record galaxy location
                galaxy_locs.append((row, col))

                # Update column tracker
                col_tracker[col] = 0

                is_row_empty = 0

        # Update column tracker
        row_tracker[row] = is_row_empty

    # Cumulative empty row trackers
    row_cumsum = np.cumsum(row_tracker)
    col_cumsum = np.cumsum(col_tracker)

    sum_distances = 0
    for (i1, j1), (i2, j2) in combinations(galaxy_locs, 2):
        # Number of empty rows/columns between these two galaxies
        row_expansion = row_cumsum[i2] - row_cumsum[i1]
        col_expansion = col_cumsum[j2] - col_cumsum[j1]

        # Taxicab + expansion metric
        distance = np.abs(i2 - i1 + (factor - 1) * row_expansion) + np.abs(
            j2 - j1 + (factor - 1) * col_expansion
        )

        # Convert back to native int, to avoid overflow errors with np.int32
        sum_distances += int(distance)

    return sum_distances
