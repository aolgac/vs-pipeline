from pathlib import Path
import pandas as pd
import logging
import time
import sys
from pymol import cmd

logging.basicConfig(
    filename="vina_rmsd.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def load_config(cfg_path):
    cfg = {}
    with open(cfg_path) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                k, v = line.strip().split("=", 1)
                cfg[k.strip()] = v.strip()
    return cfg

def match_reference_to_poses(ref_dir, pose_dir):
    ref_files = list(ref_dir.glob("*.pdb"))
    pose_files = list(pose_dir.glob("*.pdbqt"))

    matches = []
    for ref in ref_files:
        ref_id = ref.stem.replace("_-_prepared", "")
        for pose in pose_files:
            pose_id = pose.stem.replace("_-_prepared_protein", "").replace("_-_prepared", "")
            if ref_id in pose_id:
                matches.append((ref, pose))
    return matches

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python vina_rmsd_reference_benchmark.py config.conf")

    cfg = load_config(sys.argv[1])

    ref_dir = Path(cfg["REFERENCE_DIR"])
    pose_dir = Path(cfg["POSE_DIR"])
    output_csv = Path(cfg["OUTPUT_CSV"])

    results = []
    start = time.time()

    pairs = match_reference_to_poses(ref_dir, pose_dir)
    logging.info(f"Total matched pairs: {len(pairs)}")

    for ref, pose in pairs:
        try:
            cmd.load(ref.as_posix(), "ref")
            cmd.load(pose.as_posix(), "pose")
            rmsd = cmd.rms_cur("pose", "ref", matchmaker=4)
            cmd.delete("all")

            results.append({
                "Reference": ref.name,
                "Pose": pose.name,
                "RMSD": rmsd
            })

            logging.info(f"{ref.name} vs {pose.name}: RMSD={rmsd:.3f}")

        except Exception as e:
            logging.error(f"Failed RMSD for {pose.name}: {e}")

    pd.DataFrame(results).to_csv(output_csv, index=False)
    logging.info(f"Finished in {time.time() - start:.2f} s")

if __name__ == "__main__":
    main()
