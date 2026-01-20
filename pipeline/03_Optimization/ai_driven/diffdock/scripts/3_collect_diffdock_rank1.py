import os
import shutil
import configparser

config = configparser.ConfigParser()
config.read("config/diffdock_collect.conf")

base_dir = config["DEFAULT"]["base_dir"]
dest_dir = config["DEFAULT"]["dest_dir"]

os.makedirs(dest_dir, exist_ok=True)

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file == "rank1.sdf":
            source_path = os.path.join(root, file)
            dir_name = os.path.basename(os.path.dirname(source_path))
            dest_file_name = f"{dir_name}.sdf"
            dest_path = os.path.join(dest_dir, dest_file_name)
            shutil.copyfile(source_path, dest_path)
            print(f"Copied {source_path} to {dest_path}")
