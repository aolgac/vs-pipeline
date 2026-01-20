#!/usr/bin/env python3

import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import configparser


def plot_heatmap(matrix_file, output_png, title, boundaries):
    # Load RMSD matrix
    matrix = pd.read_excel(matrix_file, index_col=0)

    # Define custom colormap
    colors = ["green", "yellow", "red"]
    n_bins = 100
    custom_cmap = LinearSegmentedColormap.from_list(
        "custom_rmsd_cmap", colors, N=n_bins
    )

    norm = plt.Normalize(vmin=min(boundaries), vmax=max(boundaries))

    plt.figure(figsize=(18, 14))
    ax = sns.heatmap(
        matrix,
        cmap=custom_cmap,
        annot=True,
        fmt=".2f",
        norm=norm,
        cbar_kws={
            "label": "RMSD (Å)",
            "ticks": boundaries
        }
    )

    ax.set_xlabel("Target", fontsize=16)
    ax.set_ylabel("Reference Ligand", fontsize=16)
    ax.set_title(title, fontsize=18)

    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=12)
    cbar.set_label("RMSD (Å)", fontsize=14)

    plt.tight_layout()
    plt.savefig(output_png, dpi=300)
    plt.close()

    print(f"Heatmap saved to {output_png}")


def main(conf_file):
    cfg = configparser.ConfigParser()
    cfg.read(conf_file)

    matrix_file = cfg["input"]["matrix_xlsx"]
    output_png = cfg["output"]["heatmap_png"]
    title = cfg["plot"]["title"]

    boundaries = [
        float(x) for x in cfg["plot"]["rmsd_boundaries"].split(",")
    ]

    plot_heatmap(matrix_file, output_png, title, boundaries)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python 9_glide_rmsd_heatmap.py heatmap.conf")
        sys.exit(1)

    main(sys.argv[1])
