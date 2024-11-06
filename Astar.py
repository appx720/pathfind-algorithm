import numpy as np
import heapq
from visualize import show_matrix


__all__ = ['a_star']


def get_heuristic(a, b):
    # calculate manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(grid: np.ndarray, start: tuple, end: tuple):
    """
    A* algorithm to find shortest path in a grid

    :param grid:
        a 2D grid where 0 is an open space and 1 is an obstacle
    :param start:
        the starting point
    :param end:
        the ending point

    :return list:
        a list of nodes in the shortest path
    """
    
    previous_node = {node : None for node in np.ndindex(grid.shape)}
    
    # store cost of current state
    g_score = {node: float('inf') for node in np.ndindex(grid.shape)}
    g_score[start] = 0

    # store expected cost to destination(g_score + heuristic)
    f_score = {node: float('inf') for node in np.ndindex(grid.shape)}
    f_score[start] = get_heuristic(start, end)

    # priority queue
    queue = [(0, start)]

    while queue:
        current_cost, current = heapq.heappop(queue)

        # search neighbor
        for neighbor in get_neighbors(current, grid):
            expected_g_score = g_score[current] + 1

            if expected_g_score < g_score[neighbor]:
                previous_node[neighbor] = current
                g_score[neighbor] = expected_g_score

                # core of A* algorithm
                f_score[neighbor] = g_score[neighbor] + get_heuristic(neighbor, end)
                
                if (f_score[neighbor], neighbor) not in queue:
                    heapq.heappush(queue, (f_score[neighbor], neighbor))

    return search_path(previous_node, start, end)


def get_neighbors(node, grid):
    """
    find all neighbors of a given node
    """
    neighbors = []

    # left, right, down, up
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        neighbor = (node[0] + dx, node[1] + dy)

        if 0 <= neighbor[0] < grid.shape[0] and 0 <= neighbor[1] < grid.shape[1]:
            if grid[neighbor] != 1:
                neighbors.append(neighbor)
    
    return neighbors


def search_path(previous_node, start, end):
    """
    Reconstructs the shortest path from the start node to the end node.

    :param previous_node: 
        A dictionary mapping each node to its predecessor along the shortest path.
    :param start: 
        The starting node of the path.
    :param end: 
        The ending node of the path.

    :return: 
        A list of nodes representing the reconstructed path from start to end.
    """
    path = [end]

    while path[-1] != start:
        path.append(previous_node[path[-1]])
    
    path.reverse()
    return path


# set matrix ('1' means obstacle of the path)
grid = np.array([
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 1],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0]
])

path = a_star(grid, (0, 0), (4, 4))

show_matrix(grid, path)