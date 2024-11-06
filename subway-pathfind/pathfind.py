import algorithm
import pandas as pd
import networkx as nx



def get_connect():
    previous_num = 0
    previous_station = None
    connections = []


    for i in range(len(distance_dat_f)):
        row = distance_dat_f.iloc[i]

        if row["호선"] != previous_num:
            previous_num = row["호선"]
            previous_station = row["역명"]
            
        else:
            connections.append((previous_station, row["역명"]))
            previous_station = row["역명"]

    return connections

def get_distance(start, end):
    if (start, end) in distances.keys():
        return distances[(start, end)]
    
    elif (end, start) in distances.keys():
        return distances[(end, start)]
    
    return -1 #error



distance_dat_f = pd.read_csv("subway-pathfind/data.csv", encoding="CP949")
distance_raw = distance_dat_f["소요시간"]
distance = []

for i in distance_raw:
    # remove start station
    if i == "0:00":
        continue

    # hour to min
    distance.append(int(i.split(":")[0])*60 + int(i.split(":")[1]))

connect = get_connect()

distances = {c: d for c, d in zip(connect, distance)}



class Station:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.connections = []

    def add_connection(self, station, distance):
        self.connections.append((station, distance))

    def get_all(self):
        return [self.name, self.color, self.connections]



def find_path(start, end):
    G = nx.read_gml("subway-pathfind/graph.gml")

    nodes = {}

    for node in G.nodes(data=True):
        nodes[node[0]] = Station(node[0], node[1]) # name, color


    for edge in G.edges(data=True):
        d = get_distance(edge[0], edge[1])

        if not d:
            return False # error

        nodes[edge[0]].add_connection(nodes[edge[1]], d)
        nodes[edge[1]].add_connection(nodes[edge[0]], d)


    return algorithm.get_path(nodes, start, end)



print(find_path('서울역', '강남구청'))