from dataclasses import dataclass, field
from itertools import combinations
import numpy as np


@dataclass
class Hailstone:
    position: list = field(default_factory=list)
    velocity: list = field(default_factory=list)


def process_input(input_lines):
    stones = []
    for line in input_lines:
        pos, vel = line.split(" @ ")
        stones.append(
            Hailstone(
                position=[int(x) for x in pos.split(", ")],
                velocity=[int(x) for x in vel.split(", ")],
            )
        )
    return stones


def count_2d_intersections(stones, bounds):
    intersections = 0

    # Loop over all pairs of intersections
    for stone1, stone2 in combinations(stones, 2):
        p1x, p1y = stone1.position[0], stone1.position[1]
        p2x, p2y = stone2.position[0], stone2.position[1]
        v1x, v1y = stone1.velocity[0], stone1.velocity[1]
        v2x, v2y = stone2.velocity[0], stone2.velocity[1]

        # Check if velocities are parallel
        det = v1x * v2y - v1y * v2x
        if det == 0:
            continue

        # Times of intersection
        t1 = ((p2x - p1x) * v2y - (p2y - p1y) * v2x) / (v1x * v2y - v1y * v2x)
        t2 = ((p1x - p2x) * v1y - (p1y - p2y) * v1x) / (v2x * v1y - v2y * v1x)

        # Remove past intersections
        if t1 < 0 or t2 < 0:
            continue

        # Check in bounds
        p = [p1x + t1 * v1x, p1y + t1 * v1y]
        if not bounds[0] <= p[0] <= bounds[1]:
            continue
        if not bounds[0] <= p[1] <= bounds[1]:
            continue

        intersections += 1

    return intersections


def compute_throw_intersection(stones):
    # Convenient helper quantities
    # Using the first three stones as the default
    X = np.cross(stones[0].position, stones[0].velocity)
    Y = np.cross(stones[1].position, stones[1].velocity)
    Z = np.cross(stones[2].position, stones[2].velocity)

    a = stones[0].position
    b = stones[0].velocity
    m = stones[1].position
    n = stones[1].velocity
    p = stones[2].position
    q = stones[2].velocity

    # Matrix to invert
    M = [
        [0, b[2], -b[1], 0, -a[2], a[1], -1, 0, 0],
        [-b[2], 0, b[0], a[2], 0, -a[0], 0, -1, 0],
        [b[1], -b[0], 0, -a[1], a[0], 0, 0, 0, -1],
        [0, n[2], -n[1], 0, -m[2], m[1], -1, 0, 0],
        [-n[2], 0, n[0], m[2], 0, -m[0], 0, -1, 0],
        [n[1], -n[0], 0, -m[1], m[0], 0, 0, 0, -1],
        [0, q[2], -q[1], 0, -p[2], p[1], -1, 0, 0],
        [-q[2], 0, q[0], p[2], 0, -p[0], 0, -1, 0],
        [q[1], -q[0], 0, -p[1], p[0], 0, 0, 0, -1],
    ]

    # Target vector
    v = [X[0], X[1], X[2], Y[0], Y[1], Y[2], Z[0], Z[1], Z[2]]

    # Solve and
    sol = np.matmul(np.linalg.inv(M), v)
    p, v, c = sol[:3], sol[3:6], sol[6:]

    # Check that c = p x v
    assert np.allclose(np.cross(p, v), c)

    return p, v
