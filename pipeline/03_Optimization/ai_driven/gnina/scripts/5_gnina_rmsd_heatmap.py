import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import importlib.util

config_path = os.path.join(os.path.dirname(__file__), "../config/gnina_heatmap.conf")
spec = importlib.util.spec_from_file_location("conf", config_path)
conf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(conf)

os.makedirs(os.path.dirname(conf.output_png), exist_ok=True)

matrix = pd.read_csv(conf.input_csv, index_col=0)

cmap = LinearSegmentedColormap.from_list("custom_cmap", conf.colors, N=100)
norm = plt.Normalize(vmin=min(conf.boundaries), vmax=max(conf.boundaries))

plt.figure(figsize=conf.figure_size)
heatmap = sns.heatmap(matrix, cmap=cmap, annot=conf.annot, fmt=conf.fmt, cbar_kws={'label': 'RMSD Value', 'ticks': conf.boundaries}, norm=norm)

plt.xlabel('Target', fontsize=conf.fontsize_labels)
plt.ylabel('Reference', fontsize=conf.fontsize_labels)
plt.title('RMSD Heatmap of Gnina', fontsize=conf.fontsize_title)

cbar = heatmap.collections[0].colorbar
cbar.ax.tick_params(labelsize=conf.fontsize_cbar)
cbar.set_label('RMSD Value', fontsize=conf.fontsize_cbar)

plt.savefig(conf.output_png, dpi=conf.dpi)
plt.show()
