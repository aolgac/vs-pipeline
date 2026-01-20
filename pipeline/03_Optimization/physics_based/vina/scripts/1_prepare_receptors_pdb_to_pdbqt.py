import subprocess
from pathlib import Path
import sys

def load_config(cfg_path):
    cfg = {}
    with open(cfg_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            k, v = line.split("=", 1)
            cfg[k.strip()] = v.strip()
    return cfg

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python prepare_receptors_pdb_to_pdbqt.py config.conf")

    cfg = load_config(sys.argv[1])

    pdb_dir = Path(cfg["PDB_DIR"])
    pythonsh = cfg["MGLTOOLS_PYTHONSH"]
    prepare_script = cfg["PREPARE_RECEPTOR_SCRIPT"]

    for pdb_file in pdb_dir.glob("*.pdb"):
        out_file = pdb_file.with_suffix(".pdbqt")
        subprocess.run(
            [pythonsh, prepare_script, "-r", str(pdb_file), "-o", str(out_file)],
            check=True
        )
        print(f"Processed {pdb_file.name} -> {out_file.name}")

if __name__ == "__main__":
    main()
