import random
from matplotlib import animation
import numpy as np
import osmnx as ox
import pandas as pd
from numpy import linalg as LA
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.stats import gaussian_kde


bbox = (52.537448, 52.528285, 13.427782, 13.449653)
area = ox.graph_from_bbox(bbox=bbox, network_type="drive", simplify=True)
buildings = ox.features_from_bbox(bbox=bbox, tags={"building": True})
roads = ox.features_from_bbox(
    bbox=bbox, tags={"highway": ["residential", "primary"]})
paths = ox.features_from_bbox(
    bbox=bbox, tags={"highway": ["pedestrian", "footway",]})
parks = ox.features_from_bbox(
    bbox=bbox, tags={"leisure": "park", "landuse": "grass"})


adj = dict()
for i in area.adjacency():
    adj[i[0]] = set(i[1].keys())

# make adj symmetric
for i in adj:
    for j in adj[i]:
        adj[j].add(i)

node_df, edge_df = ox.graph_to_gdfs(area)

# select two random nodes and find shortes path between them
# start_node = random.choice(list(adj.keys()))
# end_node = random.choice(list(adj.keys()))
# while end_node == start_node:
#     end_node = random.choice(list(adj.keys()))

start_node = 9629731359
end_node = 29268019

print(f"Start node: {start_node}, End node: {end_node}")

# plot the path
fig, ax = ox.plot_graph(area, show=False, close=False, bgcolor="none")

path = ox.shortest_path(area, start_node, end_node)

buildings.plot(ax=ax, facecolor="silver", alpha=0.7)

# plot the path
path_plot = ox.plot.plot_graph_route(area, path, ax=ax, route_linewidth=6,
                                     route_alpha=0.8, orig_dest_size=100, orig_dest_node_color="r")


plt.show()
