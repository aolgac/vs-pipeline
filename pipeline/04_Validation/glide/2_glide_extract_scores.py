import os
import re
import pandas as pd
import yaml

with open("glide_scores.conf.example", "r") as f:
    config = yaml.safe_load(f)

log_dir = config["log_dir"]
output_csv = config["output_csv"]

score_pattern = re.compile(r"Best docking score:\s*(-\d+\.\d+)")

results = []

for log_file in os.listdir(log_dir):
    if log_file.endswith(".log"):
        log_file_path = os.path.join(log_dir, log_file)
        with open(log_file_path, "r") as f:
            content = f.read()
            match = score_pattern.search(content)
            if match:
                best_score = float(match.group(1))
                results.append([log_file, best_score])

df = pd.DataFrame(results, columns=["File Name", "Results"])
df.to_csv(output_csv, index=False)

print(f"Best docking scores saved to {output_csv}")
