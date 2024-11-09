import numpy as np

def handle_handoff(ue_positions, base_stations, rsrp_values):
    handoffs = []

    for i, ue_pos in enumerate(ue_positions):
        best_bs = None
        best_rsrp = -np.inf
        for j, bs_pos in enumerate(base_stations):
            rsrp = rsrp_values[i][j]
            if rsrp > best_rsrp:
                best_rsrp = rsrp
                best_bs = j
        handoffs.append(best_bs)

    return handoffs
