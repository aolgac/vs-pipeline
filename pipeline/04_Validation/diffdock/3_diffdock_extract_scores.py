import os
import re
import pandas as pd
import yaml

with open("diffdock_scores.conf.example", "r") as f:
    config = yaml.safe_load(f)

sdf_folder = config["sdf_folder"]
output_csv = config["output_csv"]

patterns = {
    "minimizedAffinity": r"> <minimizedAffinity>\n(.*?)\n"
}

data = []

for sdf_file in os.listdir(sdf_folder):
    if sdf_file.endswith(".sdf"):
        with open(os.path.join(sdf_folder, sdf_file), 'r') as file:
            content = file.read()
            file_data = {"File": sdf_file}
            for key, pattern in patterns.items():
                match = re.search(pattern, content)
                file_data[key] = match.group(1) if match else None
            data.append(file_data)

df = pd.DataFrame(data)
df.to_csv(output_csv, index=False)
print(f"Extracted DiffDock & GNINA rescoring results saved to {output_csv}")
