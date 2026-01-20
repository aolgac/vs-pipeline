import os
import subprocess
import configparser

config = configparser.ConfigParser()
config.read("config/diffdock_inference.conf")

input_csv = config["DEFAULT"]["protein_ligand_csv"]
config_yaml = config["DEFAULT"]["inference_config"]
output_dir = config["DEFAULT"]["out_dir"]
log_file = config["DEFAULT"].get("log_file", "diffdock_inference.log")

os.makedirs(output_dir, exist_ok=True)

cmd = [
    "python3",
    "-m", "inference",
    "--config", "default_inference_args.yaml",
    "--protein_ligand_csv", input_csv,
    "--out_dir", output_dir
]

with open(log_file, "w") as f:
    process = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT)
    print(f"Running DiffDock inference: PID {process.pid}")
