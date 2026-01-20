#!/usr/bin/env python3

import os
import sys
import subprocess
import pathlib
import configparser
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def run_glide_jobs(conf_file: str):
    cfg = configparser.ConfigParser()
    cfg.read(conf_file)

    script_dir = pathlib.Path(cfg["glide"]["input_dir"])
    glide_exec = cfg["glide"]["glide_exec"]
    host       = cfg["glide"]["host"]

    if not script_dir.exists():
        logging.error(f"Input directory not found: {script_dir}")
        sys.exit(1)

    scripts = sorted(script_dir.glob("*.in"))

    if not scripts:
        logging.error("No Glide input (.in) files found.")
        sys.exit(1)

    for script in scripts:
        cmd = [
            glide_exec,
            str(script),
            "-HOST", host
        ]

        logging.info(f"Running Glide: {script.name}")
        subprocess.run(cmd, check=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python 4_glide_run_grids.py glide_run.conf")
        sys.exit(1)

    run_glide_jobs(sys.argv[1])
