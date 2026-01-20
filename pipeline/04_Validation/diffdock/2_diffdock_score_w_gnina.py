import os
import subprocess
import time
import yaml

with open("diffdock_gnina_score.conf.example", "r") as f:
    config = yaml.safe_load(f)

res_dir = config["protein_dir"]
lig_dir = config["ligand_dir"]
out_dir = config["log_dir"]
results_dir = config["results_dir"]
seed = config.get("seed", 12345)
minimize = config.get("minimize", True)

os.makedirs(out_dir, exist_ok=True)
os.makedirs(results_dir, exist_ok=True)

protein_files = sorted([os.path.join(res_dir, f) for f in os.listdir(res_dir) if f.endswith('.pdb')])
ligand_files = sorted([os.path.join(lig_dir, f) for f in os.listdir(lig_dir) if f.endswith('.sdf')])

if not protein_files or not ligand_files:
    raise FileNotFoundError("No protein or ligand files found in the specified directories.")

for protein_file in protein_files:
    protein_base = os.path.basename(protein_file).split('.')[0]

    for ligand_file in ligand_files:
        ligand_base = os.path.basename(ligand_file).split('.')[0]
        start_time = time.time()
        output_file = os.path.join(results_dir, f"{protein_base}_{ligand_base}.sdf.gz")

        cmd = [
            "gnina",
            "-r", protein_file,
            "-l", ligand_file,
            "-o", output_file,
            "--seed", str(seed)
        ]

        if minimize:
            cmd.append("--minimize")

        try:
            subprocess.run(cmd, check=True)
            elapsed_time = time.time() - start_time
            print(f"Docking completed for Protein: {protein_base}, Ligand: {ligand_base} in {elapsed_time:.2f}s")

            log_file = os.path.join(out_dir, f"gnina_{protein_base}_{ligand_base}.out")
            with open(log_file, 'a') as log:
                log.write(f"Completed in {elapsed_time:.2f}s\n")

        except subprocess.CalledProcessError as e:
            print(f"Error during GNINA docking: Protein {protein_base}, Ligand {ligand_base}")
            err_file = os.path.join(out_dir, f"gnina_{protein_base}_{ligand_base}.err")
            with open(err_file, 'a') as err_log:
                err_log.write(str(e) + "\n")
