import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_throughput(sinr, prbs, bandwidth):
  
    capacity_per_prb = bandwidth * np.log2(1 + 10 ** (sinr / 10))
    return prbs * capacity_per_prb

def calculate_jitter(delays):
   
    return np.var(delays)

def calculate_delay(sinr):
   
    return 1 / (1 + 10 ** (sinr / 10))

def analyze_qos(throughput_data, jitter_data, delay_data):
   
    df_throughput = pd.DataFrame(throughput_data, columns=["Time", "Scenario", "Throughput"])
    df_jitter = pd.DataFrame(jitter_data, columns=["Time", "Scenario", "Jitter"])
    df_delay = pd.DataFrame(delay_data, columns=["Time", "Scenario", "Delay"])

    plt.figure(figsize=(12, 8))

    plt.subplot(3, 1, 1)
    sns.lineplot(data=df_throughput, x="Time", y="Throughput", hue="Scenario")
    plt.title("Throughput Comparison (Static vs. Dynamic PRB Allocation)")
    plt.ylabel("Throughput (Mbps)")
    plt.xlabel("Time Step")

    plt.subplot(3, 1, 2)
    sns.lineplot(data=df_jitter, x="Time", y="Jitter", hue="Scenario")
    plt.title("Jitter Comparison (Static vs. Dynamic PRB Allocation)")
    plt.ylabel("Jitter (Variance)")
    plt.xlabel("Time Step")

    plt.subplot(3, 1, 3)
    sns.lineplot(data=df_delay, x="Time", y="Delay", hue="Scenario")
    plt.title("Delay Comparison (Static vs. Dynamic PRB Allocation)")
    plt.ylabel("Delay (ms)")
    plt.xlabel("Time Step")

    plt.tight_layout()
    plt.show()
