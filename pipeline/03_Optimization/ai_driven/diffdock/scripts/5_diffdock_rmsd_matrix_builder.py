import pandas as pd
import configparser
import os

config = configparser.ConfigParser()
config.read("config/diffdock_rmsd_matrix.conf")

csv_file = config["DEFAULT"]["csv_file"]
output_file = config["DEFAULT"]["output_file"]

df = pd.read_csv(csv_file)

# Extract the unique grid identifier from Pose_File
df["Pose_Grid"] = df["Pose_File"].str.extract(r"^([0-9A-Za-z]+(?:_[A-Za-z]+)?)")

# Pivot to create matrix
matrix = df.pivot(index="Reference_Ligand", columns="Pose_Grid", values="RMSD")

# Ensure output directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Save matrix to Excel
matrix.to_excel(output_file)

print(f"Matrix created successfully: {output_file}")
print(matrix)