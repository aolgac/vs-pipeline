import os
import pandas as pd
import yaml

with open("flexx_extract_scores.conf.example", "r") as f:
    config = yaml.safe_load(f)

sdf_dir = config["sdf_dir"]
output_csv = config["output_csv"]

data = []

for sdf_file in os.listdir(sdf_dir):
    if sdf_file.endswith(".sdf"):
        file_path = os.path.join(sdf_dir, sdf_file)
        with open(file_path, "r") as f:
            content = f.read()
            if "<BIOSOLVEIT.DOCKING_SCORE>" in content:
                start_idx = content.find("<BIOSOLVEIT.DOCKING_SCORE>") + len("<BIOSOLVEIT.DOCKING_SCORE>")
                end_idx = content.find("$$$$", start_idx)
                score = content[start_idx:end_idx].strip()
                data.append([sdf_file, float(score)])

df = pd.DataFrame(data, columns=["File Name", "Results"])
df.to_csv(output_csv, index=False)

print(f"Docking scores extracted and saved to {output_csv}")
