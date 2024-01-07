def process_input(input_list: list[str]) -> list[list[str]]:
    out = []
    this_grid = []
    for line in input_list:
        if line == "":
            out.append(this_grid)
            this_grid = []
        else:
            this_grid.append(line)
    out.append(this_grid)
    return out


def summarise_notes(grid: list[str], num_differences=0) -> int:
    # n columns, m rows
    n = len(grid[0])
    m = len(grid)

    # A neat way to transpose a list of strings!
    transposed_grid = list(map(lambda x: "".join(x), zip(*grid)))

    # Check each potential row/column mirror position
    # Exact reflections will have 0 differences
    potential_horizontal_line = [
        sum_differences(grid[j::-1], grid[j + 1 :]) for j in range(m - 1)
    ]
    potential_vertical_line = [
        sum_differences(transposed_grid[i::-1], transposed_grid[i + 1 :])
        for i in range(n - 1)
    ]

    # Compute the summaries by finding entries with 0 differences
    horizontal_summary = sum(
        [
            100 * (j + 1)
            for j, val in enumerate(potential_horizontal_line)
            if val == num_differences
        ]
    )
    vertical_summary = sum(
        [
            i + 1
            for i, val in enumerate(potential_vertical_line)
            if val == num_differences
        ]
    )

    # Puzzle leaves open possibility of multiple mirror lines
    return horizontal_summary + vertical_summary


def sum_differences(half_1: list[str], half_2: list[str]) -> int:
    # Only compare the overlapping portions
    min_length = min(len(half_1), len(half_2))
    half_1 = half_1[:min_length]
    half_2 = half_2[:min_length]

    # For each half of the array, compare the corresponding strings
    # Sum the number of differences between each pair
    diffs = [
        sum([char_1 != char_2 for char_1, char_2 in zip(string_1, string_2)])
        for string_1, string_2 in zip(half_1, half_2)
    ]

    return sum(diffs)
