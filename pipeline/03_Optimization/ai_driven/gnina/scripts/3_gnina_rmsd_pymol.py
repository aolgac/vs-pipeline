import os
import pandas as pd
import logging
import time
from pymol import cmd
import importlib.util

config_path = os.path.join(os.path.dirname(__file__), "../config/gnina_rmsd.conf")
spec = importlib.util.spec_from_file_location("conf", config_path)
conf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(conf)

os.makedirs(os.path.dirname(conf.output_file), exist_ok=True)
os.makedirs(os.path.dirname(conf.log_file), exist_ok=True)

logging.basicConfig(
    filename=conf.log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def match_reference_to_poses(ref_dir, pose_dir):
    ref_files = [f for f in os.listdir(ref_dir) if f.endswith('.sdf')]
    pose_files = [f for f in os.listdir(pose_dir) if f.endswith('.sdf')]
    matches = {"Reference_Ligand": [], "Matching_Poses": []}

    for ref_file in ref_files:
        ref_core_id = ref_file.replace('.sdf', '')
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
                logging.info(f"RMSD calculated: Reference={ref_ligand}, Pose={pose_file}, RMSD={rmsd}")
                results.append({"Reference_Ligand": ref_ligand, "Pose_File": pose_file, "RMSD": rmsd})
            except Exception as e:
                logging.error(f"Error calculating RMSD: Reference={ref_ligand}, Pose={pose_file}, Error={e}")
                results.append({"Reference_Ligand": ref_ligand, "Pose_File": pose_file, "RMSD": f"Error: {e}"})

    pd.DataFrame(results).to_csv(output_file, index=False)
    logging.info(f"Total RMSD calculation time: {time.time() - start_time:.2f} seconds.")
    logging.info("RMSD calculations completed.")

calculate_rmsd_and_save(conf.ref_dir, conf.pose_dir, conf.output_file)
