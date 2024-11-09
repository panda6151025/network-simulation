import numpy as np

def calculate_path_loss(distance):
    distance = max(distance, 1e-6)
    return 128.1 + 37.6 * np.log10(distance / 1000)

def calculate_rsrp(tx_power, path_loss):
    return tx_power - path_loss

def calculate_sinr(rsrp, interference, noise):
    return rsrp - (interference + noise)

def calculate_throughput(sinr, bandwidth):
    return bandwidth * np.log2(1 + 10 ** (sinr / 10))
