#!/usr/bin/env python3
"""Illustrate exact formulas. Floating-point plotting does not prove inequalities."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
n = np.arange(2, 501, dtype=float)
fixed = np.exp(n * np.log(40 / 41)) / 200
claim = n ** -2
envelope = 0.2 / n * np.exp((n - 1) * np.log1p(-1 / n))
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False})
fig, ax = plt.subplots(figsize=(7.2, 3.5), constrained_layout=True)
ax.loglog(n, claim, color="#796325", linewidth=2,
          label="Conjectured bound: 1/N²")
ax.loglog(n, fixed, color="#744A7D", linewidth=2,
          label="One fixed rational matrix")
ax.loglog(n, envelope, color="#28776B", linewidth=2,
          label="Optimised linear envelope (instance varies with N)")
ax.scatter([20], [(40 / 41) ** 20 / 200], color="#744A7D", zorder=5, s=30)
ax.annotate("N = 20: 22.05% above the claim",
            xy=(20, (40 / 41) ** 20 / 200), xytext=(35, 0.012),
            fontsize=9, arrowprops={"arrowstyle": "-", "color": "#744A7D"})
ax.set_xlabel("Residual index N (N − 1 completed updates)")
ax.set_ylabel("Squared residual / initial distance²")
ax.set_xlim(2, 500)
ax.set_ylim(1e-8, 0.4)
ax.grid(True, which="major", color="#DEDEDE", linewidth=0.6)
ax.legend(loc="lower left", fontsize=8.5, frameon=False)
fig.savefig(ROOT / "residual_rates.png", dpi=220, facecolor="white")
print(ROOT / "residual_rates.png")

