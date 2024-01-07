import math
import matplotlib.pyplot as plt


def bounds(time: int, distance: int) -> tuple[float]:
    disc = time**2 - 4 * distance
    if disc < 0:
        raise ValueError("No real solutions!")

    sqrt_disc = math.sqrt(disc)
    return (0.5 * (time - sqrt_disc), 0.5 * (time + sqrt_disc))
