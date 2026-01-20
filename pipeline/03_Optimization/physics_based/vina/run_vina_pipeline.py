import subprocess
import sys

pipeline_steps = [
    ("1_prepare_receptors_pdb_to_pdbqt.py", "configs/vina_receptor.conf.example"),
    ("2_convert_ligands_mae_to_pdbqt.py", "configs/vina_ligand.conf.example"),
    ("3_run_vina_crossdocking.py", "configs/vina_docking.conf.example"),
    ("4_extract_vina_model1.py", "configs/model1_extraction.conf.example"),
    ("5_vina_rmsd_pymol.py", "configs/vina_rmsd.conf.example"),
    ("6_vina_rmsd_matrix_builder.py", "configs/rmsd_matrix.conf.example"),
    ("7_vina_rmsd_heatmap.py", "configs/heatmap.conf.example")
]

for script, conf in pipeline_steps:
    print(f"Running {script} with {conf}...")
    subprocess.run([sys.executable, f"scripts/{script}", conf], check=True)
