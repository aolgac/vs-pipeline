#!/usr/bin/env python3

import os
import sys
import time
import logging
import pathlib
import configparser
import pandas as pd
from pymol import cmd


def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )


def match_reference_to_poses(ref_dir, pose_dir):
    ref_files = [f for f in os.listdir(ref_dir) if f.endswith(".pdb")]
    pose_files = [f for f in os.listdir(pose_dir) if f.endswith(".mae")]

    matches = []

    for ref in ref_files:
        ref_id = ref.replace("_-_prepared", "").replace(".pdb", "")

        for pose in pose_files:
            pose_id = pose.replace("grid_", "").rsplit("_pv_ligand", 1)[0]
            if ref_id in pose_id:
                matches.append((ref, pose))

    return matches


def calculate_rmsd(ref_dir, pose_dir, output_csv):
    start = time.time()
    results = []

    pairs = match_reference_to_poses(ref_dir, pose_dir)
    logging.info(f"Total RMSD pairs: {len(pairs)}")

    for ref, pose in pairs:
        ref_path = os.path.join(ref_dir, ref)
        pose_path = os.path.join(pose_dir, pose)

        try:
            cmd.load(ref_path, "ref")
            cmd.load(pose_path, "pose")

            rmsd = cmd.rms_cur("pose", "ref", matchmaker=4)

            cmd.delete("ref")
            cmd.delete("pose")

            results.append({
                "Reference_Ligand": ref,
                "Pose_File": pose,
                "RMSD": rmsd
            })

            logging.info(f"RMSD OK | {ref} vs {pose} = {rmsd:.3f}")

        except Exception as e:
            logging.error(f"RMSD FAILED | {ref} vs {pose} | {e}")
            results.append({
                "Reference_Ligand": ref,
                "Pose_File": pose,
                "RMSD": "ERROR"
            })

    pd.DataFrame(results).to_csv(output_csv, index=False)
    logging.info(f"Finished in {time.time() - start:.2f}s")


def main(conf_file):
    cfg = configparser.ConfigParser()
    cfg.read(conf_file)

    ref_dir = cfg["input"]["reference_dir"]
    pose_dir = cfg["input"]["pose_dir"]
    output_csv = cfg["output"]["csv"]
    log_file = cfg["output"]["log"]

    setup_logging(log_file)

    calculate_rmsd(ref_dir, pose_dir, output_csv)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python 7_glide_rmsd_pymol.py glide_rmsd.conf")
        sys.exit(1)

    main(sys.argv[1])
