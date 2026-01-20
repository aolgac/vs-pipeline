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

def run_ligprep(conf_file: str):
    cfg = configparser.ConfigParser()
    cfg.read(conf_file)

    inp_dir = pathlib.Path(cfg["ligands"]["input_dir"])
    out_dir = pathlib.Path(cfg["ligands"]["output_dir"])
    ligprep = cfg["schrodinger"]["ligprep"]

    out_dir.mkdir(parents=True, exist_ok=True)

    ligands = sorted(inp_dir.glob("*.sdf"))

    if not ligands:
        logging.error("No ligand files found.")
        sys.exit(1)

    for sdf in ligands:
        out_mae = out_dir / f"{sdf.stem}_ligprep.mae"

        cmd = [
            ligprep,
            "-WAIT",
            "-i", str(sdf),
            "-o", str(out_mae)
        ]

        logging.info(f"Preparing ligand: {sdf.name}")
        subprocess.run(cmd, check=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python 2_glide_prepare_ligands.py glide_ligand.conf")
        sys.exit(1)

    run_ligprep(sys.argv[1])
