import os
import json
import logging
import re
import pandas as pd
import subprocess
from concurrent.futures import ThreadPoolExecutor
from time import time
import argparse


def parse_mae_to_dict(mae_file):
    with open(mae_file, "r") as f:
        content = f.read()

    molecules = content.split("f_m_ct {")
    if len(molecules) <= 1:
        return {}

    header = molecules[0]
    molecule_dict = {}

    for molecule in molecules[1:]:
        match = re.search(r'"(.+)"', molecule)
        if match:
            name = match.group(1)
            molecule_dict[name] = header + f"f_m_ct {{\n{molecule}"

    return molecule_dict


def parse_csv_to_dict(csv_file):
    df = pd.read_csv(csv_file)
    return set(df["Molecule Name"].values)


def write_molecule_to_file(args):
    output_file, content = args
    with open(output_file, "w") as f:
        f.write(content)

def extract_molecules(mae_dict, molecule_names, config, vs_context):
    checkpoint_dir = config["checkpoint_dir"]
    os.makedirs(config["extracted_mae_dir"], exist_ok=True)

    to_write = []

    for name, molecule in mae_dict.items():
        if name not in molecule_names:
            continue

        formatted = f"{vs_context}_{name.replace(' ', '_')}.mae"
        out_path = os.path.join(config["extracted_mae_dir"], formatted)
        chk = os.path.join(checkpoint_dir, f"{formatted}.chk")

        if os.path.exists(chk):
            logging.info(f"Checkpoint exists, skipping {formatted}")
            continue

        to_write.append((out_path, molecule))

        with open(chk, "w") as f:
            f.write("DONE")

    with ThreadPoolExecutor() as exe:
        exe.map(write_molecule_to_file, to_write)

def convert_mae_to_mol2(mae_files, config):
    checkpoint_dir = config["checkpoint_dir"]
    os.makedirs(config["mol2_output_dir"], exist_ok=True)

    def convert_single(mae_file):
        base = os.path.splitext(os.path.basename(mae_file))[0]
        mol2 = os.path.join(config["mol2_output_dir"], f"{base}.mol2")
        chk = os.path.join(checkpoint_dir, f"{base}.mol2.chk")

        if os.path.exists(chk):
            logging.info(f"Skipping conversion (checkpoint): {base}")
            return

        cmd = [
            config["schrodinger_run"],
            "structconvert.py",
            mae_file,
            mol2
        ]

        try:
            subprocess.run(cmd, check=True)
            with open(chk, "w") as f:
                f.write("DONE")
            logging.info(f"Converted {base}.mae → mol2")
        except subprocess.CalledProcessError as e:
            logging.error(f"Conversion failed for {mae_file}: {e}")

    with ThreadPoolExecutor() as exe:
        exe.map(convert_single, mae_files)

def generate_diffdock_csv(ligand_dir, output_csv, protein_file):
    ligands = []

    for root, _, files in os.walk(ligand_dir):
        for f in files:
            if f.endswith((".sdf", ".mol2")):
                ligands.append(os.path.join(root, f))

    ligands.sort()
    protein_base = os.path.splitext(os.path.basename(protein_file))[0]

    rows = []
    for lig in ligands:
        lig_base = os.path.splitext(os.path.basename(lig))[0]
        rows.append({
            "complex_name": f"{protein_base}_{lig_base}",
            "protein_path": protein_file,
            "ligand_description": lig,
            "protein_sequence": None
        })

    pd.DataFrame(rows).to_csv(output_csv, index=False)
    logging.info(f"DiffDock CSV created: {output_csv} ({len(rows)} complexes)")


def create_slurm_script(config):
    if not config.get("create_slurm_script", False):
        return

    slurm_dir = config["slurm_dir"]
    os.makedirs(slurm_dir, exist_ok=True)

    job = config.get("slurm_job_name", "diffdock_job")
    script = os.path.join(slurm_dir, f"{job}.sh")

    content = f"""#!/bin/bash
#SBATCH --job-name={job}
#SBATCH --output={slurm_dir}/{job}_%j.out
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --partition=gpu

source ~/.bashrc
conda activate {config["conda_env"]}

cd {config["diffdock_root"]}

python -m inference \\
  --config {config["diffdock_config"]} \\
  --protein_ligand_csv {config["final_csv_output"]} \\
  --out_dir {config["slurm_output_dir"]}
"""

    with open(script, "w") as f:
        f.write(content)

    logging.info(f"SLURM script written: {script}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", required=True)
    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)

    start = time()

    os.makedirs(config["log_dir"], exist_ok=True)
    os.makedirs(config["checkpoint_dir"], exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(os.path.join(config["log_dir"], "pipeline.log")),
            logging.StreamHandler()
        ]
    )

    logging.info("Starting DiffDock pipeline")

    molecule_names = parse_csv_to_dict(config["csv_file"])
    vs_context = os.path.basename(os.path.dirname(config["extracted_mae_dir"]))

    for mae in os.listdir(config["mae_dir"]):
        if mae.endswith(".mae"):
            mae_path = os.path.join(config["mae_dir"], mae)
            mae_dict = parse_mae_to_dict(mae_path)
            extract_molecules(mae_dict, molecule_names, config, vs_context)

    extracted = [
        os.path.join(config["extracted_mae_dir"], f)
        for f in os.listdir(config["extracted_mae_dir"])
        if f.endswith(".mae")
    ]

    convert_mae_to_mol2(extracted, config)

    generate_diffdock_csv(
        config["mol2_output_dir"],
        config["final_csv_output"],
        config["protein_file"]
    )

    create_slurm_script(config)

    logging.info(f"Pipeline finished in {time() - start:.2f} seconds")


if __name__ == "__main__":
    main()
