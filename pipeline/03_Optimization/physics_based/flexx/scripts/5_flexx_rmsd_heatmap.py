import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

with open("flexx_heatmap.conf") as f:
    cfg = json.load(f)

matrix = pd.read_excel(cfg["input_matrix"], index_col=0)

cmap = LinearSegmentedColormap.from_list(
    "custom_cmap",
    cfg["colors"],
    N=cfg["n_bins"]
)

norm = plt.Normalize(vmin=min(cfg["boundaries"]), vmax=max(cfg["boundaries"]))

plt.figure(figsize=tuple(cfg["figsize"]))
ax = sns.heatmap(
    matrix,
    cmap=cmap,
    annot=cfg["annot"],
    fmt=cfg["fmt"],
    norm=norm,
    cbar_kws={"ticks": cfg["boundaries"], "label": cfg["cbar_label"]}
)

ax.set_xlabel(cfg["xlabel"], fontsize=cfg["label_fontsize"])
ax.set_ylabel(cfg["ylabel"], fontsize=cfg["label_fontsize"])
ax.set_title(cfg["title"], fontsize=cfg["title_fontsize"])

cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=cfg["cbar_tick_fontsize"])
cbar.set_label(cfg["cbar_label"], fontsize=cfg["cbar_label_fontsize"])

plt.savefig(cfg["output_png"], dpi=cfg["dpi"])
