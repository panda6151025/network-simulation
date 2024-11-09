import numpy as np


TOTAL_PRBS_PER_BS = 100  
TARGET_THROUGHPUT = 10e6  

def calculate_prb_demand(sinr, target_throughput, bandwidth):
   
    capacity_per_prb = bandwidth * np.log2(1 + 10 ** (sinr / 10))
    prb_demand = np.ceil(target_throughput / capacity_per_prb)
    return int(prb_demand)

def allocate_prbs(ue_index, source_bs, target_bs, sinr, prb_table, bandwidth):

    prb_demand = calculate_prb_demand(sinr, TARGET_THROUGHPUT, bandwidth)
    free_prbs_target = TOTAL_PRBS_PER_BS - sum(prb_table[target_bs].values())

    if prb_demand <= free_prbs_target:
       
        prb_table[target_bs][ue_index] = prb_demand
        
        if ue_index in prb_table[source_bs]:
            del prb_table[source_bs][ue_index]
    else:
       
        fair_prb_allocation = int(free_prbs_target * (sinr / sum([s for s in prb_table[target_bs].values()])))
        prb_table[target_bs][ue_index] = fair_prb_allocation

    return prb_table

def adjust_prb_allocation(ue_index, bs_index, sinr, prb_table, bandwidth):
   
    prb_demand = calculate_prb_demand(sinr, TARGET_THROUGHPUT, bandwidth)

    if prb_demand > prb_table[bs_index].get(ue_index, 0):
        prb_table[bs_index][ue_index] = min(prb_demand, TOTAL_PRBS_PER_BS - sum(prb_table[bs_index].values()))
    elif prb_demand < prb_table[bs_index].get(ue_index, 0):
        prb_table[bs_index][ue_index] = max(1, prb_demand)

    return prb_table
