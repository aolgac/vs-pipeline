#!/usr/bin/env python3

import subprocess
import configparser
import pathlib
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def run_prepwizard(conf_file: str):
    cfg = configparser.ConfigParser()
    cfg.read(conf_file)

    inp_dir = pathlib.Path(cfg["receptors"]["input_dir"])
    out_dir = pathlib.Path(cfg["receptors"]["output_dir"])
    prepwizard = cfg["schrodinger"]["prepwizard"]

    out_dir.mkdir(parents=True, exist_ok=True)

    receptors = sorted(inp_dir.glob("*.pdb"))

    if not receptors:
        logging.error("No PDB files found.")
        sys.exit(1)

    for pdb in receptors:
        out_mae = out_dir / f"{pdb.stem}_prepared.mae"

        cmd = [
            prepwizard,
            "-WAIT",
            str(pdb),
            str(out_mae)
        ]

        logging.info(f"Preparing receptor: {pdb.name}")
        subprocess.run(cmd, check=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python 1_glide_prepare_receptors.py glide_receptor.conf")
        sys.exit(1)

    run_prepwizard(sys.argv[1])
