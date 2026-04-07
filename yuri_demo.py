"""
HLX Grid Restoration Demo (Final)

Demonstrates:
- Restoration under shared operational constraints
- Difference between uncoordinated vs optimized restoration
- Measurable improvement in recovery performance

This script is intentionally simplified for demonstration purposes.
"""

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

# =========================
# CONFIG
# =========================
N_NODES = 1000
SEED = 42
OUTAGE_RATE = 0.5
MAX_STEP_LOAD = 120.0
STEPS = 15
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# GRID BUILD
# =========================
def build_grid(n_nodes, seed=None):
    np.random.seed(seed)

    G = nx.erdos_renyi_graph(n_nodes, 0.01)

    for n in G.nodes:
        node_type = np.random.choice(["Gen", "Load"], p=[0.1, 0.9])

        G.nodes[n]["type"] = node_type
        G.nodes[n]["status"] = "OFF"
        G.nodes[n]["load"] = np.random.uniform(1, 5)
        G.nodes[n]["gen"] = np.random.uniform(25, 100) if node_type == "Gen" else 0

    return G

# =========================
# OUTAGE
# =========================
def apply_outage(G, outage_rate):
    gens = [n for n in G.nodes if G.nodes[n]["type"] == "Gen"]
    failed = np.random.choice(gens, int(len(gens) * outage_rate), replace=False)

    for n in failed:
        G.nodes[n]["status"] = "FAULT"
        G.nodes[n]["gen"] = 0

    return failed

# =========================
# BASELINE RESTORATION
# =========================
def baseline_restore(G, steps=STEPS):
    restored_counts = []
    restored = set()

    # Initial generators
    for n in G.nodes:
        if G.nodes[n]["type"] == "Gen" and G.nodes[n]["status"] != "FAULT":
            G.nodes[n]["status"] = "ON"
            restored.add(n)

    for _ in range(steps):
        new_restored = set(restored)
        added_load = 0.0

        candidates = []
        for n in G.nodes:
            if n not in restored and G.nodes[n]["status"] == "OFF":
                if any(nb in restored for nb in G.neighbors(n)):
                    candidates.append(n)

        # Uncoordinated: random order
        np.random.shuffle(candidates)

        for n in candidates:
            load = G.nodes[n]["load"]

            if added_load + load > MAX_STEP_LOAD:
                continue

            if np.random.rand() < 0.5:  # noisy decision process
                new_restored.add(n)
                added_load += load

        restored = new_restored
        restored_counts.append(len(restored))

    return restored_counts

# =========================
# OPTIMIZED RESTORATION
# =========================
def optimized_restore(G, steps=STEPS):
    restored_counts = []
    restored = set()

    # Initial generators
    for n in G.nodes:
        if G.nodes[n]["type"] == "Gen" and G.nodes[n]["status"] != "FAULT":
            G.nodes[n]["status"] = "ON"
            restored.add(n)

    for _ in range(steps):
        new_restored = set(restored)
        added_load = 0.0

        candidates = []
        for n in restored:
            for nb in G.neighbors(n):
                if nb not in restored:
                    candidates.append(nb)

        candidates = list(set(candidates))

        # Coordinated: prioritize smallest load first (efficient capacity use)
        candidates.sort(key=lambda x: G.nodes[x]["load"])

        for n in candidates:
            load = G.nodes[n]["load"]

            if added_load + load > MAX_STEP_LOAD:
                continue

            new_restored.add(n)
            added_load += load

        restored = new_restored
        restored_counts.append(len(restored))

    return restored_counts

# =========================
# MAIN
# =========================
def run_simulation():
    G1 = build_grid(N_NODES, SEED)
    G2 = G1.copy()

    apply_outage(G1, OUTAGE_RATE)
    apply_outage(G2, OUTAGE_RATE)

    baseline = baseline_restore(G1)
    optimized = optimized_restore(G2)

    steps = list(range(len(baseline)))

    # =========================
    # PLOT
    # =========================
    plt.figure(figsize=(12, 6))

    plt.plot(steps, baseline, 'r-o', linewidth=2, label='Baseline (Uncoordinated)')
    plt.plot(steps, optimized, 'g-o', linewidth=2, label='Optimized (HLX)')

    plt.xlabel("Time Step")
    plt.ylabel("Nodes Restored")
    plt.title("Restoration Performance Under Operational Constraints")
    plt.legend()
    plt.grid(True)

    plot_path = os.path.join(OUTPUT_DIR, "yuri_restoration_plot.png")
    plt.savefig(plot_path)
    plt.close()

    # =========================
    # SUMMARY
    # =========================
    baseline_final = baseline[-1]
    optimized_final = optimized[-1]

    improvement = ((optimized_final - baseline_final) / max(1, baseline_final)) * 100

    summary = {
        "Baseline Restored": baseline_final,
        "Optimized Restored": optimized_final,
        "Improvement (%)": round(improvement, 2)
    }

    df_summary = pd.DataFrame([summary])
    summary_path = os.path.join(OUTPUT_DIR, "yuri_summary.csv")
    df_summary.to_csv(summary_path, index=False)

    print("\n=== RESTORATION SUMMARY ===")
    print(f"Baseline Restored: {baseline_final:.0f}")
    print(f"Optimized Restored: {optimized_final:.0f}")
    print(f"Improvement: {improvement:.2f}%")

    print(f"\nSaved plot → {plot_path}")
    print(f"Saved summary → {summary_path}")

# =========================
# ENTRY
# =========================
if __name__ == "__main__":
    run_simulation()