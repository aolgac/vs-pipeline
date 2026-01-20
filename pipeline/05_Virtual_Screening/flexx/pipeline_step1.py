import os
import glob
import json
import argparse
import subprocess
from rdkit import Chem
from concurrent.futures import ProcessPoolExecutor, as_completed

def load_config(config_path):
    with open(config_path, "r") as f:
        return json.load(f)

def checkpoint_path(step, checkpoint_dir, prefix):
    return os.path.join(checkpoint_dir, f"{step}_{prefix}.chk")

def convert_single_mae_to_sdf(mae_file, sdf_file):
    schrodinger = os.environ.get("SCHRODINGER")
    if not schrodinger:
        raise EnvironmentError("SCHRODINGER environment variable is not set.")
    cmd = [f"{schrodinger}/run", "structconvert.py", mae_file, sdf_file]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def merge_sdf_files(sdf_files, merged_file):
    writer = Chem.SDWriter(merged_file)
    for sdf_file in sdf_files:
        file_stem = os.path.splitext(os.path.basename(sdf_file))[0]
        suppl = Chem.SDMolSupplier(sdf_file)
        if suppl is None:
            print(f"Warning: could not read {sdf_file}")
            continue
        for mol in suppl:
            if mol is not None:
                mol.SetProp("_Name", file_stem)
                writer.write(mol)
    writer.close()

def main():
    parser = argparse.ArgumentParser(description="Convert MAE to SDF and merge them")
    parser.add_argument("-c", "--config", required=True, help="Path to JSON config file")
    args = parser.parse_args()
    config = load_config(args.config)

    input_mae_dir = config["input_mae_dir"]
    output_sdf_dir = config["output_sdf_dir"]
    merged_sdf_path = config["merged_sdf_path"]
    checkpoint_dir = config["checkpoint_dir"]
    checkpoint_prefix = config.get("checkpoint_prefix", "flexx")

    os.makedirs(output_sdf_dir, exist_ok=True)
    os.makedirs(checkpoint_dir, exist_ok=True)

    cp1 = checkpoint_path("mae_to_sdf", checkpoint_dir, checkpoint_prefix)
    cp2 = checkpoint_path("merge_sdf", checkpoint_dir, checkpoint_prefix)

    if not os.path.exists(cp1):
        mae_files = glob.glob(os.path.join(input_mae_dir, "*.mae"))
        print(f"Converting {len(mae_files)} MAE files to SDF using {os.cpu_count()} processes.")

        with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
            futures = {}
            for mae_file in mae_files:
                base = os.path.basename(mae_file).replace(".mae", ".sdf")
                sdf_file = os.path.join(output_sdf_dir, base)
                if os.path.exists(sdf_file):
                    continue
                futures[executor.submit(convert_single_mae_to_sdf, mae_file, sdf_file)] = mae_file

            for future in as_completed(futures):
                mae_file = futures[future]
                try:
                    success = future.result()
                    if not success:
                        print(f"Conversion failed: {mae_file}")
                except Exception as e:
                    print(f"Error converting {mae_file}: {e}")

        with open(cp1, "w") as f:
            f.write("done")
        print("MAE to SDF conversion completed.")
    else:
        print("MAE to SDF conversion skipped (checkpoint exists).")

    if not os.path.exists(cp2):
        sdf_files = glob.glob(os.path.join(output_sdf_dir, "*.sdf"))
        print(f"Merging {len(sdf_files)} SDF files into {merged_sdf_path}.")
        merge_sdf_files(sdf_files, merged_sdf_path)
        with open(cp2, "w") as f:
            f.write("done")
        print("Merge completed.")
    else:
        print("Merge step skipped (checkpoint exists).")

if __name__ == "__main__":
    main()
