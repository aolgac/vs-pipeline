import os
import pandas as pd
import configparser

# Read configuration
config = configparser.ConfigParser()
config.read("diffdock_filepaths.conf")

input_directory = config["DEFAULT"]["input_directory"]
output_csv = config["DEFAULT"]["output_csv"]

def generate_file_paths_csv(directory, output_csv):
    pdb_files = []
    sdf_mol2_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.pdb'):
                pdb_files.append(file_path)
            elif file.endswith('.sdf') or file.endswith('.mol2'):
                sdf_mol2_files.append(file_path)

    pdb_files.sort()
    sdf_mol2_files.sort()

    print(f"Number of .pdb files found: {len(pdb_files)}")
    print(f"Number of .sdf/.mol2 files found: {len(sdf_mol2_files)}")
    print(f"Number of complexes must be: {len(pdb_files) * len(sdf_mol2_files)}")

    complex_name = []
    protein_path = []
    ligand_description = []
    protein_sequence = []

    for protein_file in pdb_files:
        protein_base = os.path.basename(protein_file).split('.')[0]
        for ligand_file in sdf_mol2_files:
            ligand_base = os.path.basename(ligand_file).split('.')[0]
            complex_name.append(f"{protein_base}_{ligand_base}")
            protein_path.append(protein_file)
            ligand_description.append(ligand_file)
            protein_sequence.append(None)

    df = pd.DataFrame({
        'complex_name': complex_name,
        'protein_path': protein_path,
        'ligand_description': ligand_description,
        'protein_sequence': protein_sequence
    })

    df.to_csv(output_csv, index=False)
    print(f"'{output_csv}' has been generated for DiffDock with {len(df)} complexes.")

if __name__ == "__main__":
    generate_file_paths_csv(input_directory, output_csv)
