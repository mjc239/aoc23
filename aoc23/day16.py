import matplotlib.pyplot as plt

LIGHT_DIRECTION = {}

# .
LIGHT_DIRECTION[(".", "n")] = "n"
LIGHT_DIRECTION[(".", "e")] = "e"
LIGHT_DIRECTION[(".", "s")] = "s"
LIGHT_DIRECTION[(".", "w")] = "w"

# /
LIGHT_DIRECTION[("/", "n")] = "e"
LIGHT_DIRECTION[("/", "e")] = "n"
LIGHT_DIRECTION[("/", "s")] = "w"
LIGHT_DIRECTION[("/", "w")] = "s"

# \
LIGHT_DIRECTION[("\\", "n")] = "w"
LIGHT_DIRECTION[("\\", "e")] = "s"
LIGHT_DIRECTION[("\\", "s")] = "e"
LIGHT_DIRECTION[("\\", "w")] = "n"

# |
LIGHT_DIRECTION[("|", "n")] = "n"
LIGHT_DIRECTION[("|", "s")] = "w"

# F
LIGHT_DIRECTION[("F", "n")] = "e"
LIGHT_DIRECTION[("F", "w")] = "s"

# 7
LIGHT_DIRECTION[("7", "n")] = "w"
LIGHT_DIRECTION[("7", "e")] = "s"

# |
LIGHT_DIRECTION[("|", "n")] = "n"
LIGHT_DIRECTION[("|", "s")] = "s"
LIGHT_DIRECTION[("|", "e")] = "ns"
LIGHT_DIRECTION[("|", "w")] = "ns"

# -
LIGHT_DIRECTION[("-", "n")] = "we"
LIGHT_DIRECTION[("-", "s")] = "we"
LIGHT_DIRECTION[("-", "e")] = "e"
LIGHT_DIRECTION[("-", "w")] = "w"


def new_index(row: int, col: int, direction: str):
    match direction:
        case "n":
            return (row - 1, col)
        case "e":
            return (row, col + 1)
        case "s":
            return (row + 1, col)
        case "w":
            return (row, col - 1)
        case "_":
            raise ValueError(f"direction {direction} not recognised!")


def find_charged_tiles(
    grid: list[str], start_tile: tuple[int] = None, start_direction: str = "e"
) -> set[tuple[int]]:
    n_rows = len(grid)
    n_cols = len(grid[0])
    start_tile = start_tile or (0, 0)

    # Keep track of charged tiles in a set
    # Use stack to keep track of visited tiles with direction
    charged_tiles = set()
    stack = [(start_tile, start_direction)]

    # Continue while there still exist visited tiles on stack
    while len(stack) > 0:
        # Take next visited tile from stack
        (row, col), direction = stack.pop()
        charged_tiles.add(((row, col), direction))
        tile_type = grid[row][col]
        direction = LIGHT_DIRECTION[(tile_type, direction)]

        # May have multiple directions from splitter
        for char in direction:
            # Check if going off edge of grid
            row, col = new_index(row, col, char)
            valid_index = (0 <= row < n_rows) and (0 <= col < n_cols)

            # Check if we have already seen this (tile, direction) pair
            # Without this check, we can go round in circles forever
            seen_state = ((row, col), direction) in charged_tiles

            if valid_index and not seen_state:
                stack.append(((row, col), char))

    # Drop directions, just return tiles
    return set([tile[0] for tile in charged_tiles])


def visualise_charged_tiles(
    grid: list[str],
    charged_tiles: set(tuple[int]),
    start_tile: tuple[int],
    plot_factor: float = None,
):
    n_rows = len(grid)
    n_cols = len(grid[0])
    plot_factor = plot_factor or 15 / n_cols

    # Construct binary matrix, with 1s along the beam path
    mat = []
    for i in range(n_rows):
        line = []
        for j in range(n_cols):
            if (i, j) in charged_tiles:
                line.append(1)
            else:
                line.append(0)
        mat.append(line)

    # Indicate the starting tile
    mat[start_tile[0]][start_tile[1]] = 0.75

    # Plot path, along with tile types
    fig, ax = plt.subplots(figsize=(plot_factor * n_cols, plot_factor * n_rows))
    ax.matshow(mat)
    for i in range(n_rows):
        for j in range(n_cols):
            text = ax.text(
                j, i, grid[i][j].replace("-", "--"), ha="center", va="center", color="b"
            )


def maximise_charged_tiles(grid: list[str]) -> tuple[tuple[int], str, int]:
    n_rows = len(grid)
    n_cols = len(grid[0])

    # Keep track of maximums
    max_charge = 0
    max_start_tile = None
    max_direction = None

    # Top edge
    for j in range(n_cols):
        n = len(find_charged_tiles(grid, start_tile=(0, j), start_direction="s"))
        if n > max_charge:
            max_charge = n
            max_start_tile = (0, j)
            max_direction = "s"

    # Left edge
    for i in range(n_rows):
        n = len(find_charged_tiles(grid, start_tile=(i, 0), start_direction="e"))
        if n > max_charge:
            max_charge = n
            max_start_tile = (i, 0)
            max_direction = "e"

    # Bottom edge
    for j in range(n_cols):
        n = len(
            find_charged_tiles(grid, start_tile=(n_rows - 1, j), start_direction="n")
        )
        if n > max_charge:
            max_charge = n
            max_start_tile = (n_rows - 1, j)
            max_direction = "n"

    # Right edge
    for i in range(n_rows):
        n = len(
            find_charged_tiles(grid, start_tile=(i, n_cols - 1), start_direction="w")
        )
        if n > max_charge:
            max_charge = n
            max_start_tile = (i, n_cols - 1)
            max_direction = "w"

    return max_start_tile, max_direction, max_charge
