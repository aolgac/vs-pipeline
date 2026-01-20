#!/usr/bin/env python3

import os
import sys
import subprocess
import pathlib
import configparser
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def run_glide(script_path: pathlib.Path, glide_exec: str, host: str):
    cmd = [
        glide_exec,
        str(script_path),
        "-HOST", host
    ]

    try:
        subprocess.run(cmd, check=True)
        return f"OK: {script_path.name}"
    except subprocess.CalledProcessError as e:
        return f"FAIL: {script_path.name} ({e})"

def main(conf_file: str):
    cfg = configparser.ConfigParser()
    cfg.read(conf_file)

    script_dir  = pathlib.Path(cfg["glide"]["input_dir"])
    glide_exec  = cfg["glide"]["glide_exec"]
    host        = cfg["glide"]["host"]
    n_workers   = int(cfg["glide"]["threads"])

    scripts = sorted(script_dir.glob("*.in"))

    if not scripts:
        logging.error("No Glide input (.in) files found.")
        sys.exit(1)

    logging.info(f"Running {len(scripts)} Glide jobs with {n_workers} workers")

    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        futures = {
            executor.submit(run_glide, s, glide_exec, host): s
            for s in scripts
        }

        for future in as_completed(futures):
            logging.info(future.result())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python 5_glide_crossdocking_runner.py glide_crossdock.conf")
        sys.exit(1)

    main(sys.argv[1])
