#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

# (script, config)
PIPELINE_STEPS = [
    ("1_glide_prepare_receptors.py", "glide_receptor.conf"),
    ("2_glide_prepare_ligands.py", "glide_ligand.conf"),
    ("3_glide_generate_grid_inputs.py", "glide_grid.conf"),
    ("4_glide_run_grids.py", "glide_run.conf"),
    ("5_glide_crossdocking_runner.py", "glide_crossdock.conf"),
    ("6_glide_convert_and_collect_poses.py", "glide_pose.conf"),
    ("7_glide_rmsd_pymol.py", "glide_rmsd.conf"),
    ("8_glide_rmsd_matrix_builder.py", "rmsd_matrix.conf"),
    ("9_glide_rmsd_heatmap.py", "heatmap.conf"),
]


def run_step(script, config):
    cmd = ["python", script, str(Path("../config") / config)]

    print(f"\n>>> Running: {' '.join(cmd)}")

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print(f"\nERROR: Step failed -> {script}")
        sys.exit(1)


def main():
    scripts_dir = Path.cwd()
    config_dir = scripts_dir.parent / "config"

    print("=== Glide Cross-Docking Pipeline ===")
    print("Environment: vs-pipeline must be activated\n")

    for script, config in PIPELINE_STEPS:
        script_path = scripts_dir / script
        config_path = config_dir / config

        if not script_path.exists():
            print(f"ERROR: Missing script: {script}")
            sys.exit(1)

        if not config_path.exists():
            print(f"ERROR: Missing config: {config}")
            sys.exit(1)

        run_step(script, config)

    print("\n=== Glide pipeline completed successfully ===")


if __name__ == "__main__":
    main()
