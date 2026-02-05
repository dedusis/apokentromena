import pandas as pd
from pastry_adapter import PastryAdapter
from chord_adapter import ChordAdapter  
import unicodedata

def norm_key(s: str) -> str:
    s = "" if s is None else str(s)
    s = unicodedata.normalize("NFKC", s)   
    s = " ".join(s.strip().split())        
    return s

from experiments import (
    run_experiment_insert,
    run_experiment_lookup,
    run_experiment_delete,
    run_experiment_join_impact,
    run_experiment_leave_impact,
)
from concurrency import run_concurrent

def main():
    print("Loading Dataset...")
    df = pd.read_csv("data_movies_clean.csv")
    df = df.dropna(subset=['title'])
    
    choice = input("Choose DHT (chord / pastry): ").strip().lower()
    
    if choice == "pastry":
        dht = PastryAdapter()
    elif choice == "chord":
        dht = ChordAdapter()
    else:
        print("Invalid choice")
        return

    print(f"Building {choice} network with 100 nodes...")
    dht.build(nodes=100)
    

    insert_hops, insert_time = run_experiment_insert(dht, df, limit=1000)
    print(f"INSERT | avg hops={insert_hops:.3f} | time={insert_time:.3f}s")

    keys = [norm_key(x) for x in df["title"].tolist()]
    lookup_keys = keys[:200]
    delete_keys = keys[:200]

    lookup_hops, lookup_time = run_experiment_lookup(dht, lookup_keys)
    print(f"LOOKUP | avg hops={lookup_hops:.3f} | time={lookup_time:.3f}s")
    
    print("\n=== Concurrent Popularity Lookup ===")
    K = 30

    titles_to_check = [norm_key(x) for x in df["title"].head(K).tolist()]
    results = run_concurrent(dht, titles_to_check)

    for i, (title, res) in enumerate(zip(titles_to_check, results), start=1):
        if isinstance(res, dict):
         print(f"{i:02d}. {title:<60} | popularity: {res.get('popularity')}")
        else:
            print(f"{i:02d}. {title:<60} | NOT FOUND | repr={repr(title)}")

    delete_hops, delete_time = run_experiment_delete(dht, delete_keys)
    print(f"DELETE | avg hops={delete_hops:.3f} | time={delete_time:.3f}s")

   
    join_hops, join_time = run_experiment_join_impact(dht, lookup_keys, joins=10)
    print(f"JOIN   | avg hops={join_hops:.3f} | time={join_time:.3f}s")

    joined_names = [f"join_{i}" for i in range(10)]
    leave_hops, leave_time = run_experiment_leave_impact(dht, lookup_keys, joined_names)
    print(f"LEAVE  | avg hops={leave_hops:.3f} | time={leave_time:.3f}s")


    
if __name__ == "__main__":
    main()