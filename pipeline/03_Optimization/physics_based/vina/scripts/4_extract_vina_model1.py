from pathlib import Path
import sys

def extract_model1(in_file: Path, out_file: Path):
    with in_file.open() as fin, out_file.open("w") as fout:
        write = False
        for line in fin:
            if line.startswith("MODEL 1"):
                write = True
            if write:
                fout.write(line)
            if line.startswith("ENDMDL"):
                break

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python extract_vina_model1.py config.conf")

    cfg = {}
    with open(sys.argv[1]) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                k, v = line.strip().split("=", 1)
                cfg[k] = v

    in_dir = Path(cfg["INPUT_DIR"])
    out_dir = Path(cfg["OUTPUT_DIR"])
    out_dir.mkdir(exist_ok=True)

    for pdbqt in in_dir.glob("*.pdbqt"):
        extract_model1(pdbqt, out_dir / pdbqt.name)

    print("MODEL 1 extraction finished.")

if __name__ == "__main__":
    main()
