# Import everything needed
import io
import pickle
import matplotlib.pyplot as plt
import osmnx as ox
import os
from data import base_street_widths, colors, underground_lines

log = None

bbox = (51.7189, 51.3452, 0.2506, -0.5328)
figsize = (16, 9)


def plot_map_bg():
    fig, ax = plt.subplots(figsize=figsize)

    def plot_feature(tag, value, color):
        log.info(
            f"[PLOT] Drawing {tag if isinstance(value, list) else value} features")
        G = ox.features_from_bbox(bbox=bbox, tags={tag: value})
        ox.plot_footprints(G, ax=ax, show=False, close=False,
                           bgcolor=colors["background"], color=colors[color], save=False, figsize=figsize)

    plot_feature("natural", "water", 'water')
    plot_feature("leisure", ["pitch", "park", "playground"], 'parks')
    plot_feature("natural", ["tree", "wood", "grassland",
                 "tree_row", "scrub", "peak"], 'parks')
    plot_feature("landuse", ["meadow", "forest", "orchard", "farmland",
                 "vineyard", "farmyard", "recreation_ground", "allotments"], 'parks')

    return fig


def plot_map_snapshot(bg, zoom):
    pickle_file = io.BytesIO()
    pickle.dump(bg, pickle_file)
    pickle_file.seek(0)
    plt.close(bg)
    fig = pickle.load(pickle_file)
    ax = fig.get_axes()[0]

    street_widths = {key: (width / 100) / zoom for key,
                     width in base_street_widths.items()}

    log.info(f"[PLOT] Drawing railways")
    G = ox.graph_from_bbox(bbox=bbox, custom_filter='["railway"~"rail"]')
    ox.plot_graph(G, ax=ax, node_alpha=0, show=False,
                  close=False, edge_color=colors["railways"], edge_linewidth=1, figsize=figsize)

    log.info(f"[PLOT] Drawing streets")
    G = ox.graph_from_bbox(
        bbox=bbox, custom_filter='["highway"~"motorway|trunk|primary"]')
    ox.plot_figure_ground(G, ax=ax, node_alpha=0, show=False,
                          close=False, street_widths=street_widths, color=colors["highways"], dpi=300, figsize=figsize)
    
    for line in underground_lines:
        log.info(f"[PLOT] Drawing {line} line")
        G = ox.graph_from_bbox(
            bbox=bbox, custom_filter=f'["railway"~"subway"]["name"~"{line}"]')
        ox.plot_graph(G, ax=ax, node_alpha=0, show=False,
                      close=False, edge_color=underground_lines[line], edge_linewidth=1, figsize=figsize)

    ax.set_facecolor(colors["background"])
    return fig


def save_pickle(obj, filename):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)


def load_pickle(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def create_map_snapshot(debug=False):
    if debug:
        ox.config(log_console=True, use_cache=True)
    if os.path.exists('fig.pickle'):
        return load_pickle('fig.pickle')
    background = plot_map_bg()
    fig = plot_map_snapshot(bg=background, zoom=0.02)
    save_pickle(fig, 'fig.pickle')
    return fig