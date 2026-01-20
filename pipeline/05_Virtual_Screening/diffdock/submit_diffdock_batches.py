import os
import time
import subprocess
import json
import logging
import argparse


def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)


def submit_and_monitor_jobs(config_dir, pipeline_script, poll_interval, cooldown):
    config_files = sorted(
        [
            os.path.join(config_dir, f)
            for f in os.listdir(config_dir)
            if f.endswith(".json")
        ]
    )

    for config_path in config_files:
        logging.info(f"Processing config: {config_path}")

        try:
            with open(config_path) as f:
                config = json.load(f)

            slurm_dir = config.get("slurm_dir")
            job_script = config.get("slurm_script_name", "diffdock_job.sh")

            if not slurm_dir:
                raise ValueError("Missing 'slurm_dir' in config")

            slurm_script_path = os.path.join(slurm_dir, job_script)

            # Step 1: generate SLURM script
            logging.info("Generating SLURM script via DiffDock pipeline")
            subprocess.run(
                ["python", pipeline_script, "--config", config_path],
                check=True
            )

            if not os.path.exists(slurm_script_path):
                raise FileNotFoundError(f"SLURM script not found: {slurm_script_path}")

            # Step 2: submit job
            logging.info(f"Submitting job: {slurm_script_path}")
            result = subprocess.run(
                ["sbatch", "--parsable", slurm_script_path],
                stdout=subprocess.PIPE,
                text=True,
                check=True
            )

            job_id = result.stdout.strip()
            logging.info(f"Submitted job {job_id}")

            # Step 3: monitor job
            while True:
                status = subprocess.run(
                    ["squeue", "-j", job_id, "-h"],
                    stdout=subprocess.PIPE,
                    text=True
                )

                if status.stdout.strip() == "":
                    break

                logging.info(f"Job {job_id} running. Rechecking in {poll_interval}s.")
                time.sleep(poll_interval)

            logging.info(f"Job {job_id} completed. Cooling down for {cooldown}s.")
            time.sleep(cooldown)

        except Exception as e:
            logging.error(f"Error processing {config_path}: {e}", exc_info=True)

    logging.info("All DiffDock jobs completed.")


def main():
    parser = argparse.ArgumentParser(description="Submit and monitor DiffDock SLURM jobs")
    parser.add_argument("--config_dir", required=True, help="Directory containing DiffDock config JSON files")
    parser.add_argument("--pipeline_script", default="vs_diffdock_pipeline.py")
    parser.add_argument("--log_file", default="submission.log")
    parser.add_argument("--poll_interval", type=int, default=300)
    parser.add_argument("--cooldown", type=int, default=30)

    args = parser.parse_args()
    setup_logging(args.log_file)

    submit_and_monitor_jobs(
        args.config_dir,
        args.pipeline_script,
        args.poll_interval,
        args.cooldown
    )


if __name__ == "__main__":
    main()
