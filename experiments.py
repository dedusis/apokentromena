import time
import random
import pandas as pd
from interfaces import DHTInterface

def run_experiment_insert(dht: DHTInterface, df, limit=1000):
    hops_list = []
    start_time = time.time()
    
    sample = df.head(limit)
    
    for _, row in sample.iterrows():
        key = row['title']
        val = row.to_dict()
        dht.insert(key, val)
        hops_list.append(dht.get_hops())

    duration = time.time() - start_time
    avg_hops = sum(hops_list) / len(hops_list) if hops_list else 0
    return avg_hops, duration

def run_experiment_lookup(dht: DHTInterface, keys_to_find):
    hops_list = []
    start_time = time.time()
    
    for key in keys_to_find:
        dht.lookup(key)
        hops_list.append(dht.get_hops())
        
    duration = time.time() - start_time
    avg_hops = sum(hops_list) / len(hops_list) if hops_list else 0
    return avg_hops, duration

def run_experiment_delete(dht: DHTInterface, keys_to_delete):
    hops_list = []
    start_time = time.time()

    for key in keys_to_delete:
        dht.delete(key)
        hops_list.append(dht.get_hops())

    duration = time.time() - start_time
    avg_hops = sum(hops_list) / len(hops_list) if hops_list else 0
    return avg_hops, duration

def run_experiment_join_impact(dht: DHTInterface, lookup_keys, joins=10):
    # baseline lookup
    base_hops, _ = run_experiment_lookup(dht, lookup_keys)

    start_time = time.time()
    for i in range(joins):
        dht.node_join(f"join_{i}")
    join_time = time.time() - start_time

    after_hops, after_time = run_experiment_lookup(dht, lookup_keys)

    return after_hops, join_time



def run_experiment_leave_impact(dht: DHTInterface, lookup_keys, joined_names):
    base_hops, _ = run_experiment_lookup(dht, lookup_keys)

    start_time = time.time()
    for name in joined_names:
        dht.node_leave(name)
    leave_time = time.time() - start_time

    after_hops, after_time = run_experiment_lookup(dht, lookup_keys)

    return after_hops, leave_time
