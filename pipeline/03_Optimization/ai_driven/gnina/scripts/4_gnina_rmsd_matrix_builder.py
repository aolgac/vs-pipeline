import os
import pandas as pd
import importlib.util

config_path = os.path.join(os.path.dirname(__file__), "../config/gnina_rmsd_matrix.conf")
spec = importlib.util.spec_from_file_location("conf", config_path)
conf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(conf)

os.makedirs(os.path.dirname(conf.output_csv), exist_ok=True)

df = pd.read_csv(conf.input_csv)
df["Pose_Grid"] = df["Pose_File"].str.extract(r"^([0-9A-Za-z]+(?:_[A-Za-z]+)?)")
matrix = df.pivot(index="Reference_Ligand", columns="Pose_Grid", values="RMSD")
matrix.to_csv(conf.output_csv)

print("RMSD matrix created successfully:")
print(matrix)
