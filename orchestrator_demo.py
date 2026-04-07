"""
HLX Grid Orchestrator Demo (Final Polished)

Demonstrates:
- Phased restoration under operational constraints
- Capacity-limited energization
- Stall detection and adaptive retry
- Plateau identification (intervention boundary)

Author: HLX Grid System
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import os

# =========================
# CONFIG
# =========================
N_NODES = 200
SEED = 42
MAX_STEP_LOAD = 40.0
STALL_THRESHOLD = 3
MAX_PHASES = 6
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# GRID BUILD
# =========================
def build_grid(n_nodes, seed=None):
    np.random.seed(seed)
    G = nx.erdos_renyi_graph(n_nodes, 0.02)

    for n in G.nodes:
        node_type = np.random.choice(["Gen", "Load"], p=[0.1, 0.9])
        G.nodes[n]["type"] = node_type
        G.nodes[n]["status"] = "OFF"
        G.nodes[n]["load"] = np.random.uniform(1, 5)
        G.nodes[n]["gen"] = np.random.uniform(20, 100) if node_type == "Gen" else 0

    return G

# =========================
# INITIALIZATION
# =========================
def initialize_blackstart(G):
    gens = [n for n in G.nodes if G.nodes[n]["type"] == "Gen"]
    blackstart = max(gens, key=lambda x: G.nodes[x]["gen"])

    G.nodes[blackstart]["status"] = "ON"
    return {blackstart}

# =========================
# CASCADE STEP
# =========================
def cascade_step(G, active_nodes):
    newly = set()
    added_load = 0.0

    candidates = []
    for n in active_nodes:
        for nb in G.neighbors(n):
            if G.nodes[nb]["status"] == "OFF":
                candidates.append(nb)

    candidates = list(set(candidates))
    candidates.sort(key=lambda x: G.nodes[x]["load"])

    for n in candidates:
        load = G.nodes[n]["load"]

        if added_load + load > MAX_STEP_LOAD:
            continue

        G.nodes[n]["status"] = "ON"
        newly.add(n)
        added_load += load

    return newly, added_load

# =========================
# MAIN ORCHESTRATOR
# =========================
def run_orchestrator():
    G = build_grid(N_NODES, SEED)
    active = initialize_blackstart(G)

    history = []
    phase_markers = []
    phase_stats = []

    phase = 0
    total_restored = len(active)

    print("\n=== HLX ORCHESTRATED RESTORATION ===")

    while phase < MAX_PHASES:
        phase += 1
        print(f"\n=== Phase {phase} ===")

        stall_count = 0
        phase_added = 0
        phase_mw = 0.0

        for tick in range(1, 50):

            newly, added_load = cascade_step(G, active)

            if newly:
                active.update(newly)
                total_restored = len(active)
                history.append(total_restored)

                phase_added += len(newly)
                phase_mw += added_load
                stall_count = 0
            else:
                stall_count += 1

            percent = (total_restored / N_NODES) * 100

            print(f"[Phase {phase:>2} | Tick {tick:>2}] "
                  f"New: {len(newly):>3}  (+{added_load:6.2f} MW) "
                  f"| Total: {total_restored:>3} ({percent:6.2f}%)")

            if stall_count >= STALL_THRESHOLD:
                print("...stall detected → re-evaluating system state")
                phase_markers.append(len(history))
                break

        phase_stats.append((phase, phase_added, phase_mw, percent))

        if percent >= 98:
            print("\n✔ Automated restoration limit reached")
            phase_markers.append(len(history))
            break

    # =========================
    # SUMMARY
    # =========================
    percent = (total_restored / N_NODES) * 100

    print("\n=== FINAL SUMMARY ===")
    print(f"Nodes Restored: {total_restored}/{N_NODES}")
    print(f"Percent Restored: {percent:.2f}%")
    print(f"Phases Used: {phase}")

    print("\n=== PHASE BREAKDOWN ===")
    for p, added, mw, pct in phase_stats:
        print(f"Phase {p}: +{added} nodes, +{mw:.2f} MW → {pct:.2f}%")

    if percent < 100:
        print("\n⚠ Plateau detected:")
        print("Remaining nodes require intervention (topology repair or control recovery).")

    # =========================
    # VISUALIZATION (ENHANCED)
    # =========================
    plt.figure(figsize=(12, 6))

    # Spread X-axis slightly for readability
    x_vals = np.arange(len(history)) * 2

    plt.plot(x_vals, history, marker='o', linewidth=2, label="Cumulative Nodes Energized")

    # Phase boundaries
    for pt in phase_markers:
        plt.axvline(pt * 2, linestyle='--', alpha=0.4, color='gray')

    # Plateau line
    plt.axhline(total_restored, linestyle='--', alpha=0.5, color='red', label="Plateau")

    plt.xlabel("Iteration (Scaled)")
    plt.ylabel("Nodes Energized")
    plt.title("Phased Restoration Under Operational Constraints")
    plt.grid(True)
    plt.legend()

    plot_path = os.path.join(OUTPUT_DIR, "orchestrator_progress.png")
    plt.savefig(plot_path)
    plt.close()

    print(f"\nSaved plot → {plot_path}")

# =========================
# ENTRY
# =========================
if __name__ == "__main__":
    run_orchestrator()