import math
import numpy as np


def next_element(sequence):
    diffs = []
    while any(sequence):
        diffs.append(sequence)
        sequence = np.diff(sequence)

    return sum([diff[-1] for diff in diffs])
