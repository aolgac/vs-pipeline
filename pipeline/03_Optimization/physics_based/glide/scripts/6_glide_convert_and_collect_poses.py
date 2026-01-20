#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess
import logging
import pathlib
import configparser
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def convert_maegz(maegz_file, schrodinger_run, output_dir):
    out_file = output_dir / f"{maegz_file.stem}.mae"

    cmd = [
        schrodinger_run,
        "split_structure.py",
        "-m", "ligand",
        "-many_files",
        str(maegz_file),
        str(out_file)
    ]

    subprocess.run(cmd, check=True)

def collect_best_pose(ligand_dir, rmsd_dir):
    files = {f.name for f in ligand_dir.glob("*.mae")}

    for f in ligand_dir.glob("*.mae"):
        if "_pv_ligand" not in f.stem:
            continue

        base = f.stem.split("_pv_ligand")[0]
        cand2 = f"{base}_pv_ligand2.mae"
        cand1 = f"{base}_pv_ligand1.mae"

        selected = None
        if cand2 in files:
            selected = cand2
        elif cand1 in files:
            selected = cand1

        if selected:
            shutil.copy(
                ligand_dir / selected,
                rmsd_dir / selected
            )

def main(conf_file):
    cfg = configparser.ConfigParser()
    cfg.read(conf_file)

    maegz_dir = pathlib.Path(cfg["input"]["maegz_dir"])
    ligand_dir = pathlib.Path(cfg["output"]["ligand_dir"])
    rmsd_dir   = pathlib.Path(cfg["output"]["rmsd_dir"])
    sch_run    = cfg["schrodinger"]["run"]
    threads    = int(cfg["general"]["threads"])

    ligand_dir.mkdir(parents=True, exist_ok=True)
    rmsd_dir.mkdir(parents=True, exist_ok=True)

    maegz_files = list(maegz_dir.glob("*.maegz"))

    with ThreadPoolExecutor(max_workers=threads) as exe:
        exe.map(
            lambda f: convert_maegz(f, sch_run, ligand_dir),
            maegz_files
        )

    collect_best_pose(ligand_dir, rmsd_dir)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python 6_glide_convert_and_collect_poses.py glide_pose.conf")
        sys.exit(1)

    main(sys.argv[1])
