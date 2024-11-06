import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm



def create_graph() -> None:
    G = nx.Graph()

    # color map
    color = ["blue", "green", "orange", "skyblue", "purple", "brown", "#6F4C3E", "pink"]

    previous_node = None
    previous_id = None

    for i in range(len(data)):
        row = data.iloc[i]
        name = row["역명"]
        c = color[int(row["호선"]) - 1]

        if previous_id != row["호선"]:
            previous_id = row["호선"]
            previous_node = None
        
        
        if row["환승"]:
            # add transfer
            if name not in G:
                G.add_node(name, color='red')
            
        else:
            G.add_node(name, color=c)

        if previous_node:
            G.add_edge(previous_node, name, color=c)

        previous_node = name

    # write gml file
    nx.write_gml(G, "subway-pathfind/graph.gml")



def get_pos():
    """
    Load position data from csv file and return as a dictionary.

    Returns:
        dict: node name as key, tuple of (latitude, longitude) as value
    """
    position = pd.read_csv("subway-pathfind/pos.csv", encoding="CP949")
    pos = {}

    for index, row in position.iterrows():
        name = row["역명"]
        latitude = row["위도"]
        longitude = row["경도"]
        pos[name] = (latitude, longitude)
    
    return pos


# read csv
data = pd.read_csv('subway-pathfind/data.csv', encoding="CP949")
font_path = "C:/Windows/Fonts/NanumGothic.ttf"
font_prop = fm.FontProperties(fname=font_path)

# it is required at the first
# create_graph()

# read gml file
G = nx.read_gml("subway-pathfind/graph.gml")

pos = get_pos()
edges = G.edges()
colors = [G[u][v]['color'] for u, v in edges]

plt.figure(figsize=(12, 8))


for edge in edges:
    plt.plot(*zip(pos[edge[0]], pos[edge[1]]), color=G[edge[0]][edge[1]]['color'], linewidth=1)


for node in G.nodes():
    # intersection's color is set red
    if G.nodes[node]['color'] == 'red':
        plt.scatter(*pos[node], s=30, facecolors=G.nodes[node]['color'], edgecolor=None)
    
    else:
        plt.scatter(*pos[node], s=30, marker='o', edgecolor=G.nodes[node]['color'], facecolors='none', linewidths=1)

    # add text
    plt.text(pos[node][0], pos[node][1], node, fontsize=7, ha='center', fontproperties=font_prop)


plt.title("Seoul Subway Visualization", fontproperties=font_prop, fontsize=16)
plt.axis('off')
plt.show()