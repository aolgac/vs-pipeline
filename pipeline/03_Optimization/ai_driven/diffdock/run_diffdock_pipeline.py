import subprocess

pipeline_steps = [
    ("1_generate_diffdock_csv.py", "diffdock_filepaths.conf.py"),
    ("2_run_diffdock_inference.py", "diffdock_inference.conf.py"),
    ("3_collect_diffdock_rank1.py", "diffdock_collect.conf.py"),
    ("4_diffdock_rmsd_pymol.py", "diffdock_rmsd.conf.py"),
    ("5_diffdock_rmsd_matrix_builder.py", "diffdock_rmsd_matrix.conf.py"),
    ("6_diffdock_rmsd_heatmap.py", "diffdock_heatmap.conf.py"),
]

for script, conf_file in pipeline_steps:
    print(f"Running {script} with {conf_file}")
    subprocess.run(["python3", script], check=True)