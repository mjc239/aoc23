from copy import deepcopy
from heapq import heapify, heappop, heappush
from collections import deque, defaultdict
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as mcolors
import networkx as nx


class Block:
    def __init__(self, ends):
        self.cubes = self._compute_cubes(ends)
        self.length = len(self.cubes)
        self.minx = min(self.cubes[0][0], self.cubes[-1][0])
        self.maxx = max(self.cubes[0][0], self.cubes[-1][0])
        self.miny = min(self.cubes[0][1], self.cubes[-1][1])
        self.maxy = max(self.cubes[0][1], self.cubes[-1][1])
        self.minz = min(self.cubes[0][2], self.cubes[-1][2])
        self.maxz = max(self.cubes[0][2], self.cubes[-1][2])
        self.set_id()

    def __repr__(self):
        return self.id

    def set_id(self):
        self.id = f"({self.minx}, {self.miny}, {self.minz}) -> ({self.maxx}, {self.maxy}, {self.maxz})"

    @staticmethod
    def _compute_cubes(ends):
        # Process the input string into a list of cubes
        end1, end2 = ends.split("~")
        end1 = np.array([int(x) for x in end1.split(",")])
        end2 = np.array([int(x) for x in end2.split(",")])

        v = end2 - end1
        length = max(v)

        # Construct list of arrays representing cubes
        blocks = [end1 + i * v / max(length, 1) for i in range(length + 1)]
        return sorted(blocks, key=lambda x: (x[2], x[1], x[0]))

    def __lt__(self, other):
        # Use z-coordinate to provide a partial ordering on the blocks
        return min(self.cubes[0][2], self.cubes[-1][2]) < min(
            other.cubes[0][2], other.cubes[-1][2]
        )


class BlockDropper:
    def __init__(self, blocks):
        self.blocks = blocks

        # Allows block to be retrieved
        # by increasing z-coordinate
        heapify(self.blocks)

        # Useful variables, to track the resting places of the drops
        self.lowest_free_space = defaultdict(lambda: 1)
        self.xy_entries = defaultdict(lambda: {})
        self.nonzero_drops = 0
        self.is_dropped = False

        # Colours for visualization
        self.colors = list(mcolors.TABLEAU_COLORS.keys())

    def drop_blocks(self):
        assert not self.is_dropped
        dropped_blocks = []
        self.dropped = {b.id: False for b in self.blocks}

        while not all(self.dropped.values()):
            # Retrieve next block
            b = heappop(self.blocks)
            self.dropped[b.id] = True

            # Find distance to lowest unoccupied space in z-direction
            drop_distance = min(
                [
                    cube[2] - self.lowest_free_space[(cube[0], cube[1])]
                    for cube in b.cubes
                ]
            )

            # Keep track of number of blocks dropped
            if drop_distance > 0:
                self.nonzero_drops = self.nonzero_drops + 1

            # Update the cube coordinates after drop
            b.cubes = [
                np.array([cube[0], cube[1], cube[2] - drop_distance])
                for cube in b.cubes
            ]

            # Keep track of which blocks occupy spaces in each x-y column
            for cube in b.cubes:
                self.xy_entries[(cube[0], cube[1])][cube[2]] = b

            # Update block z information
            b.minz = b.minz - drop_distance
            b.maxz = b.maxz - drop_distance
            b.set_id()

            # Update lowest_free_space, as block now occupies current one
            for cube in b.cubes:
                self.lowest_free_space[(cube[0], cube[1])] = (
                    max(self.lowest_free_space[(cube[0], cube[1])], cube[2]) + 1
                )

            dropped_blocks.append(b)

        self.is_dropped = True
        self.blocks = dropped_blocks

    def visualize_blocks(self, **fig_args):
        # Create axes
        minx = np.min([b.minx for b in self.blocks])
        maxx = np.max([b.maxx for b in self.blocks])
        miny = np.min([b.miny for b in self.blocks])
        maxy = np.max([b.maxy for b in self.blocks])
        minz = np.min([b.minz for b in self.blocks])
        maxz = np.max([b.maxz for b in self.blocks])

        axes = [int(maxx) + 1, int(maxy) + 1, int(maxz) + 1]

        # Create data
        data = np.zeros(axes)
        colors = np.empty(data.shape, dtype=object)
        for i, block in enumerate(self.blocks):
            for cube in block.cubes:
                coords = [int(cube[0]), int(cube[1]), int(cube[2]) - 1]
                data[*coords] = 1
                colors[*coords] = self.colors[i % len(self.colors)]

        # Plot figure
        fig = plt.figure(**fig_args)
        ax = fig.add_subplot(111, projection="3d")

        ax.voxels(data, facecolors=colors, alpha=0.8)
        ax.set_box_aspect((maxx - minx, maxy - miny, maxz - 1))
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.set_zticklabels([])
        return fig, ax


def compute_support(dropper):
    # The two dicts to construct
    support = {block: set() for block in dropper.blocks}
    atop = {block: set() for block in dropper.blocks}

    xy = dropper.xy_entries

    # For each (x,y) position, find blocks which
    # lie in neighbouring z slots
    for x, y in xy.keys():
        for z, block in xy[(x, y)].items():
            if z + 1 in xy[(x, y)]:
                support[block].add(xy[(x, y)][z + 1])
                atop[xy[(x, y)][z + 1]].add(block)

    # Remove blocks which are in their own support/atop entry
    # (happens when block is oriented vertically)
    for k in support:
        while k in support[k]:
            support[k].remove(k)

    for k in atop:
        while k in atop[k]:
            atop[k].remove(k)

    return support, atop


def compute_n_falling(block, support, atop):
    # Falling flags for all blocks
    is_falling = {b: False for b in support}

    # Block under consideration is
    # considered to be falling
    is_falling[block] = True

    # Add block to queue
    queue = deque(support[block])
    while queue:
        # Consider next block n queue
        b = queue.popleft()

        if all([is_falling[a] for a in atop[b]]):
            # Update flag
            is_falling[b] = True

            # Add all dependents to queue
            for c in support[b]:
                queue.append(c)

    # Return number of falling blocks
    # (minus first block)
    return sum(is_falling.values()) - 1
