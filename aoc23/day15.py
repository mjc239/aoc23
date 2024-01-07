import math


def hash_algorithm(string: str) -> int:
    ascii_codes = [ord(char) for char in string]
    current_value = 0
    for code in ascii_codes:
        current_value += code
        current_value = (17 * current_value) % 256
    return current_value


def place_lenses(steps: list[str]) -> list[dict[str, int]]:
    # Each box: {label: focal}
    boxes = [{} for _ in range(256)]

    for step in steps:
        if step[-1] == "-":
            # Get label and box index
            label = step[:-1]
            box_idx = hash_algorithm(label)

            # Remove lens (if it exists)
            boxes[box_idx].pop(label, None)

        elif "=" in step:
            # Get label, focal length and box index
            label, focal = step.split("=")
            box_idx = hash_algorithm(label)

            # Replace or add lens
            boxes[box_idx][label] = int(focal)

        else:
            raise ValueError("invalid step!")

    return boxes


def compute_focusing_power(boxes):
    power = 0
    for box_num, box in enumerate(boxes):
        for slot, (label, focal) in enumerate(box.items()):
            power += (box_num + 1) * (slot + 1) * focal
    return power
