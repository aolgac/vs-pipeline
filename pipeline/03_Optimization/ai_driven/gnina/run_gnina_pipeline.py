import subprocess
import os

base_dir = os.path.dirname(__file__)
scripts_dir = os.path.join(base_dir, "scripts")
config_dir = os.path.join(base_dir, "config")

pipeline_steps = [
    ("1_gnina_crossdock.py", "gnina_crossdock.conf"),
    ("2_extract_first_pose.py", "gnina_extract_first_pose.conf"),
    ("3_gnina_rmsd.py", "gnina_rmsd.conf"),
    ("4_gnina_rmsd_matrix.py", "gnina_rmsd_matrix.conf"),
    ("6_gnina_rmsd_heatmap.py", "gnina_heatmap.conf")
]

for script_name, conf_name in pipeline_steps:
    script_path = os.path.join(scripts_dir, script_name)
    conf_path = os.path.join(config_dir, conf_name)

    print(f"Running {script_name} with {conf_name}")
    try:
        subprocess.run(["python3", script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
        break

print("GNINA pipeline completed!")
