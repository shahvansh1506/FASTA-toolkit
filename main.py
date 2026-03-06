def read_fasta(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    sequence = ""
    for line in lines:
        if not line.startswith(">"):
            sequence += line.strip()

    return sequence


def gc_content(seq):
    g = seq.count("G")
    c = seq.count("C")
    return (g + c) / len(seq) * 100


def reverse_complement(seq):
    complement = {"A":"T","T":"A","G":"C","C":"G"}
    rev = ""

    for base in seq[::-1]:
        rev += complement.get(base, base)

    return rev


def dna_to_rna(seq):
    return seq.replace("T","U")


file = "sample.fasta"

sequence = read_fasta(file)

print("Sequence:", sequence)
print("Length:", len(sequence))
print("GC Content:", gc_content(sequence))
print("Reverse Complement:", reverse_complement(sequence))
print("RNA:", dna_to_rna(sequence))