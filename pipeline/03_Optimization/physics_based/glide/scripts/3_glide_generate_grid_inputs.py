#!/usr/bin/env python3

import os
import sys
import pathlib
import configparser
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def write_grid_input(receptor_file, grid_name, grid_center, output_dir):
    content = f"""
FORCEFIELD   OPLS4
GRID_CENTER  {grid_center}
RECEP_FILE   {receptor_file}
GRIDFILE     {grid_name}
""".strip()

    output_file = output_dir / f"glide_{grid_name.replace('.zip','')}.in"

    with open(output_file, "w") as f:
        f.write(content)

    logging.info(f"Grid input written: {output_file.name}")

def generate_grid_inputs(conf_file: str):
    cfg = configparser.ConfigParser()
    cfg.read(conf_file)

    receptor_dir = pathlib.Path(cfg["grid"]["receptor_dir"])
    output_dir   = pathlib.Path(cfg["grid"]["output_dir"])
    grid_center  = cfg["grid"]["grid_center"]

    output_dir.mkdir(parents=True, exist_ok=True)

    receptors = sorted(
        p for p in receptor_dir.iterdir()
        if p.suffix in {".mae", ".maegz"}
    )

    if not receptors:
        logging.error("No receptor files found.")
        sys.exit(1)

    for receptor in receptors:
        base = receptor.stem.split("_-_")[0]
        grid_name = f"grid_{base}.zip"

        write_grid_input(
            receptor_file=receptor,
            grid_name=grid_name,
            grid_center=grid_center,
            output_dir=output_dir
        )

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python 3_glide_generate_grid_inputs.py glide_grid.conf")
        sys.exit(1)

    generate_grid_inputs(sys.argv[1])
