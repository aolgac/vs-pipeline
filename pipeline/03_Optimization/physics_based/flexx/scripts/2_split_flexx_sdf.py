import os
import json

def split_sdf(cfg):
    input_dir = cfg["input_sdf_dir"]

    for fname in os.listdir(input_dir):
        if not fname.endswith(".sdf"):
            continue

        base = os.path.splitext(fname)[0]
        out_dir = os.path.join(input_dir, base)
        os.makedirs(out_dir, exist_ok=True)

        with open(os.path.join(input_dir, fname)) as f:
            blocks = f.read().split("$$$$\n")

        for i, block in enumerate(blocks):
            block = block.strip()
            if not block:
                continue

            lines = block.splitlines()
            name = lines[0]

            if not name.endswith(cfg["required_suffix"]):
                continue

            safe = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in name)
            out = os.path.join(out_dir, f"{safe}.sdf")

            n = 1
            while os.path.exists(out):
                out = os.path.join(out_dir, f"{safe}_{n}.sdf")
                n += 1

            with open(out, "w") as o:
                o.write(block + "\n$$$$\n")

if __name__ == "__main__":
    with open("flexx_split.conf") as f:
        cfg = json.load(f)
    split_sdf(cfg)
