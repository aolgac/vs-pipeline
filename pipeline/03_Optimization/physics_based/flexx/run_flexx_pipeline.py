import subprocess
import sys

steps = [
    ("1_run_flexx_crossdocking.py", "flexx_crossdock.conf"),
    ("2_split_flexx_sdf.py", "flexx_split.conf"),
    ("3_flexx_rmsd_pymol.py", "flexx_rmsd.conf"),
    ("4_flexx_rmsd_matrix_builder.py", "flexx_rmsd_matrix.conf"),
    ("5_flexx_rmsd_heatmap.py", "flexx_heatmap.conf"),
]

for script, conf in steps:
    cmd = ["python", script, conf]
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(f"Pipeline stopped at {script}")
