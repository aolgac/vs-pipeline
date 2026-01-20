import os
import json
import gzip
import shutil
import logging
from pathlib import Path

def setup_logging(log_file):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def copy_and_decompress_gz(src_gz_path, dest_sdf_path):
    try:
        copied_gz_path = dest_sdf_path.with_suffix(".sdfgz")
        shutil.copy(src_gz_path, copied_gz_path)
        logging.info(f"Copied {src_gz_path} to {copied_gz_path}")

        with gzip.open(copied_gz_path, 'rb') as f_in:
            with open(dest_sdf_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        logging.info(f"Decompressed {copied_gz_path} to {dest_sdf_path}")

        os.remove(copied_gz_path)
        logging.info(f"Deleted temporary file {copied_gz_path}")
    except Exception as e:
        logging.error(f"Error processing {src_gz_path}: {e}")
        raise

def main(config_path):
    with open(config_path, 'r') as f:
        config = json.load(f)

    input_dir = Path(config["input_scripts_dir"])
    output_dir = Path(config["output_files_dir"])
    checkpoints_dir = Path(config["checkpoints_dir"])
    checkpoint_file_name = config.get("checkpoint_file_name", "failed_jobs.chk")
    checkpoint_file = checkpoints_dir / checkpoint_file_name
    docking_results_dir = Path(config["docking_results_dir"])
    docking_results_dir.mkdir(exist_ok=True, parents=True)
    log_dir = Path(config.get("log_dir", "."))
    log_file = log_dir / "pipeline_step3.log"
    setup_logging(log_file)

    logging.info("Starting Glide Step 3: Process docking results")

    in_basenames = {f.stem for f in input_dir.glob("*.in")}
    sdfgz_files = list(output_dir.glob("*_lib.sdfgz"))
    completed_basenames = {f.name.replace("_lib.sdfgz", "") for f in sdfgz_files}
    incomplete_jobs = sorted(list(in_basenames - completed_basenames))

    checkpoints_dir.mkdir(exist_ok=True, parents=True)
    with open(checkpoint_file, 'w') as chk:
        for job in incomplete_jobs:
            chk.write(f"{job}.in\n")
    logging.info(f"Checkpoint file created: {checkpoint_file}")

    for sdfgz_file in sdfgz_files:
        dest_sdf_path = docking_results_dir / sdfgz_file.name.replace("_lib.sdfgz", ".sdf")
        copy_and_decompress_gz(sdfgz_file, dest_sdf_path)

    process_done_file = checkpoints_dir / "all_process_done.chk"
    with open(process_done_file, 'w') as done_file:
        done_file.write("All processes completed successfully.\n")
    logging.info(f"All processes completed. Final checkpoint created: {process_done_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python pipeline_step3.py config.json")
        exit(1)
    main(sys.argv[1])
