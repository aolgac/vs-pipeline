import argparse
import json
import subprocess
import os
from pathlib import Path
import logging

def setup_master_logging(log_path):
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

def run_script(command, log_file):
    logging.info(f"Running: {' '.join(command)}")
    with open(log_file, 'a') as lf:
        process = subprocess.Popen(command, stdout=lf, stderr=lf)
        process.wait()
    if process.returncode == 0:
        logging.info(f"Finished successfully: {command[1]}")
    else:
        logging.error(f"Failed: {command[1]} with return code {process.returncode}")
    return process.returncode

def main(config_path, max_parallel):
    with open(config_path) as f:
        config = json.load(f)

    repo_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = Path(config['log_dir'])
    log_dir.mkdir(parents=True, exist_ok=True)
    master_log = log_dir / "master.log"
    setup_master_logging(master_log)

    logging.info("Master script started.")
    logging.info(f"Config file: {config_path}")
    logging.info(f"Max parallel jobs for pipeline_step2: {max_parallel}")
    step1_script = os.path.join(repo_dir, config["step_scripts"]["step1"])
    step2_script = os.path.join(repo_dir, config["step_scripts"]["step2"])
    step3_script = os.path.join(repo_dir, config["step_scripts"]["step3"])

    ret1 = run_script(["python3", step1_script, config_path], log_dir / "pipeline_step1.log")
    if ret1 != 0: return logging.error("Step 1 failed, aborting.")

    input_scripts_dir = config.get("input_scripts_dir", ".")
    os.chdir(input_scripts_dir)
    logging.info(f"Changed working directory to: {os.getcwd()}")
    ret2 = run_script(["python3", step2_script, config_path, "--max_parallel", str(max_parallel)], log_dir / "pipeline_step2.log")
    if ret2 != 0: return logging.error("Step 2 failed, aborting.")

    ret3 = run_script(["python3", step3_script, config_path], log_dir / "pipeline_step3.log")
    if ret3 != 0: return logging.error("Step 3 failed, aborting.")

    logging.info("All steps completed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Master script to run Glide pipeline steps sequentially.")
    parser.add_argument("config", help="Path to JSON config file")
    parser.add_argument("--max_parallel", default=24, type=int, help="Max parallel jobs for pipeline_step2.py")
    args = parser.parse_args()

    main(args.config, args.max_parallel)
