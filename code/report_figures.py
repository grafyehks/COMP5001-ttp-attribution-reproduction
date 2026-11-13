# Run after improvements.ipynb, inside the project environment:
#   conda activate p3
#   poetry run python report_figures.py
# Figures are written to results/improvements/figures/
import sys
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt

# Default: this file sits in code/, so the project root is one level up.
R = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else R / "results" / "improvements" / "figures"
OUT.mkdir(parents=True, exist_ok=True)
DATA = R / "data"
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#ffffff"
S1, S2, S3, GREY = "#2a78d6", "#eb6834", "#1baf7a", "#a9a8a2"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK2, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.titlesize": 10, "axes.titleweight": "bold", "axes.titlecolor": INK,
                     "axes.spines.top": False, "axes.spines.right": False, "figure.facecolor": SURF})

b1 = pd.read_csv(R / "results/improvements/B1_corrected_metric.csv")
isl = pd.read_csv(R / "results/improvements/C2_information_islands_scorecard.csv")
led = pd.read_csv(R / "results/improvements/A2_number_ledger.csv")
aud = pd.read_csv(R / "results/improvements/A3_cisa_source_audit.csv")
b2 = pd.read_csv(R / "results/improvements/B2_shuffle_test.csv")

# recompute pair distributions for the histogram
comp = pd.read_pickle(DATA / "comp_data_ttps.pkl")
X = comp.to_numpy().astype(bool); lab = comp.index.get_level_values("TA").to_numpy()
same, diff = [], []
for i in range(len(X)):
    for j in range(i + 1, len(X)):
        v = (X[i] & X[j]).sum() / min(X[i].sum(), X[j].sum())
        (same if lab[i] == lab[j] else diff).append(v)
same, diff = np.array(same), np.array(diff)

def fig_b1(ax):
    rows = b1[b1["result"].str.contains("average|Table 6")].copy()
    names = ["Same group\n(Table 5)", "Different groups,\ncompany (Table 6a)", "Different groups,\nCISA (Table 6b)"]
    rep = rows.iloc[:, 1].to_numpy(); eq1 = rows.iloc[:, 2].to_numpy()
    y = np.arange(3)[::-1]; h = 0.36
    ax.barh(y + h/2 + 0.01, rep, height=h, color=GREY, label="Reported (code: containment)", edgecolor=SURF, linewidth=1)
    ax.barh(y - h/2 - 0.01, eq1, height=h, color=S1, label="Paper's Eq. 1 (overlap)", edgecolor=SURF, linewidth=1)
    for yy, a, b in zip(y, rep, eq1):
        ax.text(a + 0.01, yy + h/2 + 0.01, f"{a:.2f}", va="center", color=INK2, fontsize=8.5)
        ax.text(b + 0.01, yy - h/2 - 0.01, f"{b:.2f}", va="center", color=INK, fontsize=8.5, fontweight="bold")
    ax.set_yticks(y, names); ax.set_xlim(0, 0.8); ax.set_xlabel("Mean similarity (0 = nothing shared, 1 = identical)")
    ax.xaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True); ax.tick_params(axis="y", length=0)
    ax.legend(loc="upper right", frameon=False, fontsize=8)
    ax.set_title("With its own formula, different groups look as alike as the same group", loc="left")

def fig_b2(ax):
    bins = np.linspace(0, 1, 21)
    ax.hist(diff, bins=bins, density=True, color=S1, alpha=0.55, edgecolor=SURF, linewidth=1, label=f"Different groups ({len(diff)} pairs)")
    ax.hist(same, bins=bins, density=True, color=S2, alpha=0.55, edgecolor=SURF, linewidth=1, label=f"Same group ({len(same)} pairs)")
    ax.set_ylim(0, 6.6); top = 6.6
    for m, c, t in [(diff.mean(), S1, "mean"), (same.mean(), S2, "mean")]:
        ax.axvline(m, color=c, lw=1.5, ls="--")
    ax.text(diff.mean() - 0.01, top * 0.97, f"{diff.mean():.2f}", ha="right", va="top", color=INK, fontsize=8.5, fontweight="bold")
    ax.text(same.mean() + 0.01, top * 0.97, f"{same.mean():.2f}", ha="left", va="top", color=INK, fontsize=8.5, fontweight="bold")
    p = float(b2.loc[b2["pile"].str.startswith("p-value"), "value"].iloc[0])
    ax.text(0.99, 0.55, f"Shuffle test (2,000 runs)\np = {p:.3f}", transform=ax.transAxes, ha="right", va="top", color=INK2, fontsize=8)
    ax.set_xlim(0, 1); ax.set_xlabel("Overlap similarity between two incident reports (Eq. 1)"); ax.set_ylabel("Share of pairs (density)")
    ax.yaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
    ax.legend(loc="upper right", bbox_to_anchor=(1, 0.86), frameon=False, fontsize=8)
    ax.set_title("Same-group reports are more alike, but the piles overlap heavily", loc="left")

