# HLX Grid Restoration Demo

Simulation of grid restoration under constrained operating conditions.

This project compares baseline restoration behavior with an optimized coordination strategy that improves recovery outcomes while respecting operational limits.

---

## ⚡ Core Result

- Improved restoration outcomes under identical constraints  
- Capacity-aware recovery (no overload or unrealistic propagation)  
- Deterministic, reproducible behavior  

---

## 🔥 Demo 1 — Restoration Performance

Simulates a large-scale outage and compares:

- Baseline (uncoordinated restoration)  
- Coordinated restoration strategy  

### Example Output

```

Baseline Restored: 659
Optimized Restored: 766
Improvement: +16.24%

```

### What it shows

- Both systems operate under identical constraints  
- Improved recovery comes from better coordination  
- No additional resources are introduced  

---

## 🧠 Demo 2 — Phased Restoration Behavior

Models how restoration progresses under real operational constraints.

### Observed Behavior

- Rapid early recovery  
- Controlled ramp under capacity limits  
- Natural slowdown and plateau  
- Identification of restoration boundary  

### Example Output

```

Nodes Restored: 199/200
Percent Restored: 99.50%

⚠ Plateau detected:
Remaining nodes require intervention (topology repair or control recovery)

````

### What it shows

- Restoration has natural limits  
- Automated recovery eventually plateaus  
- Remaining recovery requires targeted intervention  

---

## 📊 Example Visuals

![Restoration Performance](outputs/yuri_restoration_plot.png)

![Phased Restoration](outputs/orchestrator_progress.png)

---

## ▶ Run Demo

```bash
pip install -r requirements.txt
python yuri_demo.py
python orchestrator_demo.py
````

---

## 🧭 What This Is

* A demonstration of restoration behavior under constraints
* A comparison of different decision strategies
* A system-level view of grid recovery dynamics

---

## ⚠ Notes

* This repository contains demonstration logic only
* Internal decision mechanisms are abstracted
* Performance varies depending on system conditions

---

## 🏢 By

Evo Engineering LLC

```
