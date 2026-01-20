import numpy as np
import pandas as pd
import os
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import seaborn as sns
import importlib.util

spec = importlib.util.spec_from_file_location("config", "config/diffdock_heatmap.conf.py")
cfg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cfg)

matrix = pd.read_excel(cfg.rmsd_matrix_file, index_col=0)

colors = ["green", "yellow", "red"]
boundaries = [0, 2, 4, 22]
cmap = LinearSegmentedColormap.from_list('custom_cmap', colors, N=100)
norm = plt.Normalize(vmin=min(boundaries), vmax=max(boundaries))

plt.figure(figsize=(98, 70))
heatmap = sns.heatmap(matrix, cmap=cmap, annot=True, fmt=".2f",
                      cbar_kws={'label': 'RMSD Value', 'ticks': boundaries}, norm=norm)
plt.xlabel('Target', fontsize=50)
plt.ylabel('Reference', fontsize=50)
plt.title('RMSD Heatmap of DiffDock', fontsize=60)

cbar = heatmap.collections[0].colorbar
cbar.ax.tick_params(labelsize=45)
cbar.set_label('RMSD Value', fontsize=50)

os.makedirs(os.path.dirname(cfg.heatmap_output_file), exist_ok=True)
plt.savefig(cfg.heatmap_output_file, dpi=300)
plt.show()
