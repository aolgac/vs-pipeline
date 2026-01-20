import os
import pandas as pd
import logging
import time
from pymol import cmd
import configparser

config = configparser.ConfigParser()
config.read("config/diffdock_rmsd.conf")

ref_dir = config["paths"]["ref_dir"]
pose_dir = config["paths"]["pose_dir"]
output_file = config["paths"]["output_file"]

logging.basicConfig(
    filename="rmsd_calculation_df2.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def match_reference_to_poses(ref_dir, pose_dir):
    ref_files = [f for f in os.listdir(ref_dir) if f.endswith('.pdb')]
    pose_files = [f for f in os.listdir(pose_dir) if f.endswith('.sdf')]
    matches = {"Reference_Ligand": [], "Matching_Poses": []}

    for ref_file in ref_files:
        ref_core_id = ref_file.replace('_-_prepared', '').replace('.pdb', '')
        matching_poses = []
        for pose in pose_files:
            if '_-_prepared_' in pose:
                pose_core_id = pose.split('_-_prepared_')[-1].replace('.sdf', '')
            else:
                pose_core_id = ""
            if ref_core_id == pose_core_id:
                matching_poses.append(pose)
        matches["Reference_Ligand"].append(ref_file)
        matches["Matching_Poses"].append(", ".join(matching_poses) if matching_poses else "No Match")
    return pd.DataFrame(matches)

def calculate_rmsd_and_save(ref_dir, pose_dir, output_file):
    start_time = time.time()
    matches_df = match_reference_to_poses(ref_dir, pose_dir)
    results = []

    logging.info("Starting RMSD calculations.")
    for _, row in matches_df.iterrows():
        ref_ligand = row['Reference_Ligand']
        pose_files = row['Matching_Poses'].split(", ") if row['Matching_Poses'] != "No Match" else []
        ligand_start_time = time.time()

        if not pose_files:
            logging.warning(f"No matching poses found for reference ligand: {ref_ligand}")
            continue

        for pose_file in pose_files:
            reference_path = os.path.join(ref_dir, ref_ligand)
            pose_path = os.path.join(pose_dir, pose_file)
            try:
                cmd.load(reference_path, "reference")
                cmd.load(pose_path, "pose")
                rmsd = cmd.rms_cur("pose", "reference", matchmaker=4)
                cmd.delete("reference")
                cmd.delete("pose")
                logging.info(f"RMSD calculated for Reference: {ref_ligand}, Pose: {pose_file}, RMSD: {rmsd}")
                results.append({"Reference_Ligand": ref_ligand, "Pose_File": pose_file, "RMSD": rmsd})
            except Exception as e:
                logging.error(f"Error calculating RMSD for Reference: {ref_ligand}, Pose: {pose_file}. Error: {e}")
                results.append({"Reference_Ligand": ref_ligand, "Pose_File": pose_file, "RMSD": f"Error: {e}"})

        ligand_elapsed_time = time.time() - ligand_start_time
        logging.info(f"Elapsed time for {ref_ligand}: {ligand_elapsed_time:.2f} seconds.")

    pd.DataFrame(results).to_csv(output_file, index=False)
    logging.info(f"Total elapsed time: {time.time() - start_time:.2f} seconds.")
    logging.info("RMSD calculations completed.")

calculate_rmsd_and_save(ref_dir, pose_dir, output_file)
