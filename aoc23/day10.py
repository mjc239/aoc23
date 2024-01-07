import math

pipe_direction = {}

# L
pipe_direction[("L", "s")] = "e"
pipe_direction[("L", "w")] = "n"

# J
pipe_direction[("J", "s")] = "w"
pipe_direction[("J", "e")] = "n"

# F
pipe_direction[("F", "n")] = "e"
pipe_direction[("F", "w")] = "s"

# 7
pipe_direction[("7", "n")] = "w"
pipe_direction[("7", "e")] = "s"

# |
pipe_direction[("|", "n")] = "n"
pipe_direction[("|", "s")] = "s"

# -
pipe_direction[("-", "e")] = "e"
pipe_direction[("-", "w")] = "w"


def count_inside_loop(
    input_list: list[str], loop_index_dict: dict[tuple[int], int]
) -> int:
    # Array size
    n_rows = len(input_list)
    n_cols = len(input_list[0])

    # Keep track of the inside tiles
    num_inside_loop = 0

    # Iterate over tiles line by line
    for i in range(n_rows):
        # Always start a row outside the loop
        inside_loop = False

        # Keep track of the loop tile section when crossing
        loop_tile_list = []

        for j in range(n_cols):
            tile = input_list[i][j]

            # Is this a loop tile? Check the loop_index_dict
            is_loop_tile = (i, j) in loop_index_dict

            if is_loop_tile:
                if tile == "|":
                    # Switch from in <-> out
                    inside_loop = not inside_loop
                    loop_tile_list = []

                elif tile in ["-", "F", "L"]:
                    # Start/middle of loop tile section
                    loop_tile_list.append(tile)

                elif (loop_tile_list[0] == "F" and tile == "7") or (
                    loop_tile_list[0] == "L" and tile == "J"
                ):
                    # F7 or LJ type - not a true crossing
                    loop_tile_list = []

                elif (loop_tile_list[0] == "F" and tile == "J") or (
                    loop_tile_list[0] == "L" and tile == "7"
                ):
                    # FJ or L7 type - switch from in <-> out
                    inside_loop = not inside_loop
                    loop_tile_list = []

            elif inside_loop:
                # Add to the counter if inside loop
                num_inside_loop += 1

    return num_inside_loop
