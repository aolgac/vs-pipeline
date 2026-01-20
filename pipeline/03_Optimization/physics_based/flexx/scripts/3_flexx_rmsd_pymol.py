import os
import json
import pandas as pd
import logging
import time
from pymol import cmd

logging.basicConfig(
    filename="flexx_rmsd.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def match_refs(cfg):
    refs = [f for f in os.listdir(cfg["ref_dir"]) if f.endswith(cfg["ref_ext"])]
    poses = [f for f in os.listdir(cfg["pose_dir"]) if f.endswith(cfg["pose_ext"])]

    out = []
    for r in refs:
        core = r.replace(cfg["ref_strip"], "").replace(cfg["ref_ext"], "")
        for p in poses:
            pid = p.split(cfg["pose_split"])[-1].rsplit(cfg["pose_trim"], 1)[0]
            if core in pid:
                out.append((r, p))
    return out

def run_rmsd(cfg):
    results = []
    start = time.time()

    for ref, pose in match_refs(cfg):
        try:
            cmd.load(os.path.join(cfg["ref_dir"], ref), "ref")
            cmd.load(os.path.join(cfg["pose_dir"], pose), "pose")
            rmsd = cmd.rms_cur("pose", "ref", matchmaker=4)
            cmd.delete("ref")
            cmd.delete("pose")
            results.append({"Reference": ref, "Pose": pose, "RMSD": rmsd})
        except Exception as e:
            results.append({"Reference": ref, "Pose": pose, "RMSD": f"ERR:{e}"})

    pd.DataFrame(results).to_csv(cfg["output_csv"], index=False)
    logging.info(f"Finished in {time.time() - start:.2f}s")

if __name__ == "__main__":
    with open("flexx_rmsd.conf") as f:
        cfg = json.load(f)
    run_rmsd(cfg)
