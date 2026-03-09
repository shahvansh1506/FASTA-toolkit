# main.py — FASTA Toolkit (CLI Version)

# FASTA Toolkit - Command Line Version
# Author: Vansh Shah

# -------------------------------
# Function: Calculate GC Content
# -------------------------------

from utils import *

with open("sample.fasta","rb") as f:

    sequences = read_fasta(f)


for name, seq in sequences.items():

    print("Sequence:", name)

    print("Length:", len(seq))

    print("GC Content:", gc_content(seq))

    print("RNA:", transcribe_dna(seq))

    print("Reverse Complement:", reverse_complement(seq))

    print("Protein:", translate_dna(seq))

    print("ORFs:", find_orfs(seq))

    print("-----------------------")