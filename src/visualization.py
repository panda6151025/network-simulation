import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.animation import FuncAnimation
from config.settings import GRID_SIZE

UE_COLORS = ['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'magenta', 'yellow', 'lime', 'pink']

COVERAGE_RADIUS = 2.5
LINE_STYLE = 'dotted'

def animate_network(base_stations, ue_movements, connections_history, time_steps, ax):
    G = nx.Graph()

    base_station_labels = {f"BS{i}": chr(65 + i) for i in range(len(base_stations))}

    interpolation_steps = 10
    total_frames = min(time_steps * interpolation_steps, 100)

    def interpolate_positions(start_pos, end_pos, factor):
        return start_pos + (end_pos - start_pos) * factor

    def update(frame):
        if frame >= total_frames: 
            return

        ax.clear()
        G.clear()

        time_step = frame // interpolation_steps
        interp_factor = (frame % interpolation_steps) / interpolation_steps

        for i, bs in enumerate(base_stations):
            circle = plt.Circle((bs[0], bs[1]), COVERAGE_RADIUS, color='gray', linestyle='dotted', linewidth=1.5, fill=False, alpha=0.6)
            ax.add_patch(circle)
            G.add_node(f"BS{i}", pos=(bs[0], bs[1]), color='black', size=300)

        if time_step < time_steps - 1:
            ue_positions_start = ue_movements[time_step]
            ue_positions_end = ue_movements[time_step + 1]
            connections = connections_history[time_step]

            for i, ue_pos_start in enumerate(ue_positions_start):
                ue_pos_end = ue_positions_end[i]
                ue_pos = interpolate_positions(np.array(ue_pos_start), np.array(ue_pos_end), interp_factor)

                G.add_node(f"UE{i}", pos=(ue_pos[0], ue_pos[1]), color=UE_COLORS[i % len(UE_COLORS)], size=100)
                G.nodes[f"UE{i}"]['label'] = str(i)
                bs_index = connections[i]
                G.add_edge(f"UE{i}", f"BS{bs_index}")

        pos = nx.get_node_attributes(G, 'pos')
        colors = [G.nodes[node]['color'] for node in G.nodes]
        sizes = [G.nodes[node]['size'] for node in G.nodes]
        ue_labels = {node: G.nodes[node]['label'] for node in G.nodes if node.startswith('UE')}

        nx.draw(G, pos, node_color=colors, node_size=sizes, with_labels=False, ax=ax)
        nx.draw_networkx_labels(G, pos, labels=base_station_labels, font_color='white', ax=ax)
        nx.draw_networkx_labels(G, pos, labels=ue_labels, font_color='black', ax=ax)

        ax.set_title(f"Network Visualization at Interpolated Frame {frame}")
        ax.set_xlim(-1, GRID_SIZE[0] + 1)
        ax.set_ylim(-1, GRID_SIZE[1] + 1)

    anim = FuncAnimation(ax.figure, update, frames=total_frames, interval=200, repeat=False)
    return anim