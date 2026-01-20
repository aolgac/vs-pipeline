#!/usr/bin/env python3

import sys
import pandas as pd
import configparser


def build_rmsd_matrix(input_csv, output_xlsx, regex):
    df = pd.read_csv(input_csv)

    # Extract grid / target identifier from Pose_File
    df["Pose_Grid"] = df["Pose_File"].str.extract(regex)

    matrix = df.pivot(
        index="Reference_Ligand",
        columns="Pose_Grid",
        values="RMSD"
    )

    matrix.to_excel(output_xlsx)
    print(f"RMSD matrix written to {output_xlsx}")


def main(conf_file):
    cfg = configparser.ConfigParser()
    cfg.read(conf_file)

    input_csv = cfg["input"]["rmsd_csv"]
    output_xlsx = cfg["output"]["matrix_xlsx"]
    regex = cfg["parsing"]["pose_grid_regex"]

    build_rmsd_matrix(input_csv, output_xlsx, regex)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python 8_glide_rmsd_matrix_builder.py rmsd_matrix.conf")
        sys.exit(1)

    main(sys.argv[1])
