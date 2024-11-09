import sys
import os
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import *
from src.utils import *
from src.mobility import generate_random_movement
from src.handoff import handle_handoff
from src.visualization import animate_network
from src.prb_allocation import allocate_prbs, adjust_prb_allocation
from src.qos_analysis import calculate_throughput, calculate_jitter, calculate_delay, analyze_qos
from config.settings import TOTAL_PRBS_PER_BS
import matplotlib.pyplot as plt

def generate_non_overlapping_base_stations(num_base_stations, grid_size, min_distance, max_retries=1000):
    base_stations = []
    retries = 0
    while len(base_stations) < num_base_stations and retries < max_retries:
        pos = np.random.randint(0, grid_size[0], size=(2,))
        if all(np.linalg.norm(pos - bs) >= min_distance for bs in base_stations):
            base_stations.append(pos)
        retries += 1
    if len(base_stations) < num_base_stations:
        print("Warning: Could not place all base stations without overlap.")
    return np.array(base_stations)
def main():
 
    throughput_data = []
    jitter_data = []
    delay_data = []

    base_stations = generate_non_overlapping_base_stations(NUM_BASE_STATIONS, GRID_SIZE, min_distance=2)
    ue_movements = generate_random_movement(NUM_UES, GRID_SIZE, TIME_STEPS)
    prb_table_static = [{i: TOTAL_PRBS_PER_BS // NUM_UES for i in range(NUM_UES)} for _ in range(NUM_BASE_STATIONS)]
    prb_table_dynamic = [{i: 0 for i in range(NUM_UES)} for _ in range(NUM_BASE_STATIONS)]

    connections_history = []

    fig1, ax1 = plt.subplots(figsize=(8, 6))
    fig2, (ax2, ax3, ax4) = plt.subplots(3, 1, figsize=(10, 12))

    animation = animate_network(base_stations, ue_movements, connections_history, TIME_STEPS, ax1)

    for t in range(TIME_STEPS):
        ue_positions = ue_movements[t]
        rsrp_values = np.zeros((NUM_UES, NUM_BASE_STATIONS))

        for i, ue_pos in enumerate(ue_positions):
            for j, bs_pos in enumerate(base_stations):
                distance = np.linalg.norm(ue_pos - bs_pos)
                path_loss = calculate_path_loss(distance)
                rsrp_values[i][j] = calculate_rsrp(TX_POWER, path_loss)

        connections = handle_handoff(ue_positions, base_stations, rsrp_values)
        connections_history.append(connections)

        for i, ue_pos in enumerate(ue_positions):
            current_bs = connections[i]
            sinr = calculate_sinr(rsrp_values[i][current_bs], 0, THERMAL_NOISE + NOISE_FIGURE)

            prbs_static = prb_table_static[current_bs][i]
            throughput_static = calculate_throughput(sinr, prbs_static, BANDWIDTH)
            delay_static = calculate_delay(sinr)
            jitter_static = calculate_jitter([delay_static])

            previous_bs = connections_history[-2][i] if t > 0 else current_bs
            prb_table_dynamic = allocate_prbs(i, previous_bs, current_bs, sinr, prb_table_dynamic, BANDWIDTH)
            prbs_dynamic = prb_table_dynamic[current_bs].get(i, 0)
            throughput_dynamic = calculate_throughput(sinr, prbs_dynamic, BANDWIDTH)
            delay_dynamic = calculate_delay(sinr)
            jitter_dynamic = calculate_jitter([delay_dynamic])


            throughput_data.extend([[t, "Static", throughput_static], [t, "Dynamic", throughput_dynamic]])
            jitter_data.extend([[t, "Static", jitter_static], [t, "Dynamic", jitter_dynamic]])
            delay_data.extend([[t, "Static", delay_static], [t, "Dynamic", delay_dynamic]])

      
        animation._draw_frame(t)
        fig1.canvas.draw_idle()

       
        ax2.clear()
        ax3.clear()
        ax4.clear()


        ax2.plot([d[0] for d in throughput_data if d[1] == "Static"], [d[2] for d in throughput_data if d[1] == "Static"], label="Static", color="blue")
        ax2.plot([d[0] for d in throughput_data if d[1] == "Dynamic"], [d[2] for d in throughput_data if d[1] == "Dynamic"], label="Dynamic", color="red")
        ax2.set_title("Throughput Comparison")
        ax2.set_ylabel("Throughput (Mbps)")
        ax2.legend()


        ax3.plot([d[0] for d in jitter_data if d[1] == "Static"], [d[2] for d in jitter_data if d[1] == "Static"], label="Static", color="blue")
        ax3.plot([d[0] for d in jitter_data if d[1] == "Dynamic"], [d[2] for d in jitter_data if d[1] == "Dynamic"], label="Dynamic", color="red")
        ax3.set_title("Jitter Comparison")
        ax3.set_ylabel("Jitter (Variance)")
        ax3.legend()

      
        ax4.plot([d[0] for d in delay_data if d[1] == "Static"], [d[2] for d in delay_data if d[1] == "Static"], label="Static", color="blue")
        ax4.plot([d[0] for d in delay_data if d[1] == "Dynamic"], [d[2] for d in delay_data if d[1] == "Dynamic"], label="Dynamic", color="red")
        ax4.set_title("Delay Comparison")
        ax4.set_ylabel("Delay (ms)")
        ax4.legend()

        fig2.canvas.draw_idle()
        plt.pause(0.01)

    plt.show()

if __name__ == "__main__":
    main()