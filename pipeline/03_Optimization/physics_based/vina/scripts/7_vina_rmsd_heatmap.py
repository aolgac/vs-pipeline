from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import sys

def load_config(cfg_path):
    cfg = {}
    with open(cfg_path) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                k, v = line.strip().split("=", 1)
                cfg[k.strip()] = v.strip()
    return cfg

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python vina_rmsd_heatmap.py config.conf")

    cfg = load_config(sys.argv[1])

    matrix_file = Path(cfg["MATRIX_FILE"])
    output_png = Path(cfg["OUTPUT_PNG"])

    df = pd.read_excel(matrix_file, index_col=0)

    colors = ["green", "yellow", "red"]
    boundaries = [0, 2, 4, float(df.max().max())]
    cmap = LinearSegmentedColormap.from_list("rmsd_cmap", colors, N=100)

    plt.figure(figsize=(20, 15))
    ax = sns.heatmap(
        df,
        cmap=cmap,
        annot=True,
        fmt=".2f",
        cbar_kws={"label": "RMSD"}
    )

    ax.set_xlabel("Target")
    ax.set_ylabel("Reference")
    ax.set_title("Vina RMSD Heatmap")

    plt.tight_layout()
    plt.savefig(output_png, dpi=300)
    plt.close()

if __name__ == "__main__":
    main()
