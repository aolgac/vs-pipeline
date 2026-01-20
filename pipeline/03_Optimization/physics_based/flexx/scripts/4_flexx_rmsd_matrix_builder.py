import pandas as pd
import json

with open("flexx_rmsd_matrix.conf") as f:
    cfg = json.load(f)

df = pd.read_csv(cfg["input_csv"])
df["Pose_Grid"] = df[cfg["pose_column"]].str.extract(cfg["grid_regex"])
matrix = df.pivot(
    index=cfg["index_column"],
    columns="Pose_Grid",
    values=cfg["value_column"]
)
matrix.to_excel(cfg["output_xlsx"])
