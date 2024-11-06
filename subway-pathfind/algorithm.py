"""dijkstra algorithm and create graph for visualization"""
import heapq


__all__ = ['get_path']


def get_path(nodes: dict, start: str, end: str):
    """
    Dijkstra's algorithm to find the shortest path in subway nodes

    :param nodes: 
        list containing the subway nodes
    :param start: 
        the starting point (station name)
    :param end: 
        the ending point (station name)

    :return list:
        a list of station names in the shortest path
    """

    station_map = {name: nodes[name] for name in nodes.keys()}

    previous_node = {station: None for station in station_map.keys()}
    cost = {station: float('inf') for station in station_map.keys()}
    cost[start] = 0

    # priority queue
    queue = [(0, start)]

    while queue:
        current_cost, current = heapq.heappop(queue)

        if current == end:
            return search_path(previous_node, start, end)

        # skip if distance is greater than last distance
        if current_cost > cost[current]:
            continue


        # find neighbor
        for neighbor in (station_map[current].get_all()[2:][0]):
            neighbor_name = neighbor[0].get_all()[0]

            _cost = neighbor[1]
            expected_cost = int(cost[current] + _cost)


            if expected_cost < cost[neighbor_name]:
                previous_node[neighbor_name] = current
                cost[neighbor_name] = expected_cost
                heapq.heappush(queue, (cost[neighbor_name], neighbor_name))

    

    return [] # path is not exist


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
    path = []
    current = end

    while current is not None:
        path.append(current)
        current = previous_node[current]
    
    path.reverse()
    return path
