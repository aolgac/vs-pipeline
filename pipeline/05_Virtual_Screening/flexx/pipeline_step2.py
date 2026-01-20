import os
import json
import argparse
import subprocess

def load_config(config_path):
    with open(config_path, "r") as f:
        return json.load(f)

def run_flexx_docking(config):
    input_sdf = config["merged_sdf_path"]
    protein_path = config["protein_path"]
    reference_ligand = config.get("reference_ligand", None)
    
    checkpoint_dir = config["checkpoint_dir"]
    flexx_executable = config["flexx_executable"]
    output_sdf = os.path.join(config["output_base_dir"], config.get("docking_output_sdf_name", "flexx_docked.sdf"))
    checkpoint_file = os.path.join(checkpoint_dir, "flexx_docking_done.chk")
    log_file_path = os.path.join(config["output_base_dir"], "flexx_docking.log")

    os.makedirs(checkpoint_dir, exist_ok=True)
    os.makedirs(config["output_base_dir"], exist_ok=True)

    if os.path.exists(checkpoint_file):
        print("FlexX docking skipped (checkpoint exists).")
        return

    command = [
        flexx_executable,
        "-i", input_sdf,
        "-o", output_sdf,
        "--protein", protein_path
    ]

    if reference_ligand:
        command += ["--refligand", reference_ligand]

    command += ["-v", "4"]

    print("Running FlexX docking...")
    try:
        with open(log_file_path, "w") as log_file:
            subprocess.run(command, check=True, stdout=log_file, stderr=subprocess.STDOUT)
        with open(checkpoint_file, "w") as f:
            f.write("done")
        print("Docking completed successfully. Log saved to:", log_file_path)
    except subprocess.CalledProcessError:
        print("FlexX docking failed.")
        print("Command:", " ".join(command))
        print(f"Check log file: {log_file_path}")
        raise

def main():
    parser = argparse.ArgumentParser(description="Run FlexX docking with config file")
    parser.add_argument("-c", "--config", required=True, help="Path to JSON config file")
    args = parser.parse_args()

    config = load_config(args.config)
    run_flexx_docking(config)

if __name__ == "__main__":
    main()
