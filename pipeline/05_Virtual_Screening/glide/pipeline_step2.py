import os
import time
import logging
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import json

def setup_logging(log_path):
    logging.basicConfig(
        filename=log_path,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='a'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def run_glide(script_path, glide_path):
    cmd = f"{glide_path} -HOST localhost {script_path}"
    logging.info(f"Starting: {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True)
        logging.info(f"Finished successfully: {script_path}")
        return script_path, True
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed: {script_path} with error: {e}")
        return script_path, False

def main(config_path, max_parallel=24):
    with open(config_path) as f:
        config = json.load(f)

    input_scripts_dir = Path(config["input_scripts_dir"])
    os.chdir(input_scripts_dir)
    log_file = Path(config["log_dir"]) / "pipeline_step2.log"
    checkpoint_file = Path(config["checkpoints_dir"]) / "submitted_all_in_files.chk"
    glide_path = config.get("glide_path", "glide")

    setup_logging(str(log_file))

    input_scripts = sorted(input_scripts_dir.glob("*.in"))
    completed_jobs = set()
    if checkpoint_file.exists():
        with checkpoint_file.open("r") as f:
            completed_jobs = set(line.strip() for line in f if line.strip())

    scripts_to_process = [script for script in input_scripts if script.name not in completed_jobs]
    if not scripts_to_process:
        logging.info("No new jobs to process. All jobs are submitted.")
        return

    batch_wait = 30
    for i in range(0, len(scripts_to_process), max_parallel):
        batch = scripts_to_process[i:i + max_parallel]
        logging.info(f"Processing batch {i // max_parallel + 1} with {len(batch)} jobs.")

        with ThreadPoolExecutor(max_workers=max_parallel) as executor:
            futures = {executor.submit(run_glide, script, glide_path): script for script in batch}

            for future in as_completed(futures):
                script_path, success = future.result()
                if success:
                    with checkpoint_file.open("a") as f:
                        f.write(f"{script_path.name}\n")
                else:
                    logging.error(f"Failed: {script_path}")

        logging.info(f"Batch {i // max_parallel + 1} completed. Waiting {batch_wait} seconds.")
        time.sleep(batch_wait)

    logging.info("All batches processed.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run Glide docking in parallel batches.")
    parser.add_argument("config", help="Path to JSON config file")
    parser.add_argument("--max_parallel", default=24, type=int, help="Max parallel jobs")
    args = parser.parse_args()

    main(args.config, args.max_parallel)
