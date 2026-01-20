import argparse
import json
import logging
import os
import shutil
import time

def copy_mae_dir(config):
    """Copy .mae files to a working directory, checkpointed."""
    checkpoint_copy = "copy_mae_dir.chk"
    checkpoint_path = os.path.join(config["checkpoints_dir"], checkpoint_copy)
    if os.path.exists(checkpoint_path):
        logging.info("MAE directory copy checkpoint found. Skipping copying.")
        return

    src = config["mae_dir"]
    dst = os.path.join(config["copied_mae_dir"], "mae")
    logging.info(f"Copying MAE directory from {src} to {dst}")

    try:
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        logging.info("MAE directory copied successfully.")

        os.makedirs(config["checkpoints_dir"], exist_ok=True)
        with open(checkpoint_path, "w") as f:
            f.write("done")
    except Exception as e:
        logging.error(f"Failed to copy MAE directory: {e}")
        raise e

def generate_in_files(config):
    """Generate Glide .in input files for docking from .mae ligands."""
    input_scripts_dir = config.get("input_scripts_dir", os.path.join(config["copied_mae_dir"], "input_scripts"))
    mae_dir = os.path.join(config["copied_mae_dir"], "mae")
    grid_file = config["grid_file"]

    os.makedirs(input_scripts_dir, exist_ok=True)
    mae_files = [f for f in os.listdir(mae_dir) if f.endswith(".mae")]
    logging.info(f"Found {len(mae_files)} .mae files to create .in scripts.")

    for mae_file in mae_files:
        ligand_path = os.path.join(mae_dir, mae_file)
        in_file_name = os.path.splitext(mae_file)[0] + ".in"
        in_file_path = os.path.join(input_scripts_dir, in_file_name)

        file_content = f"""GRIDFILE   {grid_file}
LIGANDFILE   {ligand_path}
CALC_INPUT_RMS   True
DOCKING_METHOD confgen
FORCEFIELD OPLS4
POSE_OUTTYPE ligandlib_sd
PRECISION SP
"""
        with open(in_file_path, "w") as f:
            f.write(file_content)
        logging.info(f"Created {in_file_path}")

def main():
    parser = argparse.ArgumentParser(description="Glide Step 1: Prepare MAE files and .in scripts")
    parser.add_argument("config", type=str, help="Path to configuration JSON file")
    args = parser.parse_args()

    # Load config
    try:
        with open(args.config, "r") as f:
            config = json.load(f)
    except Exception as e:
        print(f"Failed to load config file: {e}")
        return

    # Setup logging
    os.makedirs(config["log_dir"], exist_ok=True)
    log_path = os.path.join(config["log_dir"], "pipeline_step1.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_path), logging.StreamHandler()]
    )

    start_time = time.time()

    try:
        copy_mae_dir(config)
    except Exception:
        logging.error("Aborting due to error in copying MAE directory.")
        return

    checkpoint_infiles = "generated_in_files.chk"
    checkpoint_infiles_path = os.path.join(config["checkpoints_dir"], checkpoint_infiles)
    if os.path.exists(checkpoint_infiles_path):
        logging.info("Checkpoint found for .in files generation. Skipping.")
    else:
        logging.info("Generating .in files...")
        generate_in_files(config)
        os.makedirs(config["checkpoints_dir"], exist_ok=True)
        with open(checkpoint_infiles_path, "w") as f:
            f.write("done")

    elapsed_time = time.time() - start_time
    logging.info(f"Step 1 completed in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
