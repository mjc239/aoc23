import math


def roll_east(grid: list[str]) -> list[str]:
    return [
        "#".join(["".join(sorted(round_rocks)) for round_rocks in row.split("#")])
        for row in grid
    ]


def transpose(grid: list[str]) -> list[str]:
    return list(map(lambda x: "".join(x), zip(*grid)))


def roll_direction(grid: list[str], direction: str) -> list[str]:
    match direction.lower():
        case "n":
            # Flip -> transpose -> tilt east -> transpose -> flip
            flipped_grid = transpose(grid[::-1])
            rolled_grid = roll_east(flipped_grid)
            return transpose(rolled_grid)[::-1]

        case "e":
            return roll_east(grid)

        case "s":
            # Transpose -> tilt east -> transpose
            flipped_grid = transpose(grid)
            rolled_grid = roll_east(flipped_grid)
            return transpose(rolled_grid)

        case "w":
            # Flip -> tilt east -> flip
            flipped_grid = [row[::-1] for row in grid]
            rolled_grid = roll_east(flipped_grid)
            return [row[::-1] for row in rolled_grid]

        case _:
            raise ValueError("Direction not recognised!")


def compute_load(grid: list[str]) -> int:
    n_rows = len(grid)

    load = 0
    for i, row in enumerate(grid):
        # Number of rocks in row
        n_rocks = sum([char == "O" for char in row])

        # Load contribution from row
        load += n_rocks * (n_rows - i)

    return load


def spin_cycle(grid: list[str]) -> list[str]:
    grid = roll_direction(grid, "n")
    grid = roll_direction(grid, "w")
    grid = roll_direction(grid, "s")
    grid = roll_direction(grid, "e")

    return grid


def spin_cycle_n_times(input_grid: list[str], N: int) -> list[str]:
    # Initialise to keep track of found grids
    grid = input_grid
    found_grids = {"".join(grid): 0}

    # Loop up to N (max possible value needed)
    for i in range(N):
        grid = spin_cycle(grid)
        grid_str = "".join(grid)  # hashable

        if grid_str in found_grids:
            # Already found grid - compute n and c
            # and stop iterating
            n_plus_c = i + 1
            n = found_grids[grid_str]
            c = n_plus_c - n
            break

        else:
            # Add new grid to dictionary
            found_grids[grid_str] = i + 1
    else:
        # return final grid, if no previously
        # found grid observed
        return grid

    # remainder and new N
    print(f"n = {n}, c = {c}")
    r = (N - n) % c
    N_hat = n + r

    # Invert grid
    final_grid = [k for k, v in found_grids.items() if v == N_hat][0]

    # Convert grid_str back into grid
    m, n = len(input_grid), len(input_grid[0])
    return [final_grid[n * i : n * (i + 1)] for i in range(m)]
