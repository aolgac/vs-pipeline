import os
import importlib.util

config_path = os.path.join(os.path.dirname(__file__), "../config/gnina_extract_first_pose.conf")
spec = importlib.util.spec_from_file_location("conf", config_path)
conf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(conf)

os.makedirs(conf.output_dir, exist_ok=True)

def extract_first_pose(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            outfile.write(line)
            if line.strip() == "$$$$":
                break

for filename in os.listdir(conf.input_dir):
    if filename.endswith(".sdf"):
        input_file = os.path.join(conf.input_dir, filename)
        output_file = os.path.join(conf.output_dir, filename)
        extract_first_pose(input_file, output_file)

print("Extraction of first ligand poses complete!")
