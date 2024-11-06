import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def show_graph(graph, path: None):
    """
    visualize the graph and path(optional)

    :param graph:
        A dictionary representing the graph.
    
    :param path optional:
        a list of nodes in the shortest path
    """
    G = nx.Graph()
    G.add_nodes_from(graph.keys())

    edge_list = []

    for node in graph:
        for neighbor, weight in graph[node].items():
            edge_list += ((node, neighbor, {'weight': weight}),)

    G.add_edges_from(edge_list)

    # positioning automatically
    pos = nx.spring_layout(G)

    # get edges' weight
    edge_labels = nx.get_edge_attributes(G, 'weight')

    # process special cases
    special_case = [path[0], path[-1]] # start, end
    node_colors = ['yellow' if node in special_case else 'lightblue' for node in G.nodes()]
    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]

    # draw
    nx.draw(G, pos, with_labels=True, node_size=700, node_color=node_colors, font_size=10, font_weight='bold')
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # show
    plt.title("Dijkstra Visualization")
    plt.show()


def show_matrix(grid, path):
    """
    Visualizes a 2D grid matrix and an optional path on it.

    :param grid: 
        A 2D numpy array representing the grid, where each element can be an obstacle or free space.
    :param path: 
        A list of tuples representing the path through the grid, where each tuple is a (row, column) coordinate.
        The path is visualized with blue dots and highlighted with green and red dots for the start and end points, respectively.
    """

    plt.figure(figsize = (6, 6))
    plt.imshow(grid, cmap='Greys', origin='upper')

    # Add path to the grid
    if path:
        for node in path:
            plt.scatter(node[1], node[0], color='blue')

        # Add start and end points
        plt.scatter(path[0][1], path[0][0], color='green', s=200, label='Start')
        plt.scatter(path[-1][1], path[-1][0], color='red', s=200, label='End')


    plt.title("A* Visualization")
    plt.xlabel("Columns")
    plt.ylabel("Rows")

    plt.xticks(np.arange(grid.shape[1]))
    plt.yticks(np.arange(grid.shape[0]))

    plt.gca().invert_yaxis()
    plt.legend()
    plt.grid(True)
    plt.show()