import os
import subprocess
import importlib.util

config_path = os.path.join(os.path.dirname(__file__), "../config/gnina_crossdock.conf")
spec = importlib.util.spec_from_file_location("conf", config_path)
conf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(conf)

os.makedirs(conf.output_folder, exist_ok=True)
os.makedirs(os.path.dirname(conf.log_file), exist_ok=True)

ligand_files = [f for f in os.listdir(conf.ligands_folder) if f.endswith(".sdf")]

with open(conf.log_file, "w") as log:
    for protein_file in os.listdir(conf.proteins_folder):
        if protein_file.endswith(".pdb"):
            protein_base = os.path.splitext(protein_file)[0]
            ligand_file = f"{protein_base}_ligand.sdf"
            ligand_path = os.path.join(conf.ligands_folder, ligand_file)

            if not os.path.exists(ligand_path):
                ligand_path = os.path.join(conf.ligands_folder, conf.default_ligand)

            output_path = os.path.join(conf.output_folder, f"{protein_base}_{os.path.splitext(os.path.basename(ligand_path))[0]}.sdf")

            command = [
                "gnina",
                "-r", os.path.join(conf.proteins_folder, protein_file),
                "-l", ligand_path,
                "--autobox_ligand", ligand_path,
                "-o", output_path,
                "--seed", str(conf.seed)
            ]

            result = subprocess.run(command, capture_output=True, text=True)

            log.write(f"Docking results for {protein_file} with {os.path.basename(ligand_path)}:\n")
            log.write(f"Command: {' '.join(command)}\n")
            log.write(f"Standard Output:\n{result.stdout}\n")
            log.write(f"Standard Error:\n{result.stderr}\n")
            log.write("\n" + "="*80 + "\n\n")

print(f"Docking results have been logged to {conf.log_file}")
