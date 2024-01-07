import numpy as np
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt


def process_input(input_strings):
    steps = [[s.strip("()") for s in line.split()] for line in input_strings]
    return steps


def compute_boundary(steps: list[list[str]]) -> tuple[list[tuple[int]], int]:
    # Initialise
    vertices = [(0, 0)]
    idx = (0, 0)

    # Also track the total boundary points
    n_boundary = 0

    for step in steps:
        direction, n = step[0], step[1]
        n = int(n)

        # Take steps in direction
        n_boundary += n
        if direction == "R":
            idx = (idx[0], idx[1] + n)
        if direction == "L":
            idx = (idx[0], idx[1] - n)
        if direction == "D":
            idx = (idx[0] + n, idx[1])
        if direction == "U":
            idx = (idx[0] - n, idx[1])

        vertices.append(idx)

    # Last vertex should be equal to first vertex, and is not needed
    assert vertices.pop() == vertices[0]

    return vertices, n_boundary


def shoelace_compute(vertices: list[tuple[int]]) -> int:
    area = 0

    # Loop over pairs of vertices around boundary
    for vertex_1, vertex_2 in zip(vertices, [*vertices[1:], vertices[0]]):
        area += vertex_1[0] * vertex_2[1] - vertex_1[1] * vertex_2[0]

    # Area will be negative if boundary is traversed clockwise
    return int(abs(area / 2))


def convert_colour_to_step(colour_string: str) -> tuple[str, int]:
    direction, n = colour_string[-1], colour_string[1:-1]
    n = int(n, 16)
    direction = {"0": "R", "1": "D", "2": "L", "3": "U"}[direction]

    return direction, n
