import os
import argparse
import json
import csv
from rdkit import Chem

def get_biosolveit_score(mol):
    for key in mol.GetPropNames():
        if "BIOSOLVEIT.DOCKING_SCORE" in key:
            return mol.GetProp(key)
    return "NA"

def filter_and_save_individual_poses(config):
    prefix = config["checkpoint_prefix"]
    checkpoint_dir = config["checkpoint_dir"]
    docking_output_dir = config["docking_output_dir"]
    output_base_dir = config["output_base_dir"]

    docking_output_sdf = os.path.join(output_base_dir, f"{prefix}_flexx_docked.sdf")

    os.makedirs(docking_output_dir, exist_ok=True)
    os.makedirs(checkpoint_dir, exist_ok=True)
    os.makedirs(output_base_dir, exist_ok=True)

    checkpoint_filter = os.path.join(checkpoint_dir, f"filter_poses_{prefix}.chk")
    checkpoint_csv = os.path.join(checkpoint_dir, f"csv_creation_{prefix}.chk")
    csv_path = os.path.join(output_base_dir, f"{prefix}_flexx_results.csv")

    if not os.path.exists(checkpoint_filter):
        suppl = Chem.SDMolSupplier(docking_output_sdf)
        if suppl is None:
            raise FileNotFoundError(f"Cannot open docked SDF file: {docking_output_sdf}")

        results = []
        for mol in suppl:
            if mol is None:
                continue
            name = mol.GetProp("_Name") if mol.HasProp("_Name") else ""
            if name.endswith("_01"):
                filename = f"{prefix}_{name}.sdf"
                filepath = os.path.join(docking_output_dir, filename)

                writer = Chem.SDWriter(filepath)
                writer.write(mol)
                writer.close()

                docking_score = get_biosolveit_score(mol)
                results.append((filename, docking_score))

        config["_results"] = results
        with open(checkpoint_filter, "w") as f:
            f.write("done")
        print(f"Saved {len(results)} _01 poses to {docking_output_dir}")
    else:
        print(f"Filtering checkpoint exists, skipping filtering: {checkpoint_filter}")

    if not os.path.exists(checkpoint_csv):
        results = config.get("_results")
        if results is None:
            results = []
            for fname in os.listdir(docking_output_dir):
                if fname.endswith(".sdf") and fname.startswith(prefix):
                    path = os.path.join(docking_output_dir, fname)
                    suppl = Chem.SDMolSupplier(path)
                    mol = next(iter(suppl), None)
                    if mol:
                        results.append((fname, get_biosolveit_score(mol)))

        with open(csv_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["filename", "docking_score"])
            writer.writerows(results)

        with open(checkpoint_csv, "w") as f:
            f.write("done")
        print(f"Docking scores saved to CSV: {csv_path}")
    else:
        print(f"CSV creation checkpoint exists, skipping CSV generation: {checkpoint_csv}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", required=True, help="Path to JSON config file")
    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)

    filter_and_save_individual_poses(config)

if __name__ == "__main__":
    main()
