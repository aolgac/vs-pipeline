import os
import subprocess

ligands_dir = "ligands"
proteins_dir = "proteins"
output_dir = "results"
log_file = "flexx_crossdocking.log"

os.makedirs(output_dir, exist_ok=True)

default_ligand = "default_ligand.sdf"

with open(log_file, "w") as log:
    for protein in os.listdir(proteins_dir):
        if not protein.endswith(".pdb"):
            continue

        protein_id = os.path.splitext(protein)[0]
        ligand_name = f"{protein_id}_ligand.sdf"
        ligand_path = os.path.join(ligands_dir, ligand_name)

        if not os.path.exists(ligand_path):
            ligand_path = os.path.join(ligands_dir, default_ligand)

        output_path = os.path.join(output_dir, f"{protein_id}_docked.sdf")

        cmd = [
            "flexx",
            "-i", "all_ligands.sdf",
            "-o", output_path,
            "--protein", os.path.join(proteins_dir, protein),
            "--refligand", ligand_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        log.write(f"{protein}\n")
        log.write(" ".join(cmd) + "\n")
        log.write(result.stdout + "\n")
        log.write(result.stderr + "\n")
        log.write("-" * 80 + "\n")
