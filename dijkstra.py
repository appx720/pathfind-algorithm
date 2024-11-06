import heapq
from visualize import show_graph


__all__ = ['dijkstra']


def dijkstra(graph: dict, start: str, end: str=None) -> list:
    """
    Implements Dijkstra's algorithm to find the shortest path in a graph.
    -----
    :param graph:
        A dictionary representing the graph.
        Example:
        {
            'a': {'b': 7, 'c': 3},
            'b': {'a': 7, 'd': 2},
            'c': {'a': 3, 'd': 6, 'e': 4},
            'd': {'b': 2, 'c': 6, 'e': 2},
            'e': {'c': 4, 'd': 2}
        }

    :param start:
        The name of the node to start the search from.

    :param end optional:
        The name of the node to end the search at. 
        If this node does not exist, the search will return the shortest distances to all nodes in the graph.

    :result list:
        A list containing distances and, if applicable, the path from start to end.
    """

    # initialize distances to infinite
    distances = {node: float('inf') for node in graph.keys()}
    
    # start node
    distances[start] = 0
    current_node = start

    # store paths from current node(priority queue)
    queue = [(0, start)]
    previous_node = {node: None for node in graph.keys()}

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        # skip if distance is greater than last distance
        if current_distance > distances[current_node]:
            continue

        # search all neighbors
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_node[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))


    result = [distances]

    if end:
        # track shortest path
        path = explorer_path(previous_node, [start, end])
        result[0] = result[0][end]
        result.append(path)

    return result

    

def explorer_path(previous_node: dict, path: list) -> list:
    """
    Search path based on previous nodes
    ---

    :param previous_node:
        A dictionary containing previous nodes
        ex)
        {
            'a': 'b',
            'c': 'b'
        }
    :param path:
        conist of start and end node
        [start, end]

    :return list:
        a list of shortest node path
    """

    shortest_path = []
    shortest_path.append(path[1]) # first node
    current_path = path[1]

    while current_path != path[0]:
        current_path = previous_node[current_path]
        shortest_path.append(current_path)

    shortest_path.reverse() # sort list
    return shortest_path


# sample
graph = {
            'a': {'b': 1, 'c': 2},
            'b': {'a': 7, 'd': 2},
            'c': {'a': 3, 'd': 4, 'e': 4},
            'd': {'b': 2, 'c': 6, 'e': 2},
            'e': {'c': 4, 'd': 2}
        }

path = dijkstra(graph, 'a', 'e')

# visualize
show_graph(graph, path[1])