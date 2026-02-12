import matplotlib.pyplot as plt
import pandas as pd
from chord_adapter import ChordAdapter
from pastry_adapter import PastryAdapter
from experiments import run_experiment_insert, run_experiment_lookup

# Load dataset
df = pd.read_excel("data/data_movies_clean.csv")
df = df.dropna(subset=["title"])

node_sizes = [50, 100, 200]

chord_results = []
pastry_results = []

for n in node_sizes:
    print(f"\nRunning for {n} nodes...")

    # Chord 
    chord = ChordAdapter()
    chord.build(nodes=n)
    run_experiment_insert(chord, df, limit=500)
    avg_hops, _ = run_experiment_lookup(chord, df["title"].tolist()[:200])
    chord_results.append(avg_hops)

    # Pastry 
    pastry = PastryAdapter()
    pastry.build(nodes=n)
    run_experiment_insert(pastry, df, limit=500)
    avg_hops, _ = run_experiment_lookup(pastry, df["title"].tolist()[:200])
    pastry_results.append(avg_hops)

# Plot
plt.figure()
plt.plot(node_sizes, chord_results, marker='o', label="Chord")
plt.plot(node_sizes, pastry_results, marker='o', label="Pastry")

plt.xlabel("Number of Nodes")
plt.ylabel("Average Lookup Hops")
plt.title("Scalability: Avg Hops vs Number of Nodes")
plt.legend()
plt.grid(True)
plt.show()
