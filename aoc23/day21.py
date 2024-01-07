from collections import namedtuple
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt

Plot = namedtuple('Plot', ['row', 'col'])

class PlotCalculator:

    def __init__(self, grid):
        self.grid = grid
        self.n_rows = len(grid)
        self.n_cols = len(grid[0])
    
    def find_starting_plot(self):
        for i, line in enumerate(self.grid):
            if 'S' in line:
                return (i, line.index('S'))

    def neighbouring_plots(self, plot):
        neighbour_plots = []
        
        # Step in one of the cardinal directions
        new_plots = [Plot(row=plot.row - 1, col=plot.col),
                     Plot(row=plot.row + 1, col=plot.col),
                     Plot(row=plot.row, col=plot.col - 1),
                     Plot(row=plot.row, col=plot.col + 1)]
        
        # Only accept steps inside the grid
        # and onto garden plots (not rocks)
        for new_plot in new_plots:
            if 0 <= new_plot.row < self.n_rows and 0 <= new_plot.col < self.n_cols:
                if self.grid[new_plot.row][new_plot.col] != '#':
                    neighbour_plots.append(new_plot)
                    
        return neighbour_plots

    
    def compute_visited_plots(self, n_steps):
        # Identify starting tile
        start_row, start_col = self.find_starting_plot()
        
        # Initialize odd/even parity visited tile dicts
        cumulative_plots = 1
        visited_plots = {0: {Plot(start_row, start_col): 1},
                         1: {}}
        outer_plots = {Plot(start_row, start_col): 1}
        
        # Take steps
        for i in range(1, n_steps+1):
            new_plots = {}
            step_parity = i % 2
            
            # Loop over all boundary plots
            for plot in outer_plots:
                
                # Find new neighbours
                neighbours = self.neighbouring_plots(plot)
                
                for neighbour in neighbours:
                    if neighbour not in visited_plots[step_parity]:
                        # Keep track of newly visited plots
                        new_plots[neighbour] = 1
                        visited_plots[step_parity][neighbour] = 1
            
            # Only need to look at boundary plots in next loop
            outer_plots = new_plots
        
        # Return plots with relevant step parity
        final_step_parity = n_steps % 2
        return visited_plots[final_step_parity]

    
    def visualise_visit(self, n_steps):
        visited = self.compute_visited_plots(n_steps)
        vis_grid = deepcopy(self.grid)
        
        # Replace all visited plots with 'O'
        for plot in visited.keys():
            old_row = vis_grid[plot.row]
            vis_grid[plot.row] = old_row[:plot.col] + 'O' + old_row[plot.col+1:]
            
        return vis_grid
    
class InfinitePlotCalculator(PlotCalculator):
    
    def neighbouring_plots(self, plot):
        neighbour_plots = []
        
        # Step in one of the cardinal directions
        new_plots = [Plot(row=plot.row - 1, col=plot.col),
                     Plot(row=plot.row + 1, col=plot.col),
                     Plot(row=plot.row, col=plot.col - 1),
                     Plot(row=plot.row, col=plot.col + 1)]
        
        # Only accept steps onto garden plots (not rocks)
        for new_plot in new_plots:
            row = new_plot.row % self.n_rows
            col = new_plot.col % self.n_cols
            if self.grid[row][col] != '#':
                neighbour_plots.append(new_plot)
                    
        return neighbour_plots
    
    def visualise_visit(self, n_steps, **fig_args):
        assert self.n_rows == self.n_cols
        visited = self.compute_visited_plots(n_steps)

        n = max(0, (n_steps + self.n_rows//2) // self.n_rows)
        grid = np.tile([[int(char.replace('.', '0').replace('#', '1').replace('S', '0')) for char in row] for row in self.grid], 
                         (2*n+1, 2*n+1))

        for plot in visited:
            grid[plot.row + n*self.n_rows, plot.col + n*self.n_cols] = 2

        fig, ax = plt.subplots(**fig_args)
        ax.matshow(grid)
        ax.set_title(f'Step {n_steps}')
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        
        return fig, ax