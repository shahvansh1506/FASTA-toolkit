def gc_content(sequence):
    g = sequence.count("G")
    c = sequence.count("C")
    return round((g + c) / len(sequence) * 100, 2)


def reverse_complement(sequence):
    complement = {"A":"T", "T":"A", "G":"C", "C":"G"}
    rev_comp = ""

    for base in reversed(sequence):
        rev_comp += complement[base]

    return rev_comp


def dna_to_rna(sequence):
    return sequence.replace("T","U")

def read_fasta(file_path):
    sequences = {}
    header = ""
    seq = ""

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()

            if line.startswith(">"):
                if header:
                    sequences[header] = seq
                header = line[1:]
                seq = ""
            else:
                seq += line

        if header:
            sequences[header] = seq

    return sequences

file = "sample.fasta"

sequences = read_fasta(file)

for name, seq in sequences.items():
    print("Sequence:", name)
    print("Length:", len(seq))
    print("GC Content:", gc_content(seq))
    print("Reverse Complement:", reverse_complement(seq))
    print("RNA:", dna_to_rna(seq))
    print("----------------------")