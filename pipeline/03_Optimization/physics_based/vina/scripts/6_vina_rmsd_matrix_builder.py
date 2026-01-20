from pathlib import Path
import pandas as pd
import sys
import re

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
        raise SystemExit("Usage: python vina_rmsd_matrix_builder.py config.conf")

    cfg = load_config(sys.argv[1])

    input_csv = Path(cfg["INPUT_CSV"])
    output_file = Path(cfg["OUTPUT_FILE"])

    df = pd.read_csv(input_csv)

    # Extract grid / protein identifier from pose filename
    df["Pose_Grid"] = df["Pose"].apply(
        lambda x: re.search(r"([0-9A-Za-z]+(?:_[A-Za-z]+)?)", x).group(1)
        if isinstance(x, str) else None
    )

    matrix = df.pivot(
        index="Reference",
        columns="Pose_Grid",
        values="RMSD"
    )

    if output_file.suffix == ".xlsx":
        matrix.to_excel(output_file)
    else:
        matrix.to_csv(output_file)

    print("RMSD matrix created.")

if __name__ == "__main__":
    main()
