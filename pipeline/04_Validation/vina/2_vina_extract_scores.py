import os
import pandas as pd
import yaml

with open("vina_scores.conf.example", "r") as f:
    config = yaml.safe_load(f)

pdbqt_dir = config["pdbqt_dir"]
output_csv = config["output_csv"]

data = []

for pdbqt_file in os.listdir(pdbqt_dir):
    if pdbqt_file.endswith('.pdbqt'):
        file_path = os.path.join(pdbqt_dir, pdbqt_file)
        
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith("REMARK VINA RESULT:"):
                    vina_result = float(line.split()[3])
                    data.append([pdbqt_file, vina_result])
                    break  # Move to next file after extracting result

df = pd.DataFrame(data, columns=['File Name', 'Vina Result'])
df.to_csv(output_csv, index=False)
print(f"CSV file saved to {output_csv}")
