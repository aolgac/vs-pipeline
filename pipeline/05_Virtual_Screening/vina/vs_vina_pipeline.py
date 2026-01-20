import os
import json
import argparse
import logging
import time
import subprocess
import pandas as pd
from multiprocessing import Pool, cpu_count
from functools import partial

def parse_arguments():
    parser = argparse.ArgumentParser(description="Docking process automation script")
    parser.add_argument(
        "--config",
        type=str,
        default="config.json",
        help="Path to the configuration file (default: config.json)"
    )
    return parser.parse_args()

def is_checkpoint_done(config, checkpoint_name):
    checkpoint_path = os.path.join(config["checkpoints_dir"], checkpoint_name)
    return os.path.exists(checkpoint_path)

def write_checkpoint(config, checkpoint_name):
    checkpoint_path = os.path.join(config["checkpoints_dir"], checkpoint_name)
    with open(checkpoint_path, "w") as f:
        f.write("done")

def extract_molecules(mae_file, config):
    checkpoint_name = f"extract_{os.path.basename(mae_file)}.chk"
    if is_checkpoint_done(config, checkpoint_name):
        logging.info(f"Checkpoint found. Skipping extraction for {mae_file}")
        return

    df = pd.read_csv(config["csv_file"])
    molecule_names = set(df["Molecule Name"].values)
    mae_path = os.path.join(config["mae_dir"], mae_file)
    vs_context = os.path.basename(os.path.dirname(config["extracted_mae_dir"]))

    with open(mae_path, "r") as f:
        mae_content = f.read()

    molecules = mae_content.split("f_m_ct {")
    if len(molecules) <= 1:
        logging.warning(f"No molecules found in the .mae file: {mae_file}")
        return

    header = molecules[0]
    for molecule in molecules[1:]:
        for filename in molecule_names:
            if f'"{filename}"' in molecule:
                formatted_name = f"{vs_context}_{filename.replace(' ', '_')}.mae"
                output_file = os.path.join(config["extracted_mae_dir"], formatted_name)

                with open(output_file, "w") as out_f:
                    out_f.write(header)
                    out_f.write(f"f_m_ct {{\n{molecule}")

    write_checkpoint(config, checkpoint_name)
    logging.info(f"Extraction completed for {mae_file}")

def convert_mae_to_mol2(mae_file, config):
    checkpoint_name = f"convert_mae_to_mol2_{os.path.basename(mae_file)}.chk"
    if is_checkpoint_done(config, checkpoint_name):
        logging.info(f"Checkpoint found. Skipping .mae to .mol2 conversion for {mae_file}")
        return

    base_name = os.path.splitext(os.path.basename(mae_file))[0]
    mol2_file = os.path.join(config["mol2_output_dir"], f"{base_name}.mol2")

    command = [os.path.join(config["schrodinger_path"], "run"), "structconvert.py", mae_file, mol2_file]

    try:
        subprocess.run(command, check=True)
        write_checkpoint(config, checkpoint_name)
        logging.info(f"Converted {mae_file} to {mol2_file}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error converting {mae_file} to .mol2: {e}")

def convert_mol2_to_pdbqt(mol2_file, config):
    checkpoint_name = f"convert_mol2_to_pdbqt_{os.path.basename(mol2_file)}.chk"
    if is_checkpoint_done(config, checkpoint_name):
        logging.info(f"Checkpoint found. Skipping .mol2 to .pdbqt conversion for {mol2_file}")
        return

    base_name = os.path.splitext(os.path.basename(mol2_file))[0]
    pdbqt_file = os.path.join(config["pdbqt_output_dir"], f"{base_name}.pdbqt")

    command = [
        os.path.join(config["mgltools_path"], "bin/pythonsh"),
        os.path.join(config["mgltools_path"], "MGLToolsPckgs/AutoDockTools/Utilities24/prepare_ligand4.py"),
        "-l", mol2_file,
        "-o", pdbqt_file
    ]

    try:
        subprocess.run(command, check=True)
        write_checkpoint(config, checkpoint_name)
        logging.info(f"Converted {mol2_file} to {pdbqt_file}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error converting {mol2_file} to .pdbqt: {e}")

def run_docking(pair, config):
    protein, ligand = pair
    checkpoint_name = f"docking_{protein}_{ligand}.chk"
    if is_checkpoint_done(config, checkpoint_name):
        logging.info(f"Checkpoint found. Skipping docking for {protein} and {ligand}")
        return

    protein_name = protein.replace(".pdbqt", "")
    ligand_name = ligand.replace(".pdbqt", "")
    output_file_name = f"{protein_name}_{ligand_name}.pdbqt"
    output_file = os.path.join(config["docking_output_dir"], output_file_name)

    vina_command = [
        config["vina_path"],
        "--receptor", os.path.join(config["protein_dir"], protein),
        "--ligand", os.path.join(config["pdbqt_output_dir"], ligand),
        "--center_x", str(config["grid_box"]["center_x"]),
        "--center_y", str(config["grid_box"]["center_y"]),
        "--center_z", str(config["grid_box"]["center_z"]),
        "--size_x", str(config["grid_box"]["size_x"]),
        "--size_y", str(config["grid_box"]["size_y"]),
        "--size_z", str(config["grid_box"]["size_z"]),
        "--cpu", "1",
        "--seed", "1698",
        "--out", output_file
    ]

    try:
        subprocess.run(vina_command, check=True)
        write_checkpoint(config, checkpoint_name)
        logging.info(f"Docking completed for {protein} and {ligand}. Output saved to {output_file}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error docking {protein} with {ligand}: {e}")

def main():
    start_time = time.time()
    args = parse_arguments()

    try:
        with open(args.config, "r") as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        print(f"Error: Configuration file {args.config} not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Configuration file {args.config} contains invalid JSON.")
        return

    os.makedirs(config["log_dir"], exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(os.path.join(config["log_dir"], "docking_process.log")), logging.StreamHandler()]
    )

    for key in ["extracted_mae_dir", "mol2_output_dir", "pdbqt_output_dir", "docking_output_dir", "checkpoints_dir"]:
        os.makedirs(config[key], exist_ok=True)

    logging.info("Starting molecule extraction...")
    mae_files = [f for f in os.listdir(config["mae_dir"]) if f.endswith(".mae")]
    with Pool(processes=cpu_count()) as pool:
        pool.map(partial(extract_molecules, config=config), mae_files)

    logging.info("Starting .mae to .mol2 conversion...")
    mae_files = [os.path.join(config["extracted_mae_dir"], f) for f in os.listdir(config["extracted_mae_dir"]) if f.endswith(".mae")]
    with Pool(processes=cpu_count()) as pool:
        pool.map(partial(convert_mae_to_mol2, config=config), mae_files)

    logging.info("Starting .mol2 to .pdbqt conversion...")
    mol2_files = [os.path.join(config["mol2_output_dir"], f) for f in os.listdir(config["mol2_output_dir"]) if f.endswith(".mol2")]
    with Pool(processes=cpu_count()) as pool:
        pool.map(partial(convert_mol2_to_pdbqt, config=config), mol2_files)

    logging.info("Starting docking process...")
    proteins = [f for f in os.listdir(config["protein_dir"]) if f.endswith(".pdbqt")]
    ligands = [f for f in os.listdir(config["pdbqt_output_dir"]) if f.endswith(".pdbqt")]
    docking_pairs = [(protein, ligand) for protein in proteins for ligand in ligands]
    with Pool(processes=config["num_cpus"]) as pool:
        pool.map(partial(run_docking, config=config), docking_pairs)

    elapsed_time = time.time() - start_time
    logging.info(f"Completed docking process in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