def fig_c2(ax):
    d = isl.copy()
    d["name"] = d["group (company / CISA)"].str.replace(" / ", " / ", regex=False)
    d["total"] = d[["seen by both", "company only", "CISA only"]].sum(axis=1)
    d = d.sort_values("total")
    y = np.arange(len(d))
    left = np.zeros(len(d))
    for col, c, lbl in [("seen by both", S3, "Seen by both sources"), ("company only", S1, "Company only"), ("CISA only", S2, "CISA only")]:
        v = d[col].to_numpy()
        ax.barh(y, v, left=left, color=c, edgecolor=SURF, linewidth=2, height=0.62, label=lbl)
        for yy, l, w in zip(y, left, v):
            if w >= 7:
                ax.text(l + w/2, yy, str(int(w)), ha="center", va="center", color="white", fontsize=8, fontweight="bold")
        left += v
    for yy, t, s in zip(y, d["total"], d["strong clues"]):
        ax.text(t + 1.5, yy, f"{int(s)} strong clue{'s' if s != 1 else ''}", va="center", color=INK, fontsize=8.5)
    labels = [n + (" *" if u.startswith("yes") else "") for n, u in zip(d["name"], d["link uncertain?"])]
    ax.set_yticks(y, labels); ax.tick_params(axis="y", length=0)
    ax.set_xlim(0, d["total"].max() + 22); ax.set_xlabel("Number of ATT&CK technique entries recorded for the group")
    ax.xaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
    ax.legend(loc="lower right", frameon=False, fontsize=8, ncol=1)
    ax.set_title("Each source sees part of each group; strong clues are rare", loc="left")
    ax.text(0, -0.34, "* name link marked uncertain (#?) by the authors.  Strong clue = seen by both sources and used by <25% of groups.",
            transform=ax.transAxes, fontsize=7.5, color=INK2)

def save_single(fn, name, size):
    fig, ax = plt.subplots(figsize=size)
    fn(ax); fig.tight_layout(); fig.savefig(OUT / name, dpi=300); plt.close(fig)

save_single(fig_b1, "Fig_B1_corrected_metric.png", (7, 3.2))
save_single(fig_b2, "Fig_B2_same_vs_different.png", (7, 3.4))
save_single(fig_c2, "Fig_C2_information_islands.png", (7, 3.6))

# Composite "trust dashboard": headline tiles + three panels
n_ok = (led["match"] == "✅").sum(); n_flag = (aud["check"] != "OK").sum()
p = float(b2.loc[b2["pile"].str.startswith("p-value"), "value"].iloc[0])
fig = plt.figure(figsize=(11, 8.2))
gs = fig.add_gridspec(3, 2, height_ratios=[0.36, 1, 1], hspace=0.45, wspace=0.32, top=0.93)
tiles = [(f"{n_ok}/{len(led)}", "reported numbers\nreproduced exactly (A2)"),
         (f"{n_flag}/{len(aud)}", "CISA sources need an\nerratum (A3)"),
         (f"{diff.mean():.2f} vs {same.mean():.2f}", f"different vs same group,\np = {p:.3f} (B2)"),
         (f"{int(isl['strong clues'].sum())}", "strong clues across\n6 groups (C2)")]
tax = fig.add_subplot(gs[0, :]); tax.axis("off")
for k, (big, small) in enumerate(tiles):
    x = 0.01 + k * 0.25
    tax.add_patch(plt.Rectangle((x, 0.02), 0.23, 0.96, transform=tax.transAxes, facecolor="#f4f3ef", edgecolor="none"))
    tax.text(x + 0.015, 0.72, big, transform=tax.transAxes, fontsize=17, fontweight="bold", color=INK, va="center")
    tax.text(x + 0.015, 0.27, small, transform=tax.transAxes, fontsize=8.5, color=INK2, va="center")
fig_b1(fig.add_subplot(gs[1, 0])); fig_b2(fig.add_subplot(gs[1, 1]))
fig_c2(fig.add_subplot(gs[2, :]))
fig.suptitle("Can we trust the numbers? Reproduction and improvement results", x=0.125, y=0.985, ha="left", fontsize=13, fontweight="bold", color=INK)
fig.savefig(OUT / "Fig_Trust_Dashboard.png", dpi=300, bbox_inches="tight")
print("done", sorted(p.name for p in OUT.iterdir()))
