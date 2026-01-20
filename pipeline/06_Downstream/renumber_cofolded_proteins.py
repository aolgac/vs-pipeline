#!/usr/bin/env python3

import os
import argparse
from Bio import SeqIO, pairwise2
from Bio.PDB import PDBParser, PDBIO

AA3TO1 = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C",
    "GLN": "Q", "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I",
    "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P",
    "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V"
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Renumber co-folding PDB structures using a reference FASTA sequence"
    )
    parser.add_argument(
        "--fasta",
        required=True,
        help="Reference FASTA file"
    )
    parser.add_argument(
        "--pdb_dir",
        required=True,
        help="Directory containing input PDB files"
    )
    parser.add_argument(
        "--out_dir",
        required=True,
        help="Directory to write renumbered PDB files"
    )
    return parser.parse_args()


def renumber_structure(structure, fasta_seq):
    model = structure[0]

    for chain in model:
        residues = []
        pdb_seq = ""

        for res in chain:
            if res.id[0] != " ":
                continue
            residues.append(res)
            pdb_seq += AA3TO1.get(res.resname, "X")

        if not pdb_seq:
            continue

        alignment = pairwise2.align.globalxx(
            pdb_seq,
            fasta_seq,
            one_alignment_only=True
        )

        if not alignment:
            continue

        pdb_aln, fasta_aln = alignment[0].seqA, alignment[0].seqB

        fasta_pos = 1
        res_idx = 0

        for p_char, f_char in zip(pdb_aln, fasta_aln):
            if f_char != "-":
                if p_char != "-":
                    old_id = residues[res_idx].id
                    residues[res_idx].id = (old_id[0], fasta_pos, old_id[2])
                    res_idx += 1
                fasta_pos += 1
            else:
                if p_char != "-":
                    old_id = residues[res_idx].id
                    residues[res_idx].id = (old_id[0], fasta_pos, old_id[2])
                    res_idx += 1


def main():
    args = parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    fasta_seq = str(next(SeqIO.parse(args.fasta, "fasta")).seq)

    parser = PDBParser(QUIET=True)
    io = PDBIO()

    for fname in os.listdir(args.pdb_dir):
        if not fname.endswith(".pdb"):
            continue

        pdb_path = os.path.join(args.pdb_dir, fname)
        structure = parser.get_structure("structure", pdb_path)

        renumber_structure(structure, fasta_seq)

        io.set_structure(structure)
        io.save(os.path.join(args.out_dir, fname))


if __name__ == "__main__":
    main()
