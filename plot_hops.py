import matplotlib.pyplot as plt

# Operations
operations = ["Insert", "Lookup", "Delete", "Join", "Leave"]

# Avg hops (από τα experiments σου)
chord_hops = [4.323, 3.968, 3.677, 3.935, 3.032]
pastry_hops = [1.516, 1.548, 1.581, 1.516, 1.548]

# Plot
plt.figure()
plt.plot(operations, chord_hops, marker='o', label="Chord")
plt.plot(operations, pastry_hops, marker='o', label="Pastry")

plt.xlabel("Operation")
plt.ylabel("Average Routing Hops")
plt.title("Chord vs Pastry: Average Routing Hops per Operation")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("plots/chord_vs_pastry_hops.png")
plt.show()
