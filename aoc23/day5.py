import numpy as np


def process_input_5(input_5: list[str]):
    # Extract seeds from the first line of the file
    seeds = input_5[0].split(":")[1].split()
    seeds = [int(seed) for seed in seeds]

    maps = {}
    value = []

    for line in input_5[2:]:
        if line == "":
            # Line between maps
            maps[key] = value
            value = []

        elif ":" in line:
            # Start of new map
            key = line.split()[0]

        else:
            # Map values
            value.append([int(x) for x in line.split()])

    # No empty string after last map value, so update maps
    maps[key] = value

    return seeds, maps


def seed_location(seed_idx: int, maps: dict[str, list[list[int]]]) -> int:
    for key in maps:
        map_ranges = maps[key]

        for destination, source, n in map_ranges:
            if source <= seed_idx < source + n:
                seed_idx = destination + seed_idx - source
                break

    return seed_idx


def is_valid_seed(candidate: int, seed_pairs: np.ndarray) -> bool:
    for lower, n in seed_pairs:
        if lower <= candidate < lower + n:
            return True
    return False
